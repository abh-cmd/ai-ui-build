"""
PHASE 10.1 — STEP 4: VERIFICATION

Critical safety checks before confirming patch.
All checks must pass or patch is rejected.
"""

from typing import Dict, Tuple, List
from .change_planner import ChangePlan


class Verifier:
    """
    PHASE 10.1 STEP 4: Verify patch safety and correctness.
    
    Checks:
    - Schema validity
    - Allowed component types
    - Layout safety (bbox overlap)
    - Accessibility (CTA height ≥ 44)
    - Token consistency
    
    ANY FAILURE → REJECT PATCH
    """
    
    # Valid component types
    VALID_COMPONENT_TYPES = {
        "header", "text", "button", "product_item",
        "image", "divider", "container", "label"
    }
    
    # Valid roles
    VALID_ROLES = {
        "hero", "content", "cta", "decoration", "product"
    }
    
    # Accessibility minimums
    ACCESSIBILITY_RULES = {
        "cta_button_height": 44,  # Minimum clickable height
        "text_font_size": 12,  # Minimum readable text
    }
    
    def verify_all(
        self,
        original_blueprint: Dict,
        patched_blueprint: Dict,
        plan: ChangePlan
    ) -> Tuple[bool, List[str]]:
        """
        Run all verification checks.
        
        Returns:
            Tuple of (all_pass, [error_messages])
        """
        errors = []
        
        # Check 1: Schema validity
        schema_valid, schema_errors = self._verify_schema(patched_blueprint)
        errors.extend(schema_errors)
        
        # Check 2: Component types are valid
        types_valid, type_errors = self._verify_component_types(patched_blueprint)
        errors.extend(type_errors)
        
        # Check 3: Layout safety (no overlaps)
        layout_safe, layout_errors = self._verify_layout_safety(patched_blueprint)
        errors.extend(layout_errors)
        
        # Check 4: Accessibility rules
        accessible, access_errors = self._verify_accessibility(patched_blueprint)
        errors.extend(access_errors)
        
        # Check 5: Token consistency
        tokens_valid, token_errors = self._verify_token_consistency(patched_blueprint)
        errors.extend(token_errors)
        
        # Check 6: No schema structure changes
        structure_ok, struct_errors = self._verify_structure_unchanged(original_blueprint, patched_blueprint)
        errors.extend(struct_errors)
        
        return len(errors) == 0, errors
    
    def _verify_schema(self, blueprint: Dict) -> Tuple[bool, List[str]]:
        """Verify blueprint matches expected schema."""
        errors = []
        
        # Must have components array
        if "components" not in blueprint:
            errors.append("Blueprint missing 'components' array")
            return False, errors
        
        if not isinstance(blueprint["components"], list):
            errors.append("'components' must be an array")
            return False, errors
        
        # Each component must have required fields
        for idx, comp in enumerate(blueprint["components"]):
            if not isinstance(comp, dict):
                errors.append(f"Component {idx} is not a dict")
                continue
            
            # Required fields
            for field in ["id", "type"]:
                if field not in comp:
                    errors.append(f"Component {idx} (id={comp.get('id')}) missing '{field}'")
        
        return len(errors) == 0, errors
    
    def _verify_component_types(self, blueprint: Dict) -> Tuple[bool, List[str]]:
        """Verify all components have valid types."""
        errors = []
        
        for comp in blueprint.get("components", []):
            comp_type = comp.get("type")
            comp_id = comp.get("id", "unknown")
            
            if comp_type not in self.VALID_COMPONENT_TYPES:
                errors.append(
                    f"Component '{comp_id}': invalid type '{comp_type}'. "
                    f"Valid types: {', '.join(sorted(self.VALID_COMPONENT_TYPES))}"
                )
            
            # Role check (if present)
            role = comp.get("role")
            if role and role not in self.VALID_ROLES:
                errors.append(
                    f"Component '{comp_id}': invalid role '{role}'. "
                    f"Valid roles: {', '.join(sorted(self.VALID_ROLES))}"
                )
        
        return len(errors) == 0, errors
    
    def _verify_layout_safety(self, blueprint: Dict) -> Tuple[bool, List[str]]:
        """Verify no bbox overlaps and components stay in bounds."""
        errors = []
        
        components = blueprint.get("components", [])
        
        # Get screen dimensions (typical values)
        # In real scenario, would come from tokens or blueprint meta
        screen_width = 500
        screen_height = 800
        
        bboxes = []
        
        for comp in components:
            bbox = comp.get("bbox")
            if not bbox or len(bbox) < 4:
                continue
            
            left, top, width, height = bbox[0], bbox[1], bbox[2], bbox[3]
            right = left + width
            bottom = top + height
            
            # Check bounds
            if left < 0 or top < 0 or right > screen_width or bottom > screen_height:
                errors.append(
                    f"Component '{comp.get('id')}' outside screen bounds: "
                    f"bbox=({left},{top},{width},{height}) vs screen({screen_width}×{screen_height})"
                )
            
            # Check overlaps with previous components
            for prev_comp, prev_bbox in bboxes:
                if self._bboxes_overlap(bbox, prev_bbox):
                    errors.append(
                        f"Component '{comp.get('id')}' overlaps with '{prev_comp.get('id')}'"
                    )
            
            bboxes.append((comp, bbox))
        
        return len(errors) == 0, errors
    
    def _bboxes_overlap(self, bbox1, bbox2) -> bool:
        """Check if two bboxes overlap."""
        if len(bbox1) < 4 or len(bbox2) < 4:
            return False
        
        x1_left, y1_top, w1, h1 = bbox1[0], bbox1[1], bbox1[2], bbox1[3]
        x2_left, y2_top, w2, h2 = bbox2[0], bbox2[1], bbox2[2], bbox2[3]
        
        x1_right, y1_bottom = x1_left + w1, y1_top + h1
        x2_right, y2_bottom = x2_left + w2, y2_top + h2
        
        return not (x1_right < x2_left or x2_right < x1_left or
                    y1_bottom < y2_top or y2_bottom < y1_top)
    
    def _verify_accessibility(self, blueprint: Dict) -> Tuple[bool, List[str]]:
        """Verify accessibility constraints."""
        errors = []
        
        for comp in blueprint.get("components", []):
            # CTA buttons must have min height
            if comp.get("role") == "cta":
                height = comp.get("visual", {}).get("height", 0)
                if height < self.ACCESSIBILITY_RULES["cta_button_height"]:
                    errors.append(
                        f"CTA button '{comp.get('id')}' height {height}px < "
                        f"minimum {self.ACCESSIBILITY_RULES['cta_button_height']}px"
                    )
            
            # Text must be readable
            if comp.get("type") == "text":
                font_size = comp.get("visual", {}).get("font_size", 0)
                if font_size < self.ACCESSIBILITY_RULES["text_font_size"]:
                    errors.append(
                        f"Text '{comp.get('id')}' font size {font_size}px < "
                        f"minimum {self.ACCESSIBILITY_RULES['text_font_size']}px"
                    )
        
        return len(errors) == 0, errors
    
    def _verify_token_consistency(self, blueprint: Dict) -> Tuple[bool, List[str]]:
        """Verify colors and tokens are consistent."""
        errors = []
        
        # Get available tokens
        tokens = blueprint.get("tokens", {})
        valid_colors = set(tokens.get("colors", {}).values())
        
        # Also accept common hex colors
        valid_colors.update({
            "#FFFFFF", "#000000", "#0000FF", "#FF0000",
            "#00FF00", "#FFFF00", "#FF00FF", "#00FFFF"
        })
        
        for comp in blueprint.get("components", []):
            visual = comp.get("visual", {})
            
            # Check colors
            color = visual.get("color")
            if color and color not in valid_colors:
                errors.append(
                    f"Component '{comp.get('id')}': color '{color}' not in tokens"
                )
            
            bg_color = visual.get("bg_color")
            if bg_color and bg_color not in valid_colors:
                errors.append(
                    f"Component '{comp.get('id')}': background color '{bg_color}' not in tokens"
                )
        
        return len(errors) == 0, errors
    
    def _verify_structure_unchanged(
        self,
        original: Dict,
        patched: Dict
    ) -> Tuple[bool, List[str]]:
        """Verify component IDs and count didn't change."""
        errors = []
        
        orig_ids = {c.get("id") for c in original.get("components", [])}
        patch_ids = {c.get("id") for c in patched.get("components", [])}
        
        # No deletions
        deleted = orig_ids - patch_ids
        if deleted:
            errors.append(f"Components deleted: {deleted}")
        
        # No additions
        added = patch_ids - orig_ids
        if added:
            errors.append(f"Components added: {added}")
        
        # Count must match
        if len(original.get("components", [])) != len(patched.get("components", [])):
            errors.append(
                f"Component count changed: {len(original.get('components', []))} "
                f"→ {len(patched.get('components', []))}"
            )
        
        return len(errors) == 0, errors
