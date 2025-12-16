"""
PHASE 10.2 Multi-Intent Decomposer
Breaks complex natural language commands into ordered atomic steps.
"""

import re
from typing import List, Tuple, Dict, Any
from backend.agent.phase_10_2.models import PlanStep, MultiStepPlan, PlanStatus, StepStatus


class ConflictDetector:
    """Detects logical conflicts in multi-step plans"""
    
    CONFLICT_PATTERNS = [
        # (pattern1, pattern2, conflict_description)
        (r"delete|remove", r"resize|change|edit", "Cannot modify a component after deleting it"),
        (r"delete|remove", r"move|reorder", "Cannot move a component after deleting it"),
        (r"hide", r"resize|change", "Cannot modify a hidden component"),
    ]
    
    @staticmethod
    def detect_conflicts(command: str) -> List[str]:
        """Detect logical conflicts in a command"""
        conflicts = []
        command_lower = command.lower()
        
        for pattern1, pattern2, msg in ConflictDetector.CONFLICT_PATTERNS:
            if re.search(pattern1, command_lower) and re.search(pattern2, command_lower):
                conflicts.append(msg)
        
        return conflicts


class MultiIntentDecomposer:
    """
    Decomposes a single complex command into ordered atomic steps.
    Each step is executable by Phase 10.1 agent.
    """
    
    # Command separators that indicate multiple steps
    # Order matters: longest/most specific first
    SEPARATORS = [
        r"\s+then\s+",  # then
        r";\s*",  # semicolon
        r",\s+and\s+",  # comma and
        r"\s+and\s+",  # and
        r",\s*",  # comma
    ]
    
    # Keywords that indicate end of one clause and start of another
    CLAUSE_STARTS = [
        r"make\s+(?!.*color)",  # make (except "make...color" is one clause)
        r"change\s+",
        r"move\s+",
        r"resize\s+",
        r"delete\s+",
        r"add\s+",
    ]
    
    def decompose(self, command: str, blueprint: Dict[str, Any]) -> MultiStepPlan:
        """
        Decompose command into atomic steps.
        
        Returns: MultiStepPlan with ordered steps or detected conflicts
        """
        plan = MultiStepPlan(original_command=command)
        plan.reasoning.append(f"Decomposing command: {command}")
        
        # Check for conflicts
        conflicts = ConflictDetector.detect_conflicts(command)
        if conflicts:
            for conflict in conflicts:
                plan.add_conflict(conflict)
            plan.reasoning.append(f"Conflicts detected: {conflicts}")
            return plan
        
        # Split command into clauses
        clauses = self._split_into_clauses(command)
        plan.reasoning.append(f"Split into {len(clauses)} clause(s)")
        
        # Convert each clause to a step
        last_target = None  # Track the last mentioned component
        skipped_clauses = 0
        for i, clause in enumerate(clauses, 1):
            step = self._clause_to_step(clause.strip(), i, blueprint, last_target)
            if step:
                plan.steps.append(step)
                plan.reasoning.append(f"Step {i}: {step.intent_type} on {step.target}")
                last_target = step.target  # Remember this component for pronouns
            else:
                plan.reasoning.append(f"Step {i}: Failed to extract (skipped)")
                skipped_clauses += 1
        
        # If we skipped clauses and still have steps, mark as partial/invalid
        if skipped_clauses > 0:
            plan.status = PlanStatus.REJECTED
            plan.reasoning.append(f"REJECTED: {skipped_clauses} clause(s) could not be parsed")
        
        # Calculate overall confidence
        if plan.steps:
            avg_confidence = sum(s.parameters.get('_confidence', 0.9) for s in plan.steps) / len(plan.steps)
            plan.confidence = min(1.0, avg_confidence)
        
        plan.reasoning.append(f"Plan complete: {len(plan.steps)} steps, confidence {plan.confidence:.2f}")
        return plan
    
    def _split_into_clauses(self, command: str) -> List[str]:
        """Split command into logical clauses"""
        # Try each separator
        for separator in self.SEPARATORS:
            if re.search(separator, command):
                clauses = re.split(separator, command)
                return [c.strip() for c in clauses if c.strip()]
        
        # If no separator found, treat as single clause
        return [command]
    
    def _clause_to_step(self, clause: str, step_id: int, blueprint: Dict[str, Any], last_target: Dict[str, Any] = None) -> PlanStep:
        """Convert a single clause to a step"""
        clause_lower = clause.lower()
        
        # Detect intent type
        intent_type = self._detect_intent(clause)
        if not intent_type:
            return None
        
        # Extract target component
        target = self._extract_target(clause, blueprint)
        
        # If no target found and this looks like a pronoun reference, use last target
        if target is None and last_target is not None:
            if re.search(r"it|this|that|its|the", clause_lower):
                target = last_target
        
        if not target:
            return None
        
        # Extract parameters
        parameters = self._extract_parameters(clause, intent_type, blueprint)
        
        step = PlanStep(
            step_id=step_id,
            command=clause,
            intent_type=intent_type,
            target=target,
            parameters=parameters,
            reasoning=f"Extracted from: '{clause}'",
            status=StepStatus.PENDING,
        )
        
        return step
    
    def _detect_intent(self, clause: str) -> str:
        """Detect the intent type from a clause"""
        clause_lower = clause.lower()
        
        # Check for color keywords first (more specific)
        colors = ["white", "black", "red", "blue", "green", "gray", "#"]
        if any(color in clause_lower for color in colors) and re.search(r"color|to|change|make", clause_lower):
            return "modify_color"
        
        if re.search(r"resize|bigger|smaller|increase|decrease|make.*larger", clause_lower):
            return "resize_component"
        elif re.search(r"text|label", clause_lower) and re.search(r"change|to", clause_lower):
            return "edit_text"
        elif re.search(r"bold|italic|style|font", clause_lower):
            return "modify_style"
        elif re.search(r"move|reorder|position|above|below|left|right", clause_lower):
            return "modify_position"
        
        return None
    
    def _extract_target(self, clause: str, blueprint: Dict[str, Any]) -> Dict[str, Any]:
        """Extract target component from clause"""
        clause_lower = clause.lower()
        components = blueprint.get('components', [])
        
        # First, check if this might be referring to previous component (pronouns like "its", "it")
        # In multi-step context, pronouns refer to the last mentioned component
        # For now, we'll handle explicit mentions
        
        # Try to find component by text or keywords
        for comp in components:
            comp_id = comp.get('id', '').lower()
            comp_type = comp.get('type', '').lower()
            comp_role = comp.get('role', '').lower()
            comp_text = comp.get('text', '').lower()
            
            # Check if clause mentions this component
            if (comp_id in clause_lower or 
                comp_type in clause_lower or 
                comp_role in clause_lower or
                comp_text in clause_lower):
                return {
                    "id": comp.get('id'),
                    "type": comp_type,
                    "role": comp_role,
                }
        
        # Fallback: try to match by generic keywords
        if re.search(r"header|title|hero", clause_lower):
            for comp in components:
                if comp.get('role') == 'hero' or comp.get('type') == 'header':
                    return {
                        "id": comp.get('id'),
                        "type": comp.get('type'),
                        "role": comp.get('role'),
                    }
        
        if re.search(r"button|cta|action|click", clause_lower):
            for comp in components:
                if comp.get('role') == 'cta' or comp.get('type') == 'button':
                    return {
                        "id": comp.get('id'),
                        "type": comp.get('type'),
                        "role": comp.get('role'),
                    }
        
        if re.search(r"product|section|container", clause_lower):
            for comp in components:
                if comp.get('type') == 'container' or 'product' in comp.get('text', '').lower():
                    return {
                        "id": comp.get('id'),
                        "type": comp.get('type'),
                        "role": comp.get('role'),
                    }
        
        # If still no target and this is a position-related clause, try any component
        if re.search(r"below|above|move", clause_lower) and components:
            # Return the first button/CTA by default for "move" commands
            for comp in components:
                if comp.get('role') == 'cta' or comp.get('type') == 'button':
                    return {
                        "id": comp.get('id'),
                        "type": comp.get('type'),
                        "role": comp.get('role'),
                    }
        
        return None
    
    def _extract_parameters(self, clause: str, intent_type: str, blueprint: Dict[str, Any]) -> Dict[str, Any]:
        """Extract parameters based on intent type"""
        params = {}
        clause_lower = clause.lower()
        
        if intent_type == "modify_color":
            # Extract color
            colors = blueprint.get('tokens', {}).get('colors', {})
            for color_name, color_code in colors.items():
                if color_name in clause_lower:
                    params['color'] = color_code
                    break
            params['_confidence'] = 0.95
        
        elif intent_type == "resize_component":
            if re.search(r"bigger|larger|increase", clause_lower):
                params['size_direction'] = 'increase_20'
            elif re.search(r"smaller|decrease", clause_lower):
                params['size_direction'] = 'decrease_20'
            params['_confidence'] = 0.90
        
        elif intent_type == "edit_text":
            # Extract text to change to
            match = re.search(r"(?:to|as|into)\s+['\"]?([^'\"]+?)['\"]?(?:\s+and|\s+,|$)", clause)
            if match:
                params['new_text'] = match.group(1).strip()
            params['_confidence'] = 0.90
        
        elif intent_type == "modify_style":
            if re.search(r"bold", clause_lower):
                params['font_weight'] = 'bold'
            elif re.search(r"italic", clause_lower):
                params['font_style'] = 'italic'
            params['_confidence'] = 0.85
        
        elif intent_type == "modify_position":
            if re.search(r"below|under|beneath", clause_lower):
                params['position'] = 'below'
            elif re.search(r"above|over|on top", clause_lower):
                params['position'] = 'above'
            elif re.search(r"left", clause_lower):
                params['position'] = 'left'
            elif re.search(r"right", clause_lower):
                params['position'] = 'right'
            params['_confidence'] = 0.75
        
        return params
