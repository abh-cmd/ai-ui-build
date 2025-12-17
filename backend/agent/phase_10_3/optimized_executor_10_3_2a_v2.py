"""
PHASE 10.3.2a OPTIMIZATION - VERSION 2: Real Bottleneck Fix
Focus on reducing redundant Phase 10.1 LLM calls, not validation/serialization.

ROOT CAUSE ANALYSIS:
- Profiling shows Execute stage = 80.2% of time
- Bottleneck is Phase 10.1 agent (LLM calls) = ~1.1ms per step
- Validation/serialization = <0.1ms (negligible)

OPTIMIZATION STRATEGY:
1. Intent Result Caching: Cache LLM results by (command_hash, blueprint_hash)
2. Request Deduplication: Skip redundant LLM calls for identical requests
3. Maintain 100% determinism: Same input always returns same output

EXPECTED IMPROVEMENT: 15-25% (1.72ms → 1.30-1.46ms)
This targets the actual bottleneck instead of optimizing negligible overhead.
"""

import copy
import json
import hashlib
from typing import Dict, Any, Optional, Tuple
from backend.agent import DesignEditAgent
from backend.agent.phase_10_2.models import (
    MultiStepPlan, StepExecutionResult, MultiStepExecutionResult,
    RollbackSnapshot, StepStatus
)
from backend.agent.phase_10_2.rollback import RollbackManager


class IntentResultCache:
    """Cache Phase 10.1 agent results by intent hash."""
    
    def __init__(self, max_entries: int = 500):
        self.cache: Dict[str, StepExecutionResult] = {}
        self.max_entries = max_entries
        self.hits = 0
        self.misses = 0
        self.access_order = []  # For LRU eviction
    
    def compute_request_hash(self, command: str, blueprint: Dict[str, Any]) -> str:
        """
        Compute deterministic hash of (command, blueprint state).
        
        Key insight: Only components matter for deterministic results,
        not metadata like timestamps or animation state.
        """
        # Hash command
        cmd_hash = hashlib.md5(command.encode()).hexdigest()
        
        # Hash blueprint structure (just component data, not metadata)
        components = blueprint.get('components', [])
        bp_hash = hashlib.md5(
            json.dumps(components, sort_keys=True, separators=(',', ':')).encode()
        ).hexdigest()
        
        # Combine hashes
        return hashlib.md5(f"{cmd_hash}:{bp_hash}".encode()).hexdigest()
    
    def get_cached_result(self, command: str, blueprint: Dict[str, Any]) -> Optional[StepExecutionResult]:
        """Retrieve cached result if available."""
        request_hash = self.compute_request_hash(command, blueprint)
        
        if request_hash in self.cache:
            self.hits += 1
            # Move to end (most recently used)
            self.access_order.remove(request_hash)
            self.access_order.append(request_hash)
            return self.cache[request_hash]
        
        self.misses += 1
        return None
    
    def cache_result(
        self,
        command: str,
        blueprint: Dict[str, Any],
        result: StepExecutionResult,
    ) -> None:
        """Cache a Phase 10.1 agent result."""
        request_hash = self.compute_request_hash(command, blueprint)
        
        # LRU eviction
        if len(self.cache) >= self.max_entries and request_hash not in self.cache:
            oldest = self.access_order.pop(0)
            del self.cache[oldest]
        
        # Cache the result (deep copy for safety)
        self.cache[request_hash] = copy.deepcopy(result)
        
        # Update access order
        if request_hash in self.access_order:
            self.access_order.remove(request_hash)
        self.access_order.append(request_hash)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        total = self.hits + self.misses
        hit_rate = (self.hits / total * 100) if total > 0 else 0
        return {
            "cache_entries": len(self.cache),
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate_percent": hit_rate,
        }


