# Phase 10.3.2b: Incremental Snapshots Optimization

**Status**: PLANNING  
**Objective**: Reduce snapshot overhead from full deep copies to delta-based incremental snapshots  
**Expected Gain**: 15-20% improvement  
**Cumulative Target**: +21-26% (6% from 10.3.2a + 15-20% from 10.3.2b)

---

## Problem Statement

### Current Bottleneck (After Phase 10.3.2a)
- Execute stage still takes ~1.36ms (down from 1.45ms)
- Primary cost: Phase 10.1 LLM agent calls (~80% of time)
- Secondary cost: Deep copy operations for snapshots (~15% of time)
- Other costs: Validation, serialization, rollback logic (<5%)

### Deep Copy Overhead
**Current approach (Phase 10.2):**
```python
# In RollbackManager.create_snapshot()
snapshot = copy.deepcopy(blueprint)  # Full deep copy of entire blueprint
```

**Problem:**
- For 20-component blueprint: Deep copy takes ~0.2-0.3ms
- For 100-component blueprint: Deep copy takes ~1-2ms
- Happens on EVERY STEP
- Multi-step execution: 5 steps = 1-2.5ms wasted on snapshots alone

**Solution: Delta-Based Snapshots**
- Only store CHANGES since previous snapshot
- Reconstruct full blueprint on rollback from delta chain
- Reduce snapshot size by 80-90%
- Improve snapshot creation speed by 15-20%

---

## Implementation Strategy

### Phase 10.3.2b: Delta Snapshots

**Key Components:**

1. **DeltaSnapshot Class**
   - Stores: `(step_id, changes, original_values)`
   - Changes: Only modified component properties
   - Not: Full component copies
   
2. **Optimized RollbackManager**
   - Replace: `snapshots: Dict[str, Dict]`
   - With: `snapshots: Dict[str, DeltaSnapshot]`
   - Add: `reconstruct_from_deltas()` method
   
3. **Safe Delta Tracking**
   - Before modifying component: Store original values
   - Apply: Only diff to snapshot
   - Reconstruct: Apply deltas in reverse on rollback
   
**Example:**
```python
# Current approach (Phase 10.2)
original_bp = {
    'components': [
        {'id': 'card1', 'color': 'red', 'size': 100, ...100 fields},
        {'id': 'card2', 'color': 'blue', 'size': 100, ...100 fields},
        # ... 20 components, each with 100+ fields
    ]
}
snapshot = deepcopy(original_bp)  # Copy everything
# Result: ~50KB snapshot per step

# Phase 10.3.2b approach
changes = {
    'card1': {'color': 'red→blue', 'size': 100→150}
}
snapshot = DeltaSnapshot(step_id=1, changes=changes, original={'color': 'red', 'size': 100})
# Result: ~500 bytes snapshot per step (100x smaller!)
```

**Rollback Logic:**
```python
def rollback_to_step(step_id):
    # Get delta snapshots from step_id to latest
    deltas = self.snapshots[step_id:]
    
    # Reconstruct blueprint by applying deltas in reverse
    blueprint = copy.deepcopy(current_blueprint)
    for delta in reversed(deltas):
        # Undo changes for this step
        for component_id, original_values in delta.original.items():
            blueprint['components'][find_index(component_id)] = original_values
    
    return blueprint
```

---

## Implementation Plan

### Step 1: Design DeltaSnapshot Class
- Define minimal delta representation
- Ensure deterministic reconstruction
- Add validation/safety checks

### Step 2: Modify RollbackManager
- Add delta snapshot support
- Keep Phase 10.2 interface (backward compatible)
- Add `create_delta_snapshot()` method
- Add `reconstruct_from_deltas()` method

### Step 3: Create OptimizedRollbackManager
- Inherits from RollbackManager
- Overrides snapshot creation to use deltas
- Maintains identical rollback behavior

