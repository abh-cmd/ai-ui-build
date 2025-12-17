"""
AGENT: Orchestrate full agentic pipeline.

INTENT → PLAN → PATCH → SIMULATE → VERIFY → APPLY → EXPLAIN

The heart of Phase 11. Deterministic, safe, production-ready.
"""

from typing import Dict, Any, Tuple, Optional
import copy
import json
from datetime import datetime

from .intent_graph import IntentGraph
from .planner import Planner
from .patch_generator import PatchGenerator
from .simulator import Simulator
from .verifier import Verifier
from .explainer import Explainer


class AgenticAgent:
    """Production-grade agentic AI engine for design edits."""
    
    def __init__(self):
        self.intent_graph = IntentGraph()
        self.planner = Planner()
        self.patch_generator = PatchGenerator()
        self.simulator = Simulator()
        self.verifier = Verifier()
        self.explainer = Explainer()
    
    def process(self, command: str, blueprint: Dict[str, Any]) -> Dict[str, Any]:
        """
        Full agentic pipeline: INTENT → PLAN → PATCH → SIMULATE → VERIFY → APPLY → EXPLAIN
        
        Args:
            command: User natural language command
            blueprint: Current blueprint (never modified)
        
        Returns:
            Response dict with modified blueprint, reasoning, confidence, success
        """
        try:
            # STEP 1: INTENT — Parse command into structured intents
            intents = self.intent_graph.parse(command, blueprint)
            
            if not intents:
                return self._error_response(
                    "Could not understand command",
                    command,
                    "No intents extracted"
                )
            
            # STEP 2: PLAN — Convert intents to execution plan
            plan = self.planner.plan(intents)
            
            # Detect conflicts
            conflict = self.planner.detect_conflicts(intents)
            if conflict:
                return self._error_response(
                    conflict,
                    command,
                    f"Conflict detected: {conflict}"
                )
            
            # STEP 3: PATCH — Generate JSON patches
            patches = []
            for intent in intents:
                intent_patches = self.patch_generator.generate(intent, blueprint)
                patches.extend(intent_patches)
            
            if not patches:
                return self._error_response(
                    "No patches generated",
                    command,
                    "Could not generate valid patches for intents"
                )
            
            # STEP 4: SIMULATE — Dry-run on cloned blueprint
            simulation_result = self.simulator.simulate(blueprint, patches)
            
            if not simulation_result.safe:
                # Safety check failed
                return self._error_response(
                    simulation_result.reason or "Safety check failed",
                    command,
                    f"Simulation failed: {simulation_result.reason}"
                )
            
            # STEP 5: VERIFY — Enforce all constraints
            modified = simulation_result.modified_blueprint
            
            verification_result = self.verifier.verify(modified, blueprint)
            
            if not verification_result.valid:
                return self._error_response(
                    "Blueprint failed validation",
                    command,
                    f"Verification errors: {'; '.join(verification_result.errors)}"
                )
            
            # STEP 6: APPLY — Patches are already applied to modified blueprint
            # (from simulation)
            
            # STEP 7: EXPLAIN — Generate human-readable explanation
            explanation = self.explainer.explain(
                command,
                intents,
                blueprint,
                modified,
                patches,
                simulation_result
            )
            
            # SUCCESS — Return response
            return {
                "modified_blueprint": modified,
                "reasoning": explanation.reasoning,
                "explanation": explanation.summary,
                "confidence": explanation.confidence,
                "success": True,
                "details": {
                    "intents": [
                        {
                            "type": i.type.value,
                            "target": i.target,
                            "value": i.value,
                            "confidence": i.confidence
                        }
                        for i in intents
                    ],
                    "patches_applied": len(patches),
                    "plan_complexity": self.planner.estimate_complexity(intents),
                    "simulation_risk": simulation_result.risk_score,
                    "warnings": simulation_result.warnings + verification_result.warnings
                }
            }
        
        except Exception as e:
            # Catch any unexpected errors
            return self._error_response(
                f"Unexpected error: {str(e)}",
                command,
                str(e)
            )
    
    def process_multi_step(self, commands: list[str], blueprint: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process multiple commands sequentially.
        
        Integrates with Phase 10.2 multi-step execution.
        Maintains determinism and rollback guarantees.
        """
        current_blueprint = copy.deepcopy(blueprint)
        applied_commands = []
        
        for command in commands:
            result = self.process(command, current_blueprint)
            
            if not result.get("success"):
                # Rollback: return to original
                return {
                    "modified_blueprint": blueprint,
                    "reasoning": f"Rolled back after command failed: {result.get('reasoning', '')}",
                    "success": False,
                    "failed_at_command": command,
                    "applied_commands": applied_commands
                }
            
            current_blueprint = result["modified_blueprint"]
            applied_commands.append({
                "command": command,
                "confidence": result.get("confidence", 0.9)
            })
        
        return {
            "modified_blueprint": current_blueprint,
            "reasoning": f"Applied {len(commands)} commands successfully",
            "success": True,
            "commands_applied": applied_commands,
            "confidence": sum(c["confidence"] for c in applied_commands) / len(applied_commands)
        }
    
    def _error_response(self, reason: str, command: str, details: str) -> Dict[str, Any]:
        """Generate error response."""
        return {
            "modified_blueprint": None,
            "reasoning": reason,
            "explanation": reason,
            "confidence": 0.0,
            "success": False,
            "details": {
                "error": details,
                "command": command
            }
        }
    
    def validate_determinism(self, command: str, blueprint: Dict[str, Any], runs: int = 3) -> bool:
        """
        Validate that same command always produces same result.
        
        Critical for production safety.
        """
        results = []
        
        for _ in range(runs):
            result = self.process(command, blueprint)
            results.append(json.dumps(result["modified_blueprint"], sort_keys=True))
        
        # All results should be identical
        return all(r == results[0] for r in results)
    
    def get_capabilities(self) -> Dict[str, Any]:
        """Return capability information."""
        return {
            "intent_types": [t.value for t in self.intent_graph.IntentType],
            "component_types": list(self.intent_graph.COMPONENT_TYPES.values()),
            "phases": ["intent_parsing", "planning", "patching", "simulation", "verification", "application", "explanation"],
            "guarantees": [
                "determinism",
                "immutability",
                "rollback_safety",
                "accessibility_checks",
                "schema_validation"
            ]
        }
