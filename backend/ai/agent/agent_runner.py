"""
PHASE 10.1 — AGENT RUNNER

Orchestrates the complete 5-step agentic pipeline:
1. Intent Parsing
2. Change Planning
3. Patch Application
4. Verification
5. Confirmation Output

No step may be skipped.
"""

from typing import Dict, List
from dataclasses import dataclass
from copy import deepcopy

from .intent_parser import IntentParser
from .change_planner import ChangePlanner
from .patch_engine import PatchEngine
from .verifier import Verifier


@dataclass
class AgentResponse:
    """Final structured output from the agent"""
    success: bool
    patched_blueprint: Dict = None
    summary: str = ""
    changes_applied: int = 0
    confidence: float = 0.0
    safe: bool = False
    reasoning: List[str] = None
    errors: List[str] = None


class DesignEditAgent:
    """
    PHASE 10.1 — AGENTIC AI CORE
    
    5-Step Pipeline for safe design editing:
    1. INTENT PARSING - understand command
    2. CHANGE PLANNING - plan without mutating
    3. PATCH APPLICATION - apply the plan
    4. VERIFICATION - safety checks
    5. CONFIRMATION OUTPUT - structured result
    
    This agent is deterministic, explainable, and fully testable.
    """
    
    def __init__(self):
        self.parser = IntentParser()
        self.planner = ChangePlanner()
        self.patcher = PatchEngine()
        self.verifier = Verifier()
    
    def edit(self, command: str, blueprint: Dict) -> AgentResponse:
        """
        Execute the complete 5-step pipeline.
        
        Args:
            command: Natural language edit command
            blueprint: Current blueprint JSON
            
        Returns:
            AgentResponse with complete reasoning and result
        """
        response = AgentResponse(
            success=False,
            reasoning=[],
            errors=[]
        )
        
        # ===== STEP 1: INTENT PARSING =====
        response.reasoning.append("=" * 60)
        response.reasoning.append("STEP 1: INTENT PARSING")
        response.reasoning.append("=" * 60)
        
        intent = self.parser.parse(command, blueprint)
        response.reasoning.extend(intent.reasoning)
        response.confidence = intent.confidence
        
        if intent.intent_type.value == "unknown":
            response.errors.append(f"Intent not recognized (confidence: {intent.confidence})")
            response.reasoning.append("❌ FAILED: Intent parsing unsuccessful")
            return response
        
        response.reasoning.append(f"Intent parsed: {intent.intent_type.value}")
        response.reasoning.append(f"Confidence: {intent.confidence}")
        response.reasoning.append(f"Target: {intent.target}")
        response.reasoning.append(f"Parameters: {intent.parameters}")
        
        # ===== STEP 2: CHANGE PLANNING =====
        response.reasoning.append("")
        response.reasoning.append("=" * 60)
        response.reasoning.append("STEP 2: CHANGE PLANNING (NO MUTATION)")
        response.reasoning.append("=" * 60)
        
        plan = self.planner.plan_changes(intent, blueprint)
        response.reasoning.extend(plan.rationale)
        response.reasoning.extend([f"Constraint: {c}" for c in plan.constraints])
        
        if not plan.executable:
            response.errors.append("Change plan not executable")
            response.reasoning.append("❌ FAILED: Planning unsuccessful")
            return response
        
        response.reasoning.append(f"Plan generated with {len(plan.planned_patches)} patch(es)")
        for i, patch in enumerate(plan.planned_patches):
            response.reasoning.append(
                f"  [{i+1}] {patch.component_id}: {len(patch.field_patches)} changes"
            )
        
        # ===== STEP 3: PATCH APPLICATION =====
        response.reasoning.append("")
        response.reasoning.append("=" * 60)
        response.reasoning.append("STEP 3: PATCH APPLICATION")
        response.reasoning.append("=" * 60)
        
        patched_bp, patch_success, patch_msg = self.patcher.apply_patch(plan, blueprint)
        response.reasoning.append(patch_msg)
        
        if not patch_success:
            response.errors.append(patch_msg)
            response.reasoning.append("❌ FAILED: Patch application unsuccessful")
            return response
        
        response.reasoning.append(f"Patch applied successfully")
        
        # Verify patch was applied correctly
        verify_applied, verify_msg = self.patcher.verify_patch_applied(blueprint, patched_bp, plan)
        response.reasoning.append(verify_msg)
        
        if not verify_applied:
            response.errors.append(f"Patch verification failed: {verify_msg}")
            response.reasoning.append("FAILED: Patch not correctly applied")
            return response
        
        response.reasoning.append(f"Patch verified correct")
        response.changes_applied = len(plan.planned_patches)
        
        # ===== STEP 4: VERIFICATION =====
        response.reasoning.append("")
        response.reasoning.append("=" * 60)
        response.reasoning.append("STEP 4: VERIFICATION (SAFETY CHECKS)")
        response.reasoning.append("=" * 60)
        
        all_valid, errors = self.verifier.verify_all(blueprint, patched_bp, plan)
        
        if errors:
            response.errors.extend(errors)
            response.reasoning.append(f"❌ Verification found {len(errors)} error(s):")
            for err in errors:
                response.reasoning.append(f"  - {err}")
            response.reasoning.append("❌ FAILED: Safety verification did not pass")
            return response
        
        response.reasoning.append("Schema validity check: PASS")
        response.reasoning.append("Component types check: PASS")
        response.reasoning.append("Layout safety check: PASS")
        response.reasoning.append("Accessibility rules check: PASS")
        response.reasoning.append("Token consistency check: PASS")
        response.reasoning.append("Structure unchanged: PASS")
        response.safe = True
        
        # ===== STEP 5: CONFIRMATION OUTPUT =====
        response.reasoning.append("")
        response.reasoning.append("=" * 60)
        response.reasoning.append("STEP 5: CONFIRMATION OUTPUT")
        response.reasoning.append("=" * 60)
        
        response.patched_blueprint = patched_bp
        response.success = True
        response.summary = self._generate_summary(intent, plan)
        response.reasoning.append(f"Edit complete and verified")
        response.reasoning.append(f"Summary: {response.summary}")
        
        return response
    
    def _generate_summary(self, intent, plan) -> str:
        """Generate human-readable summary of changes."""
        if intent.intent_type.value == "modify_color":
            color = intent.parameters.get("color", "requested color")
            return f"Color changed to {color}"
        
        elif intent.intent_type.value == "resize_component":
            size_dir = intent.parameters.get("size_direction", "resized")
            return f"Component {size_dir}"
        
        elif intent.intent_type.value == "edit_text":
            new_text = intent.parameters.get("new_text", "")
            return f"Text changed to '{new_text}'"
        
        elif intent.intent_type.value == "modify_style":
            style = intent.parameters.get("style", "styled")
            return f"Component {style} style applied"
        
        else:
            return "Component modified"


def run_agent(command: str, blueprint: Dict) -> Dict:
    """
    Quick runner function for API integration.
    
    Returns:
        Dict with response structure
    """
    agent = DesignEditAgent()
    response = agent.edit(command, blueprint)
    
    return {
        "success": response.success,
        "patched_blueprint": response.patched_blueprint,
        "summary": response.summary,
        "changes_applied": response.changes_applied,
        "confidence": response.confidence,
        "safe": response.safe,
        "reasoning": response.reasoning,
        "errors": response.errors,
    }
