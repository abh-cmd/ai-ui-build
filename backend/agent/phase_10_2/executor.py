"""
PHASE 10.2 Execution Engine
Executes multi-step plans with verification and rollback.
"""

import copy
from typing import List, Dict, Any, Optional
from backend.agent import DesignEditAgent
from backend.agent.phase_10_2.models import (
    MultiStepPlan, StepExecutionResult, MultiStepExecutionResult,
    RollbackSnapshot, StepStatus
)
from backend.agent.phase_10_2.rollback import RollbackManager


class MultiStepExecutor:
    """
    Executes multi-step plans with verification and rollback on failure.
    """
    
    def __init__(self, agent: DesignEditAgent = None):
        """
        Initialize executor.
        
        Args:
            agent: Phase 10.1 design edit agent (creates new if None)
        """
        self.agent = agent or DesignEditAgent()
        self.rollback_manager = RollbackManager()
    
    def execute_plan(
        self,
        plan: MultiStepPlan,
        blueprint: Dict[str, Any],
    ) -> MultiStepExecutionResult:
        """
        Execute a multi-step plan with full verification and rollback.
        
        Args:
            plan: MultiStepPlan to execute
            blueprint: Starting blueprint state
            
        Returns:
            MultiStepExecutionResult with complete execution details
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
            result.reasoning_trace.append(f"\n--- EXECUTING STEP {step.step_id} ---")
            result.reasoning_trace.append(f"Intent: {step.intent_type}")
            result.reasoning_trace.append(f"Command: {step.command}")
            
            # Create snapshot before step
            snapshot = self.rollback_manager.create_snapshot(step.step_id, current_blueprint)
            result.reasoning_trace.append(f"Snapshot created before step {step.step_id}")
            
            # Execute step using Phase 10.1 agent
            step_result = self._execute_single_step(step, current_blueprint)
            result.step_results.append(step_result)
            
            # Check if step succeeded
            if not step_result.success:
                result.reasoning_trace.append(f"Step {step.step_id} FAILED: {step_result.errors}")
                result.steps_failed += 1
                
                # Trigger rollback
                rollback_blueprint = self.rollback_manager.rollback_to_latest_valid()
                if rollback_blueprint:
                    result.final_blueprint = rollback_blueprint
                    result.rollback_triggered = True
                    result.rollback_reason = f"Step {step.step_id} failed: {step_result.errors[0]}"
                    result.status = "failed"
                    result.reasoning_trace.append(f"ROLLBACK TRIGGERED: {result.rollback_reason}")
                else:
                    result.status = "failed"
                    result.reasoning_trace.append("CRITICAL: Could not rollback - no snapshots available")
                
                # Do not execute remaining steps
                break
            
            # Step succeeded
            result.steps_executed += 1
            result.changes_applied.append(step_result.summary)
            result.reasoning_trace.append(f"Step {step.step_id} SUCCESS: {step_result.summary}")
            
            # Update current blueprint for next step
            current_blueprint = step_result.patched_blueprint
        
        # All steps succeeded
        if result.steps_failed == 0 and result.steps_executed == result.steps_total:
            result.final_blueprint = current_blueprint
            result.status = "success"
            result.reasoning_trace.append("\nAll steps completed successfully")
        elif result.steps_executed > 0 and result.steps_failed > 0:
            result.status = "partial"
        
        return result
    
    def _execute_single_step(
        self,
        step,
        blueprint: Dict[str, Any],
    ) -> StepExecutionResult:
        """
        Execute a single step through Phase 10.1 agent.
        
        Args:
            step: PlanStep to execute
            blueprint: Current blueprint state
            
        Returns:
            StepExecutionResult with execution details
        """
        try:
            # Reconstruct a more explicit command for Phase 10.1 agent
            command = self._reconstruct_command(step, blueprint)
            
            # Use Phase 10.1 agent to execute
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
            # Execution failed
            return StepExecutionResult(
                step_id=step.step_id,
                step=step,
                success=False,
                safe=False,
                errors=[f"Execution error: {str(e)}"],
            )
    
    def _reconstruct_command(self, step, blueprint: Dict[str, Any]) -> str:
        """Reconstruct a more explicit command for Phase 10.1 agent"""
        comp_id = step.target.get('id', 'component')
        intent = step.intent_type
        
        if intent == "modify_color":
            color = step.parameters.get('color')
            if color:
                # Find color name from token map
                tokens = blueprint.get('tokens', {}).get('colors', {})
                color_name = None
                for name, code in tokens.items():
                    if code == color:
                        color_name = name
                        break
                if color_name:
                    return f"change {comp_id} color to {color_name}"
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
        
        elif intent == "modify_style":
            if step.parameters.get('font_weight') == 'bold':
                return f"make {comp_id} bold"
        
        elif intent == "modify_position":
            position = step.parameters.get('position', 'below')
            return f"move {comp_id} {position}"
        
        # Fallback to original command
        return step.command
