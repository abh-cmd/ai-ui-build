"""
EXPLAINER: Generate human-readable explanations of changes.

Converts technical changes into user-friendly explanations with confidence scores.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass


@dataclass
class Explanation:
    """Human-readable explanation of changes."""
    summary: str
    details: List[str]
    confidence: float
    reasoning: str


class Explainer:
    """Generate explanations for blueprint modifications."""
    
    def explain(
        self,
        command: str,
        intents: List[Any],
        original_blueprint: Dict[str, Any],
        modified_blueprint: Dict[str, Any],
        patches: List[Any],
        simulation_result: Optional[Any] = None
    ) -> Explanation:
        """
        Generate explanation for modifications.
        
        Args:
            command: Original user command
            intents: Extracted intents
            original_blueprint: Original state
            modified_blueprint: Modified state
            patches: Applied patches
            simulation_result: Result from simulator
        
        Returns:
            Explanation object with summary, details, confidence
        """
        details: List[str] = []
        confidence = 0.9
        
        # Summarize each intent
        intent_descriptions = []
        for intent in intents:
            desc = self._describe_intent(intent, original_blueprint, modified_blueprint)
            if desc:
                intent_descriptions.append(desc)
                details.append(desc)
        
        if not intent_descriptions:
            intent_descriptions.append("No changes made")
            confidence = 0.5
        
        # Build summary
        summary = f"Applied {len(intents)} edit(s): " + "; ".join(intent_descriptions[:2])
        if len(intent_descriptions) > 2:
            summary += f" and {len(intent_descriptions) - 2} more"
        
        # Calculate final confidence
        if simulation_result:
            # Reduce confidence based on warnings
            warning_count = len(simulation_result.warnings)
            risk_score = simulation_result.risk_score
            
            confidence = 0.9 - (warning_count * 0.1) - (risk_score * 0.2)
            confidence = max(0.1, min(1.0, confidence))
        
        # Build reasoning
        reasoning = self._build_reasoning(
            command,
            intents,
            original_blueprint,
            modified_blueprint,
            patches,
            simulation_result
        )
        
        return Explanation(
            summary=summary,
            details=details,
            confidence=confidence,
            reasoning=reasoning
        )
    
    def _describe_intent(
        self,
        intent: Any,
        original: Dict[str, Any],
        modified: Dict[str, Any]
    ) -> Optional[str]:
        """Describe a single intent in human terms."""
        from .intent_graph import IntentType
        
        target = intent.target or "page"
        value = intent.value or ""
        
        if intent.type == IntentType.RESIZE:
            return f"Resized {target} {value}"
        elif intent.type == IntentType.COLOR:
            return f"Changed {target} color to {value}"
        elif intent.type == IntentType.ALIGN:
            return f"Aligned {target} {value}"
        elif intent.type == IntentType.TEXT:
            return f"Changed {target} text to '{value}'"
        elif intent.type == IntentType.STYLE:
            return f"Applied {value} style to {target}"
        elif intent.type == IntentType.POSITION:
            return f"Moved {target}"
        elif intent.type == IntentType.VISIBILITY:
            action = "hid" if value == "hide" else "showed"
            return f"{action.capitalize()} {target}"
        elif intent.type == IntentType.DELETE:
            return f"Deleted {target}"
        elif intent.type == IntentType.CREATE:
            return f"Created new {target}"
        
        return None
    
    def _build_reasoning(
        self,
        command: str,
        intents: List[Any],
        original: Dict[str, Any],
        modified: Dict[str, Any],
        patches: List[Any],
        simulation_result: Optional[Any] = None
    ) -> str:
        """Build detailed reasoning for the changes."""
        reasons = []
        
        # Why we understood the command this way
        reasons.append(f"Parsed command: '{command}'")
        reasons.append(f"Identified {len(intents)} intent(s)")
        
        # What we changed
        if patches:
            reasons.append(f"Generated {len(patches)} patch operation(s)")
        
        # Safety assessment
        if simulation_result:
            if simulation_result.safe:
                reasons.append(f"Simulation passed safety checks (risk: {simulation_result.risk_score:.1%})")
                if simulation_result.warnings:
                    reasons.append(f"Note: {len(simulation_result.warnings)} warning(s) found")
            else:
                reasons.append(f"Safety check failed: {simulation_result.reason}")
        
        # Changes made
        changes = self._summarize_changes(original, modified)
        if changes:
            for change in changes[:3]:
                reasons.append(f"• {change}")
        
        return " → ".join(reasons)
    
    def _summarize_changes(self, original: Dict[str, Any], modified: Dict[str, Any]) -> List[str]:
        """Summarize specific changes made."""
        changes: List[str] = []
        
        # Token changes
        orig_tokens = original.get("tokens", {})
        mod_tokens = modified.get("tokens", {})
        
        for key in orig_tokens:
            if orig_tokens.get(key) != mod_tokens.get(key):
                old_val = orig_tokens.get(key)
                new_val = mod_tokens.get(key)
                
                if key == "primary_color":
                    changes.append(f"Primary color: {old_val} → {new_val}")
                elif key == "base_spacing":
                    changes.append(f"Base spacing: {old_val}px → {new_val}px")
        
        # Component changes
        orig_comps = original.get("components", [])
        mod_comps = modified.get("components", [])
        
        # Removed components
        if len(orig_comps) > len(mod_comps):
            removed = len(orig_comps) - len(mod_comps)
            changes.append(f"Removed {removed} component(s)")
        
        # Added components
        if len(mod_comps) > len(orig_comps):
            added = len(mod_comps) - len(orig_comps)
            changes.append(f"Added {added} component(s)")
        
        # Modified components
        for i in range(min(len(orig_comps), len(mod_comps))):
            if orig_comps[i] != mod_comps[i]:
                comp_id = mod_comps[i].get("id", f"component_{i}")
                
                # Check specific property changes
                if orig_comps[i].get("text") != mod_comps[i].get("text"):
                    changes.append(f"{comp_id}: Text updated")
                
                if orig_comps[i].get("visual") != mod_comps[i].get("visual"):
                    orig_h = orig_comps[i].get("visual", {}).get("height")
                    mod_h = mod_comps[i].get("visual", {}).get("height")
                    
                    if orig_h != mod_h:
                        changes.append(f"{comp_id}: Height {orig_h}px → {mod_h}px")
                    
                    orig_color = orig_comps[i].get("visual", {}).get("bg_color")
                    mod_color = mod_comps[i].get("visual", {}).get("bg_color")
                    
                    if orig_color and orig_color != mod_color:
                        changes.append(f"{comp_id}: Color {orig_color} → {mod_color}")
        
        return changes
    
    def explain_rejection(self, reason: str, command: str, errors: List[str]) -> Explanation:
        """Explain why an edit was rejected."""
        return Explanation(
            summary=f"Edit rejected: {reason}",
            details=errors,
            confidence=0.0,
            reasoning=f"Command '{command}' could not be applied safely. " +
                     f"Issues: {'; '.join(errors)}"
        )
