"""
PHASE 10.1 — STEP 2: CHANGE PLANNING

Generate a non-mutating plan for blueprint changes.
Pure planning - no modifications to blueprint.

Output is a detailed plan with constraints that Step 3 will execute.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass, field
from .intent_parser import ParsedIntent, IntentType


@dataclass
class FieldPatch:
    """Single field modification"""
    field_path: str  # e.g., "visual.bg_color"
    old_value: any
    new_value: any
    reason: str


@dataclass
class ComponentPatch:
    """Changes for one component"""
    component_id: str
    component_role: str
    component_type: str
    field_patches: List[FieldPatch] = field(default_factory=list)


@dataclass
class ChangePlan:
    """Complete plan (not executed yet)"""
    planned_patches: List[ComponentPatch]
    constraints: List[str]
    rationale: List[str]
    executable: bool = True
    safety_notes: List[str] = field(default_factory=list)


class ChangePlanner:
    """
    PHASE 10.1 STEP 2: Plan changes without modifying blueprint.
    
    Rules:
    - No blueprint mutation
    - Constraints are mandatory
    - Plan is explicit and traceable
    """
    
    # Schema-defined constraints
    SCHEMA_CONSTRAINTS = {
        "height": {"min": 20, "max": 600},
        "width": {"min": 20, "max": 500},
        "font_size": {"min": 8, "max": 72},
        "font_weight": {"options": ["normal", "bold", "light", "heavy"]},
        "button_height": {"min": 44},  # Accessibility minimum
    }
    
    def plan_changes(
        self,
        intent: ParsedIntent,
        blueprint: Dict
    ) -> ChangePlan:
        """
        Generate a plan for changes based on parsed intent.
        Does NOT modify blueprint.
        
        Args:
            intent: Parsed intent from Step 1
            blueprint: Current blueprint (read-only)
            
        Returns:
            ChangePlan with patches, constraints, and rationale
        """
        plan = ChangePlan(
            planned_patches=[],
            constraints=[],
            rationale=[],
            safety_notes=[]
        )
        
        # Step 1: Validate intent is actionable
        if intent.intent_type == IntentType.UNKNOWN:
            plan.executable = False
            plan.rationale.append("Intent not recognized - cannot plan changes")
            return plan
        
        if not intent.target:
            plan.executable = False
            plan.rationale.append("Target component not identified - cannot plan changes")
            return plan
        
        plan.rationale.append(f"Planning changes for {intent.target}")
        plan.rationale.append(f"Intent type: {intent.intent_type.value}")
        
        # Step 2: Find target components in blueprint
        target_components = self._find_components(intent.target, blueprint)
        
        if not target_components:
            plan.executable = False
            plan.rationale.append(f"No components matched target: {intent.target}")
            return plan
        
        plan.rationale.append(f"Found {len(target_components)} matching component(s)")
        
        # Step 3: Plan patch for each component
        for comp in target_components:
            patch = self._plan_component_patch(
                intent.intent_type,
                intent.parameters,
                comp,
                blueprint,
                plan
            )
            if patch:
                plan.planned_patches.append(patch)
                plan.rationale.append(f"Planned {len(patch.field_patches)} changes to '{comp['id']}'")
        
        # Step 4: Add mandatory constraints
        plan.constraints.extend(self._generate_constraints(intent.intent_type, blueprint))
        
        # Step 5: Final validation
        if not plan.planned_patches:
            plan.executable = False
            plan.rationale.append("No valid patches generated - cannot proceed")
        
        return plan
    
    def _find_components(self, target, blueprint: Dict) -> List[Dict]:
        """Find components matching the target criteria."""
        matches = []
        
        if "components" not in blueprint:
            return []
        
        for comp in blueprint["components"]:
            # Match by role
            if target.role and comp.get("role") == target.role:
                matches.append(comp)
            # Match by type
            elif target.component_type and comp.get("type") == target.component_type:
                matches.append(comp)
            # Match by text
            elif target.text_match and target.text_match.lower() in comp.get("text", "").lower():
                matches.append(comp)
        
        return matches
    
    def _plan_component_patch(
        self,
        intent_type: IntentType,
        parameters: Dict,
        component: Dict,
        blueprint: Dict,
        plan: ChangePlan
    ) -> Optional[ComponentPatch]:
        """Plan changes for a single component."""
        patch = ComponentPatch(
            component_id=component.get("id"),
            component_role=component.get("role"),
            component_type=component.get("type")
        )
        
        if intent_type == IntentType.MODIFY_COLOR:
            return self._plan_color_change(parameters, component, patch, plan)
        
        elif intent_type == IntentType.RESIZE_COMPONENT:
            return self._plan_resize(parameters, component, patch, plan)
        
        elif intent_type == IntentType.EDIT_TEXT:
            return self._plan_text_edit(parameters, component, patch, plan)
        
        elif intent_type == IntentType.MODIFY_STYLE:
            return self._plan_style_change(parameters, component, patch, plan)
        
        return patch if patch.field_patches else None
    
    def _plan_color_change(
        self,
        parameters: Dict,
        component: Dict,
        patch: ComponentPatch,
        plan: ChangePlan
    ) -> ComponentPatch:
        """Plan a color modification."""
        if "color" not in parameters:
            return patch
        
        new_color = parameters["color"]
        old_color = component.get("visual", {}).get("color", "")
        
        field_patch = FieldPatch(
            field_path="visual.color",
            old_value=old_color,
            new_value=new_color,
            reason=f"Color change requested: {old_color} → {new_color}"
        )
        patch.field_patches.append(field_patch)
        
        # Add constraint: color must be valid hex
        plan.constraints.append(f"Color must be valid hex code: {new_color}")
        
        return patch
    
    def _plan_resize(
        self,
        parameters: Dict,
        component: Dict,
        patch: ComponentPatch,
        plan: ChangePlan
    ) -> ComponentPatch:
        """Plan a size modification."""
        if "size_direction" not in parameters:
            return patch
        
        size_dir = parameters["size_direction"]
        current_height = component.get("visual", {}).get("height", 44)
        
        # Calculate new height
        if size_dir.startswith("increase"):
            percent = int(size_dir.split("_")[1])
            new_height = int(current_height * (1 + percent / 100))
        elif size_dir.startswith("decrease"):
            percent = int(size_dir.split("_")[1])
            new_height = int(current_height * (1 - percent / 100))
        else:
            new_height = current_height
        
        # For buttons, enforce minimum height
        if component.get("role") == "cta":
            new_height = max(new_height, self.SCHEMA_CONSTRAINTS["button_height"]["min"])
            plan.safety_notes.append(f"Button height enforced minimum: {new_height}px")
        
        field_patch = FieldPatch(
            field_path="visual.height",
            old_value=current_height,
            new_value=new_height,
            reason=f"Size {size_dir}: {current_height} → {new_height}px"
        )
        patch.field_patches.append(field_patch)
        
        # Add constraints
        min_h = self.SCHEMA_CONSTRAINTS["height"]["min"]
        max_h = self.SCHEMA_CONSTRAINTS["height"]["max"]
        plan.constraints.append(f"Height must be between {min_h} and {max_h}")
        
        return patch
    
    def _plan_text_edit(
        self,
        parameters: Dict,
        component: Dict,
        patch: ComponentPatch,
        plan: ChangePlan
    ) -> ComponentPatch:
        """Plan a text modification."""
        if "new_text" not in parameters:
            return patch
        
        new_text = parameters["new_text"]
        old_text = component.get("text", "")
        
        field_patch = FieldPatch(
            field_path="text",
            old_value=old_text,
            new_value=new_text,
            reason=f"Text change: '{old_text}' → '{new_text}'"
        )
        patch.field_patches.append(field_patch)
        
        # Add constraint
        plan.constraints.append(f"Text length should be < 100 chars")
        
        return patch
    
    def _plan_style_change(
        self,
        parameters: Dict,
        component: Dict,
        patch: ComponentPatch,
        plan: ChangePlan
    ) -> ComponentPatch:
        """Plan a style modification."""
        if "style" not in parameters:
            return patch
        
        style = parameters["style"]
        current_weight = component.get("visual", {}).get("font_weight", "normal")
        
        # Map style keywords to font-weight
        style_map = {
            "bold": "bold",
            "heavy": "bold",
            "light": "light",
            "italic": "italic",
        }
        
        new_weight = style_map.get(style, style)
        
        field_patch = FieldPatch(
            field_path="visual.font_weight",
            old_value=current_weight,
            new_value=new_weight,
            reason=f"Style change: {style} requested"
        )
        patch.field_patches.append(field_patch)
        
        return patch
    
    def _generate_constraints(self, intent_type: IntentType, blueprint: Dict) -> List[str]:
        """Generate schema constraints based on intent."""
        constraints = [
            "No component IDs may be modified",
            "No components may be deleted",
            "Component schema must remain valid",
            "All modifications must be to 'visual' or 'text' fields only",
        ]
        
        if intent_type == IntentType.RESIZE_COMPONENT:
            constraints.append("Component bbox must not overlap others")
            constraints.append("Component must stay within screen bounds")
        
        return constraints
