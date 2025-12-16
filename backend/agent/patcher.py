"""
PHASE 10.1 — STEP 3: PATCH APPLICATION

Apply the planned patch to blueprint safely.
Only modifies what was explicitly planned.
No schema changes, no deletions.
"""

from typing import Dict, Tuple
from copy import deepcopy
from .planner import ChangePlan


class Patcher:
    """
    PHASE 10.1 STEP 3: Apply planned patches to blueprint.
    
    Rules:
    - Modify ONLY allowed fields
    - No schema changes
    - No component deletion
    - Phase 10.1 = single-step edits only
    """
    
    # Allowed field paths for modification
    ALLOWED_PATHS = {
        "text",  # Component display text
        "visual.color",  # Text color
        "visual.bg_color",  # Background color
        "visual.height",  # Height
        "visual.width",  # Width
        "visual.font_weight",  # Bold, light, etc
        "visual.font_size",  # Font size
        "visual.padding",  # Padding
        "visual.border_radius",  # Border radius
    }
    
    def apply_patch(self, plan: ChangePlan, blueprint: Dict) -> Tuple[Dict, bool, str]:
        """
        Apply the planned patch to blueprint.
        
        Args:
            plan: ChangePlan from Step 2
            blueprint: Current blueprint (will be copied)
            
        Returns:
            Tuple of (patched_blueprint, success, message)
        """
        # Step 1: Validate plan is executable
        if not plan.executable:
            return blueprint, False, "Plan is not executable"
        
        if not plan.planned_patches:
            return blueprint, False, "Plan has no patches"
        
        # Step 2: Deep copy blueprint (don't mutate original)
        patched = deepcopy(blueprint)
        
        if "components" not in patched:
            return blueprint, False, "Blueprint has no components array"
        
        # Step 3: Apply each patch
        patches_applied = 0
        errors = []
        
        for component_patch in plan.planned_patches:
            success, error = self._apply_component_patch(
                component_patch,
                patched
            )
            
            if success:
                patches_applied += 1
            else:
                errors.append(error)
        
        # Step 4: Return results
        if patches_applied == 0:
            return blueprint, False, f"No patches applied. Errors: {'; '.join(errors)}"
        
        return patched, True, f"Applied {patches_applied} patch(es)"
    
    def _apply_component_patch(self, component_patch, blueprint: Dict) -> Tuple[bool, str]:
        """Apply patch to a single component."""
        # Find component by ID
        component = None
        for comp in blueprint.get("components", []):
            if comp.get("id") == component_patch.component_id:
                component = comp
                break
        
        if not component:
            return False, f"Component {component_patch.component_id} not found"
        
        # Apply each field patch
        for field_patch in component_patch.field_patches:
            success, error = self._apply_field_patch(
                field_patch,
                component,
                component_patch.component_id
            )
            
            if not success:
                return False, error
        
        return True, None
    
    def _apply_field_patch(self, field_patch, component: Dict, comp_id: str) -> Tuple[bool, str]:
        """Apply a single field modification."""
        # Step 1: Validate field path is allowed
        if field_patch.field_path not in self.ALLOWED_PATHS:
            return False, f"Field '{field_patch.field_path}' not allowed to modify"
        
        # Step 2: Parse field path (e.g., "visual.color" → ["visual", "color"])
        path_parts = field_patch.field_path.split(".")
        
        # Step 3: Navigate to nested field
        current = component
        for i, part in enumerate(path_parts[:-1]):
            if part not in current:
                current[part] = {}
            current = current[part]
            
            if not isinstance(current, dict):
                return False, f"Cannot navigate path {field_patch.field_path}: {part} is not a dict"
        
        # Step 4: Apply the change
        final_key = path_parts[-1]
        old_value = current.get(final_key)
        current[final_key] = field_patch.new_value
        
        return True, None
    
    def verify_patch_applied(
        self,
        original: Dict,
        patched: Dict,
        plan: ChangePlan
    ) -> Tuple[bool, str]:
        """
        Verify that patch was correctly applied.
        
        Returns:
            Tuple of (verified, message)
        """
        # Count changes
        changes_verified = 0
        
        for component_patch in plan.planned_patches:
            # Find original and patched components
            orig_comp = next(
                (c for c in original.get("components", []) 
                 if c.get("id") == component_patch.component_id),
                None
            )
            
            patch_comp = next(
                (c for c in patched.get("components", []) 
                 if c.get("id") == component_patch.component_id),
                None
            )
            
            if not patch_comp:
                return False, f"Component {component_patch.component_id} missing in patched blueprint"
            
            # Verify each field change
            for field_patch in component_patch.field_patches:
                path_parts = field_patch.field_path.split(".")
                
                # Get value from patched component
                patched_value = self._get_nested_value(patch_comp, path_parts)
                
                if patched_value != field_patch.new_value:
                    return False, (
                        f"Field {field_patch.field_path} not correctly applied: "
                        f"expected {field_patch.new_value}, got {patched_value}"
                    )
                
                changes_verified += 1
        
        return True, f"Verified {changes_verified} field changes"
    
    def _get_nested_value(self, obj: Dict, path: list):
        """Get value from nested dict using path."""
        current = obj
        for part in path:
            if isinstance(current, dict):
                current = current.get(part)
            else:
                return None
        return current
