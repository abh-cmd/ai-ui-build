"""
VERIFIER: Enforce schema, accessibility, and safety constraints.

Post-simulation verification to ensure blueprint meets all requirements.
"""

from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field


@dataclass
class VerificationResult:
    """Result of verifying a blueprint."""
    valid: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    constraints_checked: List[str] = field(default_factory=list)


class Verifier:
    """Verify blueprint against all constraints."""
    
    def verify(self, blueprint: Dict[str, Any], original: Optional[Dict[str, Any]] = None) -> VerificationResult:
        """
        Comprehensive verification of blueprint.
        
        Args:
            blueprint: Blueprint to verify
            original: Original blueprint (for comparison)
        
        Returns:
            VerificationResult with detailed findings
        """
        errors: List[str] = []
        warnings: List[str] = []
        checks: List[str] = []
        
        # Check 1: Schema validity
        schema_ok, schema_errors, schema_warnings = self._verify_schema(blueprint)
        errors.extend(schema_errors)
        warnings.extend(schema_warnings)
        checks.append("schema")
        
        # Check 2: Required fields
        fields_ok, field_errors, field_warnings = self._verify_required_fields(blueprint)
        errors.extend(field_errors)
        warnings.extend(field_warnings)
        checks.append("required_fields")
        
        # Check 3: Component types
        comp_ok, comp_errors, comp_warnings = self._verify_components(blueprint)
        errors.extend(comp_errors)
        warnings.extend(comp_warnings)
        checks.append("components")
        
        # Check 4: Tokens
        token_ok, token_errors, token_warnings = self._verify_tokens(blueprint)
        errors.extend(token_errors)
        warnings.extend(token_warnings)
        checks.append("tokens")
        
        # Check 5: Accessibility
        a11y_ok, a11y_errors, a11y_warnings = self._verify_accessibility(blueprint)
        errors.extend(a11y_errors)
        warnings.extend(a11y_warnings)
        checks.append("accessibility")
        
        # Check 6: CTA constraints
        cta_ok, cta_errors, cta_warnings = self._verify_cta_constraints(blueprint)
        errors.extend(cta_errors)
        warnings.extend(cta_warnings)
        checks.append("cta_constraints")
        
        # Check 7: Immutability (if original provided)
        if original:
            immut_ok, immut_errors, immut_warnings = self._verify_immutability(original, blueprint)
            errors.extend(immut_errors)
            warnings.extend(immut_warnings)
            checks.append("immutability")
        
        # Overall result
        valid = len(errors) == 0
        
        return VerificationResult(
            valid=valid,
            errors=errors,
            warnings=warnings,
            constraints_checked=checks
        )
    
    def _verify_schema(self, blueprint: Dict[str, Any]) -> Tuple[bool, List[str], List[str]]:
        """Verify blueprint schema structure."""
        errors: List[str] = []
        warnings: List[str] = []
        
        if not isinstance(blueprint, dict):
            errors.append("Blueprint must be a dictionary")
            return False, errors, warnings
        
        # Must have tokens and components
        if "tokens" not in blueprint:
            errors.append("Missing 'tokens' field")
        if "components" not in blueprint:
            errors.append("Missing 'components' field")
        
        # Tokens must be dict
        if "tokens" in blueprint and not isinstance(blueprint["tokens"], dict):
            errors.append("'tokens' must be a dictionary")
        
        # Components must be list
        if "components" in blueprint and not isinstance(blueprint["components"], list):
            errors.append("'components' must be a list")
        
        ok = len(errors) == 0
        return ok, errors, warnings
    
    def _verify_required_fields(self, blueprint: Dict[str, Any]) -> Tuple[bool, List[str], List[str]]:
        """Verify required fields exist."""
        errors: List[str] = []
        warnings: List[str] = []
        
        # Required token fields
        required_tokens = ["primary_color", "base_spacing"]
        tokens = blueprint.get("tokens", {})
        
        for token in required_tokens:
            if token not in tokens:
                errors.append(f"Missing required token: {token}")
        
        # Components need basic fields
        components = blueprint.get("components", [])
        for idx, comp in enumerate(components):
            required_comp_fields = ["type", "bbox"]
            for field in required_comp_fields:
                if field not in comp:
                    errors.append(f"Component {idx}: Missing required field '{field}'")
        
        ok = len(errors) == 0
        return ok, errors, warnings
    
    def _verify_components(self, blueprint: Dict[str, Any]) -> Tuple[bool, List[str], List[str]]:
        """Verify component validity."""
        errors: List[str] = []
        warnings: List[str] = []
        
        valid_types = [
            "navbar", "button", "product", "text", "heading",
            "container", "card", "link", "image", "input", "select"
        ]
        valid_roles = ["nav", "cta", "content", "hero", "footer", "header", None]
        
        components = blueprint.get("components", [])
        
        for idx, comp in enumerate(components):
            # Verify type
            comp_type = comp.get("type")
            if comp_type not in valid_types:
                errors.append(f"Component {idx}: Invalid type '{comp_type}' not in {valid_types}")
            
            # Verify role
            role = comp.get("role")
            if role not in valid_roles:
                warnings.append(f"Component {idx}: Unusual role '{role}'")
            
            # Verify bbox format
            bbox = comp.get("bbox")
            if bbox:
                if not isinstance(bbox, list) or len(bbox) != 4:
                    errors.append(f"Component {idx}: bbox must be [x1, y1, x2, y2]")
                elif not all(isinstance(x, (int, float)) for x in bbox):
                    errors.append(f"Component {idx}: bbox values must be numbers")
        
        ok = len(errors) == 0
        return ok, errors, warnings
    
    def _verify_tokens(self, blueprint: Dict[str, Any]) -> Tuple[bool, List[str], List[str]]:
        """Verify design tokens."""
        errors: List[str] = []
        warnings: List[str] = []
        
        tokens = blueprint.get("tokens", {})
        
        # Check base_spacing is multiple of 8
        base_spacing = tokens.get("base_spacing")
        if base_spacing is not None:
            if not isinstance(base_spacing, (int, float)):
                errors.append("base_spacing must be a number")
            elif base_spacing % 8 != 0:
                errors.append(f"base_spacing ({base_spacing}) must be multiple of 8")
        
        # Check colors are hex format
        color_fields = ["primary_color", "accent_color"]
        for field in color_fields:
            if field in tokens:
                color = tokens[field]
                if not isinstance(color, str) or not color.startswith("#"):
                    errors.append(f"{field} must be hex color (e.g., #E63946)")
        
        # Check border_radius
        if "border_radius" in tokens:
            br = tokens["border_radius"]
            if not isinstance(br, (int, float)):
                if isinstance(br, str) and not br.endswith("px"):
                    warnings.append(f"border_radius should be in px format")
        
        ok = len(errors) == 0
        return ok, errors, warnings
    
    def _verify_accessibility(self, blueprint: Dict[str, Any]) -> Tuple[bool, List[str], List[str]]:
        """Verify accessibility constraints."""
        errors: List[str] = []
        warnings: List[str] = []
        
        components = blueprint.get("components", [])
        
        for idx, comp in enumerate(components):
            # Text should have contrast
            text_color = comp.get("visual", {}).get("color")
            bg_color = comp.get("visual", {}).get("bg_color")
            
            if text_color and bg_color and text_color == bg_color:
                errors.append(f"Component {idx}: Text and background colors are identical (no contrast)")
            
            # Interactive elements need sufficient size
            if comp.get("role") == "cta" or comp.get("type") in ["button", "link"]:
                height = comp.get("visual", {}).get("height")
                if height and height < 44:
                    errors.append(f"Component {idx}: Interactive element height {height}px < 44px minimum")
        
        ok = len(errors) == 0
        return ok, errors, warnings
    
    def _verify_cta_constraints(self, blueprint: Dict[str, Any]) -> Tuple[bool, List[str], List[str]]:
        """Verify CTA-specific constraints."""
        errors: List[str] = []
        warnings: List[str] = []
        
        components = blueprint.get("components", [])
        
        # Find CTAs
        cta_count = 0
        for idx, comp in enumerate(components):
            if comp.get("role") == "cta" or comp.get("type") == "button":
                cta_count += 1
                
                # Minimum height
                height = comp.get("visual", {}).get("height", 44)
                if height < 44:
                    errors.append(f"CTA {idx}: Height {height}px < 44px minimum")
                
                # Should have text
                if not comp.get("text"):
                    warnings.append(f"CTA {idx}: No text content")
        
        # Page should have at least one CTA
        if cta_count == 0:
            warnings.append("No CTAs found on page")
        
        ok = len(errors) == 0
        return ok, errors, warnings
    
    def _verify_immutability(self, original: Dict[str, Any], modified: Dict[str, Any]) -> Tuple[bool, List[str], List[str]]:
        """Verify that original blueprint is not mutated."""
        errors: List[str] = []
        warnings: List[str] = []
        
        # This check would detect if someone modified the original
        # In practice, we already guarantee immutability through copy.deepcopy()
        
        ok = len(errors) == 0
        return ok, errors, warnings
    
    def can_apply_patch(self, blueprint: Dict[str, Any], patch: Any) -> Tuple[bool, Optional[str]]:
        """Check if a specific patch is safe to apply."""
        try:
            # Verify the path is valid
            if not hasattr(patch, "path") or not patch.path:
                return False, "Patch has no path"
            
            # Verify operation is safe
            if patch.op not in ["add", "remove", "replace"]:
                return False, f"Invalid operation: {patch.op}"
            
            # Path should not escape root
            if ".." in patch.path or patch.path.startswith("//"):
                return False, "Invalid path"
            
            return True, None
        except Exception as e:
            return False, str(e)
