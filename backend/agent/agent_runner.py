"""
PHASE 10.1 — AGENTIC AI CORE

5-Step Deterministic Design Editing Pipeline:

STEP 1: Intent Parser     → Parse NL command → ParsedIntent
STEP 2: Change Planner    → Generate safe plan → ChangePlan
STEP 3: Patch Application → Apply patch → patched blueprint
STEP 4: Verifier          → Verify safety → pass/fail
STEP 5: Agent Response    → Return structured result

This is NOT a chatbot. It's deterministic, explainable, and verifiable.
All steps are mandatory. No steps may be skipped.
"""

from typing import Dict
from .intent_parser import IntentParser, IntentType
from .planner import Planner
from .patcher import Patcher
from .verifier import Verifier
from .result import AgentResult


def run_agent(command: str, blueprint: Dict) -> AgentResult:
    """
    Run the complete 5-step design editing agent.
    
    Args:
        command: Natural language command (e.g., "change button color to white")
        blueprint: Current blueprint JSON
        
    Returns:
        AgentResult with success status, patched blueprint, and reasoning
    """
    agent = DesignEditAgent()
    return agent.edit(command, blueprint)


class DesignEditAgent:
    """
    5-Step Agentic AI Core for deterministic design editing.
    
    Pipeline is non-negotiable:
    1. Parse intent
    2. Plan changes
    3. Apply patch
    4. Verify safety
    5. Return result
    """
    
    def __init__(self):
        """Initialize all 5 pipeline components."""
        self.parser = IntentParser()
        self.planner = Planner()
        self.patcher = Patcher()
        self.verifier = Verifier()
    
    def edit(self, command: str, blueprint: Dict) -> AgentResult:
        """
        Execute the 5-step design editing pipeline.
        
        Args:
            command: Natural language command
            blueprint: Current blueprint (will not be modified)
            
        Returns:
            AgentResult with complete reasoning trace
        """
        response = AgentResult(success=False)
        
        # STEP 1: INTENT PARSING
        response.reasoning.append("STEP 1: INTENT PARSING")
        response.reasoning.append("=" * 50)
        
        intent = self.parser.parse(command, blueprint)
        response.reasoning.extend(intent.reasoning)
        
        if intent.intent_type == IntentType.UNKNOWN:
            response.errors.append(f"Intent not recognized: {command}")
            response.reasoning.append("FAILED: Intent not recognized")
            return response
        
        response.reasoning.append(f"Intent parsed: {intent.intent_type.value}")
        response.reasoning.append(f"Confidence: {intent.confidence}")
        response.reasoning.append(f"Target: {intent.target}")
        response.reasoning.append(f"Parameters: {intent.parameters}")
        response.confidence = intent.confidence
        
        # STEP 2: CHANGE PLANNING
        response.reasoning.append("")
        response.reasoning.append("STEP 2: CHANGE PLANNING (NO MUTATION)")
        response.reasoning.append("=" * 50)
        
        plan = self.planner.plan_changes(intent, blueprint)
        response.reasoning.extend(plan.rationale)
        response.reasoning.extend(plan.constraints)
        
        if not plan.executable:
            response.errors.append("Plan is not executable")
            response.reasoning.append("FAILED: Plan not executable")
            return response
        
        response.reasoning.append(f"Plan generated with {len(plan.planned_patches)} patch(es)")
        
        for patch in plan.planned_patches:
            response.reasoning.append(f"[{len(patch.field_patches)}] {patch.component_id}: {len(patch.field_patches)} changes")
        
        # STEP 3: PATCH APPLICATION
        response.reasoning.append("")
        response.reasoning.append("STEP 3: PATCH APPLICATION")
        response.reasoning.append("=" * 50)
        
        patched_bp, patch_success, patch_msg = self.patcher.apply_patch(plan, blueprint)
        response.reasoning.append(patch_msg)
        
        if not patch_success:
            response.errors.append(f"Patch application failed: {patch_msg}")
            response.reasoning.append("FAILED: Patch not applied")
            return response
        
        # Verify patch was applied correctly
        verify_applied, verify_msg = self.patcher.verify_patch_applied(blueprint, patched_bp, plan)
        response.reasoning.append(verify_msg)
        
        if not verify_applied:
            response.errors.append(f"Patch verification failed: {verify_msg}")
            response.reasoning.append("FAILED: Patch not correctly applied")
            return response
        
        response.reasoning.append(f"Patch verified correct")
        
        # STEP 4: VERIFICATION (SAFETY CHECKS)
        response.reasoning.append("")
        response.reasoning.append("STEP 4: VERIFICATION (SAFETY CHECKS)")
        response.reasoning.append("=" * 50)
        
        verify_ok, verify_errors = self.verifier.verify_all(blueprint, patched_bp, plan)
        
        if not verify_ok:
            response.errors.extend(verify_errors)
            response.reasoning.append(f"Verification found {len(verify_errors)} error(s):")
            for error in verify_errors:
                response.reasoning.append(f"  - {error}")
            response.reasoning.append("FAILED: Safety verification did not pass")
            return response
        
        response.reasoning.append("Schema validity check: PASS")
        response.reasoning.append("Component types check: PASS")
        response.reasoning.append("Layout safety check: PASS")
        response.reasoning.append("Accessibility rules check: PASS")
        response.reasoning.append("Token consistency check: PASS")
        response.reasoning.append("Structure unchanged: PASS")
        
        # STEP 5: CONFIRMATION OUTPUT
        response.reasoning.append("")
        response.reasoning.append("STEP 5: CONFIRMATION OUTPUT")
        response.reasoning.append("=" * 50)
        
        response.patched_blueprint = patched_bp
        response.success = True
        response.safe = True
        response.summary = self._generate_summary(intent, plan)
        response.reasoning.append(f"Edit complete and verified")
        response.reasoning.append(f"Summary: {response.summary}")
        
        # Track changes
        for patch in plan.planned_patches:
            for field_patch in patch.field_patches:
                response.changes_applied.append(f"{patch.component_id}.{field_patch.field_path}")
        
        return response
    
    def _generate_summary(self, intent, plan) -> str:
        """Generate human-readable summary of changes."""
        intent_verb = {
            IntentType.MODIFY_COLOR: "Color changed to",
            IntentType.RESIZE_COMPONENT: "Component",
            IntentType.EDIT_TEXT: "Text changed to",
            IntentType.MODIFY_STYLE: "Style changed to",
            IntentType.REORDER_COMPONENT: "Component moved to",
            IntentType.MODIFY_POSITION: "Position changed to",
        }
        
        if intent.intent_type not in intent_verb:
            return "Design modified"
        
        verb = intent_verb[intent.intent_type]
        
        # Extract key parameter
        key_param = None
        if "color" in intent.parameters:
            key_param = intent.parameters["color"]
        elif "new_text" in intent.parameters:
            key_param = intent.parameters["new_text"]
        elif "size_direction" in intent.parameters:
            key_param = intent.parameters["size_direction"]
        elif "style" in intent.parameters:
            key_param = intent.parameters["style"]
        elif "position" in intent.parameters:
            key_param = intent.parameters["position"]
        
        if key_param:
            return f"{verb} {key_param}"
        else:
            return verb
