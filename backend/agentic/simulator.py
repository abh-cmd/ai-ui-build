"""
SIMULATOR: Dry-run patches on cloned blueprint to detect conflicts.

Critically important for safety. Runs patches on a clone and checks for:
- Layout overlap
- Accessibility violations
- Token conflicts
- Component validity
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
import copy


@dataclass
class SimulationResult:
    """Result of simulating patches on a blueprint."""
    safe: bool
    reason: Optional[str] = None
    diff: Dict[str, Any] = field(default_factory=dict)
    risk_score: float = 0.0  # 0.0 to 1.0
    warnings: List[str] = field(default_factory=list)
    modified_blueprint: Optional[Dict[str, Any]] = None


class Simulator:
    """Simulate patches without modifying original blueprint."""
    
    def simulate(self, blueprint: Dict[str, Any], patches: List[Any]) -> SimulationResult:
        """
        Dry-run patches on cloned blueprint.
        
        Args:
            blueprint: Original blueprint (not modified)
            patches: List of JSONPatch operations to apply
        
        Returns:
            SimulationResult with safety verdict and diff
        """
        # Clone blueprint for simulation
        simulated = copy.deepcopy(blueprint)
        
        # Apply patches
        from .patch_generator import PatchGenerator
        generator = PatchGenerator()
        
        try:
            simulated = generator.apply_patches(simulated, patches)
        except Exception as e:
            return SimulationResult(
                safe=False,
                reason=f"Patch application failed: {str(e)}",
                risk_score=1.0
            )
        
        # Run safety checks
        warnings: List[str] = []
        risk_score = 0.0
        
        # Check 1: Layout validity
        layout_ok, layout_warnings = self._check_layout(simulated)
        warnings.extend(layout_warnings)
        if not layout_ok:
            risk_score += 0.3
        
        # Check 2: Accessibility
        a11y_ok, a11y_warnings = self._check_accessibility(simulated)
        warnings.extend(a11y_warnings)
        if not a11y_ok:
            risk_score += 0.3
        
        # Check 3: Tokens
        tokens_ok, token_warnings = self._check_tokens(simulated)
        warnings.extend(token_warnings)
        if not tokens_ok:
            risk_score += 0.2
        
        # Check 4: Components
        comp_ok, comp_warnings = self._check_components(simulated)
        warnings.extend(comp_warnings)
        if not comp_ok:
            risk_score += 0.2
        
        # Calculate diff
        diff = self._calculate_diff(blueprint, simulated)
        
        # Determine if safe
        safe = layout_ok and tokens_ok and comp_ok
        reason = None if safe else "Safety checks failed"
        
        return SimulationResult(
            safe=safe,
            reason=reason,
            diff=diff,
            risk_score=min(1.0, risk_score),
            warnings=warnings,
            modified_blueprint=simulated
        )
    
    def _check_layout(self, blueprint: Dict[str, Any]) -> tuple[bool, List[str]]:
        """Check for layout conflicts (overlaps, out of bounds)."""
        warnings: List[str] = []
        ok = True
        
        components = blueprint.get("components", [])
        
        # Check each component bounds
        for idx, comp in enumerate(components):
            bbox = comp.get("bbox", [0, 0, 480, 44])
            
            # Check bounds
            if len(bbox) != 4:
                warnings.append(f"Component {idx}: Invalid bbox")
                ok = False
                continue
            
            x1, y1, x2, y2 = bbox
            
            # Check for negative or zero dimensions
            if x2 <= x1 or y2 <= y1:
                warnings.append(f"Component {idx}: Invalid dimensions")
                ok = False
            
            # Check for out of bounds (loose check, allow some overflow)
            if x1 < -100 or y1 < -100 or x2 > 580 or y2 > 1000:
                warnings.append(f"Component {idx}: Out of bounds")
                ok = False
        
        # Check for overlaps (warn but don't fail)
        for i in range(len(components)):
            for j in range(i + 1, len(components)):
                if self._bboxes_overlap(components[i].get("bbox"), components[j].get("bbox")):
                    warnings.append(f"Components {i} and {j} overlap")
        
        return ok, warnings
    
    def _check_accessibility(self, blueprint: Dict[str, Any]) -> tuple[bool, List[str]]:
        """Check accessibility requirements."""
        warnings: List[str] = []
        ok = True
        
        components = blueprint.get("components", [])
        
        for idx, comp in enumerate(components):
            # CTA minimum height
            if comp.get("role") == "cta" or comp.get("type") == "button":
                height = comp.get("visual", {}).get("height", 44)
                if height < 44:
                    warnings.append(f"Component {idx}: CTA height {height} < 44px minimum")
                    ok = False
            
            # Text contrast (simplified)
            color = comp.get("visual", {}).get("color", "#000000")
            bg_color = comp.get("visual", {}).get("bg_color", "#FFFFFF")
            
            if color == bg_color:
                warnings.append(f"Component {idx}: No contrast between text and background")
                ok = False
        
        return ok, warnings
    
    def _check_tokens(self, blueprint: Dict[str, Any]) -> tuple[bool, List[str]]:
        """Check design token validity (warnings only, not hard failures)."""
        warnings: List[str] = []
        ok = True
        
        tokens = blueprint.get("tokens", {})
        
        # Tokens are optional - blueprints might have inline styles instead
        if not tokens:
            warnings.append("No design tokens defined (using inline styles instead)")
            return ok, warnings
        
        # Check for recommended tokens (but don't fail if missing)
        recommended_tokens = ["primary_color", "base_spacing"]
        for token in recommended_tokens:
            if token not in tokens:
                warnings.append(f"Missing recommended token: {token}")
                # Don't set ok=False - optional tokens
        
        # Check base_spacing if it exists
        base_spacing = tokens.get("base_spacing")
        if base_spacing is not None and isinstance(base_spacing, (int, float)):
            if base_spacing % 8 != 0:
                warnings.append(f"base_spacing ({base_spacing}) not multiple of 8 (recommendation)")
                # Don't set ok=False - spacing is a best practice, not requirement
        
        return ok, warnings
    
    def _check_components(self, blueprint: Dict[str, Any]) -> tuple[bool, List[str]]:
        """Check component validity."""
        warnings: List[str] = []
        ok = True
        
        valid_types = ["navbar", "button", "product", "text", "heading", "container", "card", "link", "image"]
        valid_roles = ["nav", "header", "cta", "content", "hero", "footer", None]
        
        components = blueprint.get("components", [])
        
        for idx, comp in enumerate(components):
            comp_type = comp.get("type")
            if comp_type not in valid_types:
                warnings.append(f"Component {idx}: Invalid type '{comp_type}'")
                ok = False
            
            role = comp.get("role")
            if role not in valid_roles:
                warnings.append(f"Component {idx}: Invalid role '{role}'")
                ok = False
            
            # Check required fields
            if "bbox" not in comp:
                warnings.append(f"Component {idx}: Missing bbox")
                ok = False
        
        return ok, warnings
    
    def _bboxes_overlap(self, bbox1: Optional[List], bbox2: Optional[List]) -> bool:
        """Check if two bounding boxes overlap."""
        if not bbox1 or not bbox2:
            return False
        
        x1_1, y1_1, x2_1, y2_1 = bbox1
        x1_2, y1_2, x2_2, y2_2 = bbox2
        
        # No overlap if one is completely to the left/right/above/below the other
        if x2_1 < x1_2 or x2_2 < x1_1:
            return False
        if y2_1 < y1_2 or y2_2 < y1_1:
            return False
        
        return True
    
    def _calculate_diff(self, original: Dict[str, Any], modified: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate what changed between blueprints."""
        diff = {
            "token_changes": {},
            "component_changes": [],
            "components_added": 0,
            "components_removed": 0,
        }
        
        # Token changes
        orig_tokens = original.get("tokens", {})
        mod_tokens = modified.get("tokens", {})
        
        for key in set(list(orig_tokens.keys()) + list(mod_tokens.keys())):
            if orig_tokens.get(key) != mod_tokens.get(key):
                diff["token_changes"][key] = {
                    "old": orig_tokens.get(key),
                    "new": mod_tokens.get(key)
                }
        
        # Component changes
        orig_comps = original.get("components", [])
        mod_comps = modified.get("components", [])
        
        diff["components_removed"] = len(orig_comps) - len(mod_comps)
        diff["components_added"] = len(mod_comps) - len(orig_comps)
        
        # Changed components
        for i, (orig, mod) in enumerate(zip(orig_comps, mod_comps)):
            if orig != mod:
                diff["component_changes"].append({
                    "index": i,
                    "id": mod.get("id"),
                    "changes": self._compare_objects(orig, mod)
                })
        
        return diff
    
    def _compare_objects(self, obj1: Dict, obj2: Dict) -> Dict[str, Any]:
        """Compare two objects and return differences."""
        changes = {}
        
        for key in set(list(obj1.keys()) + list(obj2.keys())):
            if obj1.get(key) != obj2.get(key):
                changes[key] = {
                    "old": obj1.get(key),
                    "new": obj2.get(key)
                }
        
        return changes
