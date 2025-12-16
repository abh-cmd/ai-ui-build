"""
PHASE 10.2 Orchestrator
Main orchestrator for multi-step agentic planning and execution.
"""

from typing import Dict, Any
from backend.agent import DesignEditAgent
from backend.agent.phase_10_2.models import MultiStepExecutionResult
from backend.agent.phase_10_2.decomposer import MultiIntentDecomposer
from backend.agent.phase_10_2.executor import MultiStepExecutor


class MultiStepAgent:
    """
    Main orchestrator for PHASE 10.2.
    Handles command decomposition, execution, and result formatting.
    """
    
    def __init__(self, edit_agent: DesignEditAgent = None):
        """
        Initialize multi-step agent.
        
        Args:
            edit_agent: Phase 10.1 agent for single-step edits
        """
        self.edit_agent = edit_agent or DesignEditAgent()
        self.decomposer = MultiIntentDecomposer()
        self.executor = MultiStepExecutor(self.edit_agent)
    
    def edit_multi_step(
        self,
        command: str,
        blueprint: Dict[str, Any],
    ) -> MultiStepExecutionResult:
        """
        Execute a complex multi-step command with full planning and rollback.
        
        Args:
            command: Natural language command (may contain multiple edits)
            blueprint: Starting blueprint state
            
        Returns:
            MultiStepExecutionResult with complete execution trace
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
        
        # Step 1: Decompose command
        result.reasoning_trace.append("="*60)
        result.reasoning_trace.append("PHASE 10.2: MULTI-STEP AGENTIC PLANNING")
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
            result.reasoning_trace.append("\nNo executable steps detected in command")
            result.confidence = 0.0
            return result
        
        # Step 2: Execute plan
        result.reasoning_trace.append("\n" + "="*60)
        result.reasoning_trace.append("EXECUTION PHASE")
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
        result.reasoning_trace.append(f"Steps: {result.steps_executed}/{result.steps_total} executed")
        if result.steps_failed > 0:
            result.reasoning_trace.append(f"Failed: {result.steps_failed}")
        if result.rollback_triggered:
            result.reasoning_trace.append(f"Rollback: YES - {result.rollback_reason}")
        else:
            result.reasoning_trace.append("Rollback: NO")
        result.reasoning_trace.append(f"Confidence: {result.confidence:.2f}")
        
        return result


def execute_multi_step_edit(
    command: str,
    blueprint: Dict[str, Any],
) -> MultiStepExecutionResult:
    """
    Convenience function to execute a multi-step edit.
    
    Args:
        command: Natural language command
        blueprint: Blueprint state
        
    Returns:
        MultiStepExecutionResult
    """
    agent = MultiStepAgent()
    return agent.edit_multi_step(command, blueprint)
