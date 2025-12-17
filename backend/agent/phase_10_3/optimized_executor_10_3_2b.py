"""
PHASE 10.3.2b: Optimized Multi-Step Executor with Delta Snapshots
Combines Phase 10.3.2a optimizations (intent caching) with 10.3.2b (delta snapshots).

OPTIMIZATIONS:
1. Intent result caching (from 10.3.2a) - reuse LLM results
2. Delta-based snapshots (from 10.3.2b) - 50x smaller snapshots

EXPECTED PERFORMANCE:
- Phase 10.2: 1.45ms
- Phase 10.3.2a: 1.36ms (+6%)
- Phase 10.3.2b: 1.15ms (+20% from 10.2, +5.5% from 10.3.2a)
"""

import copy
import json
import hashlib
from typing import Dict, Any, Optional
from backend.agent import DesignEditAgent
from backend.agent.phase_10_2.models import (
    MultiStepPlan, StepExecutionResult, MultiStepExecutionResult,
    RollbackSnapshot, StepStatus
)
from backend.agent.phase_10_3.optimized_executor_10_3_2a_v2 import IntentResultCache
from backend.agent.phase_10_3.optimized_rollback_10_3_2b import OptimizedRollbackManager


class OptimizedMultiStepExecutor_10_3_2b:
    """
    PHASE 10.3.2b Optimized Executor
    
    Layers:
    1. Phase 10.3.2a: Intent result caching
    2. Phase 10.3.2b: Delta-based snapshots
    
    Result: Fast execution + minimal memory overhead
    """
    
    def __init__(self, agent: DesignEditAgent = None):
        """Initialize executor with all optimizations."""
        self.agent = agent or DesignEditAgent()
        self.rollback_manager = OptimizedRollbackManager()
        self.result_cache = IntentResultCache()
    
    def execute_plan(
        self,
        plan: MultiStepPlan,
        blueprint: Dict[str, Any],
    ) -> MultiStepExecutionResult:
        """
        Execute multi-step plan with intent caching + delta snapshots.
        
        Optimizations:
        1. Cache Phase 10.1 results (10.3.2a)
        2. Use delta snapshots instead of full copies (10.3.2b)
        
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
        
        # Clear snapshots for fresh start
        self.rollback_manager.clear_snapshots()
        
        # Execute each step
        current_blueprint = copy.deepcopy(blueprint)
        
        for step in plan.steps:
            # Reconstruct command for Phase 10.1 agent
            command = self._get_step_command(step)
            
            # OPTIMIZATION 10.3.2b: Create delta snapshot (not full copy)
            delta_snapshot = self.rollback_manager.create_snapshot(
                step.step_id,
                current_blueprint,
            )
            result.reasoning_trace.append(
                f"[Step {step.step_id}] Delta snapshot: {delta_snapshot.get_size_bytes()} bytes"
            )
            
            # OPTIMIZATION 10.3.2a: Try cached result first
            cached_result = self.result_cache.get_cached_result(command, current_blueprint)
            
            if cached_result:
                # Cache hit! Use cached result
                step_result = copy.deepcopy(cached_result)
                result.reasoning_trace.append(f"[Cache HIT] Step {step.step_id}")
            else:
                # Cache miss - execute via Phase 10.1 agent
                step_result = self._execute_single_step_via_agent(
                    step,
                    command,
                    current_blueprint,
                )
                
                # Cache successful results
                if step_result.success:
                    self.result_cache.cache_result(command, current_blueprint, step_result)
                    result.reasoning_trace.append(f"[Cache MISS] Step {step.step_id} cached")
                else:
                    result.reasoning_trace.append(f"[Cache MISS] Step {step.step_id} failed")
            
            result.step_results.append(step_result)
            
            # Check if step succeeded
            if not step_result.success:
                result.steps_failed += 1
                
                # Trigger rollback using delta snapshots
                rollback_blueprint = self.rollback_manager.rollback_to_latest_valid()
                if rollback_blueprint:
                    result.final_blueprint = rollback_blueprint
                    result.rollback_triggered = True
                    result.rollback_reason = f"Step {step.step_id} failed: {step_result.errors[0]}"
                    result.status = "failed"
                    result.reasoning_trace.append(
                        f"[ROLLBACK] {result.rollback_reason} (via deltas)"
                    )
                else:
                    result.status = "failed"
                    result.reasoning_trace.append("[ERROR] No snapshots for rollback")
                
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
            result.reasoning_trace.append(
                f"[SUCCESS] All {result.steps_total} steps completed"
            )
        elif result.steps_executed > 0 and result.steps_failed > 0:
            result.status = "partial"
        
        # Add performance stats
        stats = self.rollback_manager.get_stats()
        result.reasoning_trace.append(
            f"[STATS] Snapshots: {stats['snapshot_count']}, "
            f"Total size: {stats['total_size_bytes']} bytes, "
            f"Avg size: {stats['avg_size_bytes']:.0f} bytes/snapshot"
        )
        
        return result
    
    def _execute_single_step_via_agent(
        self,
        step,
        command: str,
        blueprint: Dict[str, Any],
    ) -> StepExecutionResult:
        """Execute single step through Phase 10.1 agent."""
        try:
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
    
    def _get_step_command(self, step) -> str:
        """Get the original command from the step."""
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
            return f"make {comp_id} {'bigger' if 'increase' in direction else 'smaller'}"
        elif intent == "edit_text":
            text = step.parameters.get('new_text', '')
            return f"change {comp_id} text to {text}" if text else f"edit {comp_id} text"
        elif intent == "modify_position":
            position = step.parameters.get('position', 'below')
            return f"move {comp_id} {position}"
        
        return f"Step {step.step_id}: {step.intent_type}"
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        return self.result_cache.get_stats()
    
    def get_snapshot_stats(self) -> Dict[str, Any]:
        """Get snapshot statistics."""
        return self.rollback_manager.get_stats()