### Step 4: Update Executor to Use Optimized RollbackManager
- Create: `OptimizedMultiStepExecutor_10_3_2b`
- Inherits from: `OptimizedMultiStepExecutor_10_3_2a_v2`
- Changes: Only rollback manager and snapshot creation
- Maintains: All Phase 10.3.2a optimizations (caching + deltas)

### Step 5: Benchmark & Validate
- Compare Phase 10.2 vs 10.3.2a vs 10.3.2b
- Measure: Snapshot creation time reduction
- Verify: Rollback works correctly
- Test: Memory stability with large blueprints

---

## Implementation Details

### DeltaSnapshot Data Structure

```python
@dataclass
class DeltaSnapshot:
    """Represents a delta-based snapshot of blueprint changes."""
    
    step_id: str
    timestamp: float
    
    # What changed in this step
    changes: Dict[str, Dict[str, Tuple[Any, Any]]]  # {component_id: {field: (old, new)}}
    
    # Original values (for rollback)
    original_state: Dict[str, Dict[str, Any]]  # {component_id: {field: value}}
    
    # For reconstruction
    parent_step_id: Optional[str] = None  # Chain to previous snapshot
    
    def compute_size_bytes(self) -> int:
        """Estimate memory usage of this delta."""
        return sys.getsizeof(json.dumps(self.__dict__))
    
    def rollback_apply(self, blueprint: Dict[str, Any]) -> Dict[str, Any]:
        """Apply inverse of changes to rollback to pre-step state."""
        result = copy.deepcopy(blueprint)
        for component_id, original_values in self.original_state.items():
            # Find component and restore original values
            for comp in result['components']:
                if comp['id'] == component_id:
                    comp.update(original_values)
                    break
        return result
```

### RollbackManager Modifications

```python
class OptimizedRollbackManager(RollbackManager):
    """Phase 10.3.2b: Uses delta snapshots instead of full deep copies."""
    
    def create_snapshot(self, step_id: str, blueprint: Dict[str, Any]) -> DeltaSnapshot:
        """
        Create delta snapshot instead of full deep copy.
        
        Approach:
        1. Compare current blueprint to previous snapshot
        2. Extract only changes
        3. Store minimal delta
        """
        # Get previous snapshot (if any)
        prev_snapshot = self.snapshots.get(self.latest_step_id)
        
        if not prev_snapshot:
            # First snapshot: use full copy (baseline)
            return DeltaSnapshot(
                step_id=step_id,
                timestamp=time.time(),
                changes={},
                original_state=self._extract_all_components(blueprint),
            )
        
        # Subsequent snapshots: extract only changes
        changes = self._compute_changes(prev_snapshot, blueprint)
        
        snapshot = DeltaSnapshot(
            step_id=step_id,
            timestamp=time.time(),
            changes=changes,
            original_state=changes,  # Store original values
            parent_step_id=self.latest_step_id,
        )
        
        self.snapshots[step_id] = snapshot
        self.latest_step_id = step_id
        
        return snapshot
    
    def _compute_changes(self, old_snapshot, new_blueprint) -> Dict[str, Dict]:
        """Compute what changed between snapshot and current blueprint."""
        changes = {}
        
        # For each component, find differences
        for comp in new_blueprint.get('components', []):
            comp_id = comp['id']
            
            # Find original component in old snapshot
            old_comp = self._find_component_in_snapshot(old_snapshot, comp_id)
            
            if old_comp and old_comp != comp:
                # Something changed
                changes[comp_id] = {
                    field: (old_comp.get(field), comp.get(field))
                    for field in set(old_comp.keys()) | set(comp.keys())
                    if old_comp.get(field) != comp.get(field)
                }
        
        return changes
    
    def rollback_to_latest_valid(self) -> Optional[Dict[str, Any]]:
        """Rollback using delta snapshots."""
        if not self.snapshots:
            return None
        
        # Get latest valid snapshot
        latest_snapshot = self.snapshots[self.latest_step_id]
        
        # Reconstruct blueprint from deltas
        return self._reconstruct_from_deltas(latest_snapshot)
    
    def _reconstruct_from_deltas(self, target_snapshot) -> Dict[str, Any]:
        """Reconstruct blueprint by replaying deltas from baseline."""
        # Start with original baseline
        blueprint = copy.deepcopy(target_snapshot.original_state)
        
        # Apply deltas in order
        for snapshot in self._get_delta_chain_to(target_snapshot):
            for comp_id, changes in snapshot.changes.items():
                # Apply each change
                pass  # Apply logic here
        
        return blueprint
```