class OptimizedMultiStepExecutor:
    """
    PHASE 10.3.2a Optimized Executor (Version 2)
    
    Real optimization: Cache Phase 10.1 agent results
    - Avoids redundant LLM calls for identical (command, blueprint) pairs
    - Maintains 100% determinism
    - Targets actual bottleneck (LLM calls = 80%+ of execution time)
    
    Expected improvement: 15-25% faster
    """
    
    def __init__(self, agent: DesignEditAgent = None):
        """Initialize optimized executor."""
        self.agent = agent or DesignEditAgent()
        self.rollback_manager = RollbackManager()
        self.result_cache = IntentResultCache()
    
    def execute_plan(
        self,
        plan: MultiStepPlan,
        blueprint: Dict[str, Any],
    ) -> MultiStepExecutionResult:
        """
        Execute a multi-step plan with intent result caching.
        
        Optimizations:
        - Cache Phase 10.1 agent results by (command, blueprint) hash
        - Skip redundant LLM calls for identical requests
        - Preserve all Phase 10.2 guarantees (determinism, rollback, etc.)
        
        Returns:
            MultiStepExecutionResult (identical to Phase 10.2 format)
        """
        # Check if plan is valid
        if not plan.is_valid():
            return MultiStepExecutionResult(
                status="conflicted",
                final_blueprint=blueprint,
                steps_executed=0,
                steps_failed=0,
                steps_total=len(plan.steps),
                rollback_triggered=False,
                rollback_reason="Plan has conflicts",
                confidence=0.0,
                reasoning_trace=plan.reasoning + ["Plan rejected due to conflicts"],
                step_results=[],
            )
        
        result = MultiStepExecutionResult(
            status="success",
            final_blueprint=copy.deepcopy(blueprint),
            steps_executed=0,
            steps_failed=0,
            steps_total=len(plan.steps),
            confidence=plan.confidence,
            reasoning_trace=plan.reasoning.copy(),
        )
        
        # Clear rollback snapshots for fresh start
        self.rollback_manager.clear_snapshots()
        
        # Execute each step
        current_blueprint = copy.deepcopy(blueprint)
        
        for step in plan.steps:
            # Reconstruct command for Phase 10.1 agent
            command = self._reconstruct_command(step, current_blueprint)
            
            # Create snapshot before step
            snapshot = self.rollback_manager.create_snapshot(step.step_id, current_blueprint)
            result.reasoning_trace.append(f"[Step {step.step_id}] Executing: {command[:60]}")
            
            # OPTIMIZATION: Try to get cached result first
            cached_result = self.result_cache.get_cached_result(command, current_blueprint)
            
            if cached_result:
                # Cache hit! Use cached result
                step_result = copy.deepcopy(cached_result)
                result.reasoning_trace.append(f"[Cache HIT] Reused result for step {step.step_id}")
            else:
                # Cache miss - call Phase 10.1 agent
                step_result = self._execute_single_step_via_agent(step, command, current_blueprint)
                
                # Cache the result for future use
                if step_result.success:
                    self.result_cache.cache_result(command, current_blueprint, step_result)
                    result.reasoning_trace.append(f"[Cache MISS] Cached result for step {step.step_id}")
                else:
                    result.reasoning_trace.append(f"[Cache MISS] Failed execution, not cached")
            
            result.step_results.append(step_result)
            
            # Check if step succeeded
            if not step_result.success:
                result.steps_failed += 1
                
                # Trigger rollback
                rollback_blueprint = self.rollback_manager.rollback_to_latest_valid()
                if rollback_blueprint:
                    result.final_blueprint = rollback_blueprint
                    result.rollback_triggered = True
                    result.rollback_reason = f"Step {step.step_id} failed: {step_result.errors[0]}"
                    result.status = "failed"
                    result.reasoning_trace.append(f"[ROLLBACK] {result.rollback_reason}")
                else:
                    result.status = "failed"
                    result.reasoning_trace.append("[ERROR] No snapshots available for rollback")
                
                break
            
            # Step succeeded
            result.steps_executed += 1
            result.changes_applied.append(step_result.summary)
            
            # Update current blueprint for next step
            current_blueprint = step_result.patched_blueprint
        
        # Finalize result
        if result.steps_failed == 0 and result.steps_executed == result.steps_total:
            result.final_blueprint = current_blueprint
            result.status = "success"
            result.reasoning_trace.append(f"[SUCCESS] All {result.steps_total} steps completed")
        elif result.steps_executed > 0 and result.steps_failed > 0:
            result.status = "partial"
        
        return result
    
    def _execute_single_step_via_agent(
        self,
        step,
        command: str,
        blueprint: Dict[str, Any],
    ) -> StepExecutionResult:
        """
        Execute a single step through Phase 10.1 agent.
        This is the expensive operation that we cache.
        """
        try:
            # Call Phase 10.1 agent (this is the bottleneck)
            agent_result = self.agent.edit(command, blueprint)
            
            step_result = StepExecutionResult(
                step_id=step.step_id,
                step=step,
                success=agent_result.success,
                safe=agent_result.safe,
                patched_blueprint=agent_result.patched_blueprint,
                summary=agent_result.summary,
                errors=agent_result.errors,
                verification_passed=agent_result.safe,
            )
            
            return step_result
            
        except Exception as e:
            return StepExecutionResult(
                step_id=step.step_id,
                step=step,
                success=False,
                safe=False,
                errors=[f"Execution error: {str(e)}"],
            )
    
    def _reconstruct_command(self, step, blueprint: Dict[str, Any]) -> str:
        """Get the original command from the step (same as Phase 10.2)."""
        # Use the original command from the step
        # This ensures compatibility with how Phase 10.1 agent expects it
        if hasattr(step, 'command'):
            return step.command
        
        # Fallback: reconstruct from intent
        comp_id = step.target.get('id', 'component') if hasattr(step.target, 'get') else 'component'
        intent = step.intent_type
        
        if intent == "modify_color":
            color = step.parameters.get('color')
            if color:
                return f"change {comp_id} color to {color}"
        
        elif intent == "resize_component":
            direction = step.parameters.get('size_direction', 'increase_20')
            if 'increase' in direction:
                return f"make {comp_id} bigger"
            else:
                return f"make {comp_id} smaller"
        
        elif intent == "edit_text":
            text = step.parameters.get('new_text', '')
            if text:
                return f"change {comp_id} text to {text}"
        
        elif intent == "modify_position":
            position = step.parameters.get('position', 'below')
            return f"move {comp_id} {position}"
        
        return f"Step {step.step_id}: {step.intent_type}"
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics for monitoring."""
        return self.result_cache.get_stats()
