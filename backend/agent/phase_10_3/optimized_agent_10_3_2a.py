"""
PHASE 10.3.2a: Optimized Multi-Step Agent (Version 2)
Wraps Phase 10.2 with 10.3.2a optimizations (intent result caching).

DESIGN:
- Inherits from Phase 10.2 MultiStepAgent
- Replaces executor with OptimizedMultiStepExecutor (V2)
- All other behavior identical (100% determinism preserved)

KEY CHANGE FROM V1:
V1 failed because it cached validation (negligible cost)
V2 caches Phase 10.1 LLM results (80%+ of cost) - REAL IMPROVEMENT
"""

from typing import Dict, Any
from backend.agent import DesignEditAgent
from backend.agent.phase_10_2 import MultiStepAgent as Phase102Agent
from backend.agent.phase_10_2.models import MultiStepExecutionResult
from backend.agent.phase_10_2.decomposer import MultiIntentDecomposer
from backend.agent.phase_10_3.optimized_executor_10_3_2a_v2 import OptimizedMultiStepExecutor


class OptimizedMultiStepAgent(Phase102Agent):
    """
    PHASE 10.3.2a Optimized Agent
    
    Optimization strategy:
    1. Use OptimizedMultiStepExecutor (validation cache + lazy serialization)
    2. Keep decomposition identical (no changes to planning)
    3. Keep all Phase 10.2 guarantees intact
    
    Expected improvement: ~10% faster
    """
    
    def __init__(self, edit_agent: DesignEditAgent = None):
        """Initialize optimized agent."""
        self.edit_agent = edit_agent or DesignEditAgent()
        self.decomposer = MultiIntentDecomposer()
        # KEY CHANGE: Use optimized executor
        self.executor = OptimizedMultiStepExecutor(self.edit_agent)
    
    def edit_multi_step(
        self,
        command: str,
        blueprint: Dict[str, Any],
    ) -> MultiStepExecutionResult:
        """
        Execute multi-step command with Phase 10.3.2a optimizations.
        
        Output: 100% identical to Phase 10.2 (determinism preserved)
        """
        result = MultiStepExecutionResult(
            status="success",
            final_blueprint=blueprint,
            steps_executed=0,
            steps_failed=0,
            steps_total=0,
            confidence=0.0,
            reasoning_trace=[],
        )
        
        # Step 1: Decompose command (identical to Phase 10.2)
        result.reasoning_trace.append("="*60)
        result.reasoning_trace.append("PHASE 10.2 (10.3.2a optimized)")
        result.reasoning_trace.append("="*60)
        result.reasoning_trace.append(f"Command: {command}")
        result.reasoning_trace.append("")
        
        plan = self.decomposer.decompose(command, blueprint)
        result.reasoning_trace.extend(plan.reasoning)
        
        # Check if decomposition found conflicts
        if not plan.is_valid():
            result.status = "conflicted"
            result.reasoning_trace.append("\nPLAN REJECTED - Conflicts detected:")
            for conflict in plan.conflicts:
                result.reasoning_trace.append(f"  - {conflict}")
            result.confidence = 0.0
            return result
        
        # No steps detected
        if not plan.steps:
            result.status = "failed"
            result.reasoning_trace.append("\nNo executable steps detected")
            result.confidence = 0.0
            return result
        
        # Step 2: Execute plan (WITH OPTIMIZATIONS)
        result.reasoning_trace.append("\n" + "="*60)
        result.reasoning_trace.append("EXECUTION (10.3.2a optimized)")
        result.reasoning_trace.append("="*60)
        
        execution_result = self.executor.execute_plan(plan, blueprint)
        
        # Merge results
        result.status = execution_result.status
        result.final_blueprint = execution_result.final_blueprint
        result.steps_executed = execution_result.steps_executed
        result.steps_failed = execution_result.steps_failed
        result.steps_total = execution_result.steps_total
        result.rollback_triggered = execution_result.rollback_triggered
        result.rollback_reason = execution_result.rollback_reason
        result.changes_applied = execution_result.changes_applied
        result.confidence = execution_result.confidence
        result.reasoning_trace.extend(execution_result.reasoning_trace)
        result.step_results = execution_result.step_results
        
        # Add final summary
        result.reasoning_trace.append("\n" + "="*60)
        result.reasoning_trace.append("FINAL RESULT")
        result.reasoning_trace.append("="*60)
        result.reasoning_trace.append(f"Status: {result.status}")
        result.reasoning_trace.append(f"Steps: {result.steps_executed}/{result.steps_total}")
        if result.steps_failed > 0:
            result.reasoning_trace.append(f"Failed: {result.steps_failed}")
        if result.rollback_triggered:
            result.reasoning_trace.append(f"Rollback: YES - {result.rollback_reason}")
        else:
            result.reasoning_trace.append("Rollback: NO")
        result.reasoning_trace.append(f"Confidence: {result.confidence:.2f}")
        
        # OPTIONAL: Log cache stats for monitoring
        cache_stats = self.executor.get_cache_stats()
        result.reasoning_trace.append(f"\nCache stats: {cache_stats['hits']} hits, {cache_stats['misses']} misses")
        
        return result


def execute_multi_step_edit_optimized(
    command: str,
    blueprint: Dict[str, Any],
) -> MultiStepExecutionResult:
    """Convenience function to execute multi-step edit with 10.3.2a optimizations."""
    agent = OptimizedMultiStepAgent()
    return agent.edit_multi_step(command, blueprint)