---

## Risk Assessment

### Safety Risks
- **MEDIUM**: Delta reconstruction must be deterministic
- **Mitigation**: Extensive testing with rollback scenarios
- **Fallback**: If issues detected, revert to Phase 10.2 deep copies

### Performance Risks
- **LOW**: Delta computation could be slower than deepcopy for small blueprints
- **Mitigation**: Optimize delta detection algorithm
- **Fallback**: Use full copy for blueprints <10 components

### Complexity Risks
- **MEDIUM**: Delta-based rollback adds code complexity
- **Mitigation**: Thorough unit testing, separate layer
- **Fallback**: Keep Phase 10.2 approach as reference

---

## Testing Strategy

### Unit Tests
1. **Delta Computation**: Verify changes detected correctly
2. **Delta Reconstruction**: Verify blueprint restored accurately
3. **Rollback Scenarios**: Test multi-step rollbacks, edge cases
4. **Determinism**: Same input → same rollback result

### Integration Tests
1. **Multi-step Execution**: Full workflows with deltas
2. **Memory Usage**: Compare snapshot sizes Phase 10.2 vs 10.3.2b
3. **Performance**: Benchmark snapshot creation time
4. **Large Blueprints**: Test with 100+ components

### Regression Tests
- Run all Phase 10.3 tests
- Verify Phase 10.2 guarantees maintained
- Check no performance regressions from 10.3.2a

---

## Success Criteria

| Metric | Target | Phase 10.2 | Phase 10.3.2a | Phase 10.3.2b |
|--------|--------|-----------|---------------|---------------|
| Avg Execution | <1.0ms | 1.45ms | 1.36ms | ~1.15ms |
| Snapshot Size | <1KB avg | ~50KB | ~50KB | ~1KB |
| Snapshot Time | <0.1ms | ~0.2ms | ~0.2ms | ~0.02ms |
| Determinism | ✓ | ✓ | ✓ | ✓ |
| Rollback Works | ✓ | ✓ | ✓ | ✓ |
| Improvement % | - | - | +6% | +20% (cumulative +26%) |

---

## Timeline

- **Design**: 30 minutes
- **Implementation**: 1-2 hours
- **Testing**: 1-2 hours
- **Total**: 2-4 hours

---

## Next Steps (After 10.3.2b)

If 10.3.2b successful (+20% improvement achieved):
- **Phase 10.3.2c**: Batch Processing (30-40% improvement)
- **Total Optimization**: +26% (10.3.2a + 10.3.2b) + pending 10.3.2c

If 10.3.2b underperforms:
- **Evaluate**: Skip to 10.3.2c or accept current performance
- **Decision Point**: Is 6% improvement (10.3.2a alone) sufficient?

---

## Files to Create/Modify

### New Files
- `backend/agent/phase_10_3/optimized_rollback_10_3_2b.py`
- `backend/agent/phase_10_3/optimized_executor_10_3_2b.py`
- `backend/agent/phase_10_3/optimized_agent_10_3_2b.py`

### Modified Files
- `backend/agent/phase_10_3/benchmark_10_3_2a.py` → `benchmark_10_3_2b.py`

### Testing
- Add delta snapshot tests to `test_suite.py`
- Create rollback scenario tests

---

## Conclusion

Phase 10.3.2b targets the secondary bottleneck (snapshot overhead) with a well-defined, low-risk implementation. Delta-based snapshots can reduce snapshot size by 100x while maintaining identical rollback behavior. Expected 15-20% improvement brings cumulative optimization to +26% toward the 50% target.

Ready to proceed when authorized.
