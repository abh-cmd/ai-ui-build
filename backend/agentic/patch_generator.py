"""
PATCH GENERATOR: Generate JSON patches from intents.

Never mutates blueprint directly. Only generates patches (JSON operations).
Whitelists allowed fields to prevent injection attacks.
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import copy


@dataclass
class JSONPatch:
    """RFC 6902 JSON Patch operation."""
    op: str  # "add", "remove", "replace"
    path: str  # JSON path (e.g., "/components/0/visual/height")
    value: Optional[Any] = None  # New value for "add" or "replace"


class PatchGenerator:
    """Generate deterministic JSON patches from intents."""
    
    # Whitelisted fields (SECURITY: prevent injection)
    ALLOWED_COMPONENT_FIELDS = {
        "text", "visual", "bbox", "type", "role", "hidden",
        "color", "bg_color", "height", "width", "padding", "margin",
        "border_radius", "font_weight", "font_style", "opacity"
    }
    
    ALLOWED_TOKEN_FIELDS = {
        "primary_color", "accent_color", "base_spacing", "border_radius",
        "font_scale", "shadow", "opacity", "contrast"
    }
    
    def generate(self, intent: Any, blueprint: Dict[str, Any]) -> List[JSONPatch]:
        """
        Generate patches for a single intent.
        
        Args:
            intent: Intent object from intent_graph
            blueprint: Current blueprint (not modified)
        
        Returns:
            List of JSONPatch operations (can be applied in order)
        """
        patches: List[JSONPatch] = []
        
        from .intent_graph import IntentType
        
        if intent.type == IntentType.RESIZE:
            patches.extend(self._generate_resize_patches(intent, blueprint))
        elif intent.type == IntentType.COLOR:
            patches.extend(self._generate_color_patches(intent, blueprint))
        elif intent.type == IntentType.ALIGN:
            patches.extend(self._generate_align_patches(intent, blueprint))
        elif intent.type == IntentType.TEXT:
            patches.extend(self._generate_text_patches(intent, blueprint))
        elif intent.type == IntentType.STYLE:
            patches.extend(self._generate_style_patches(intent, blueprint))
        elif intent.type == IntentType.POSITION:
            patches.extend(self._generate_position_patches(intent, blueprint))
        elif intent.type == IntentType.VISIBILITY:
            patches.extend(self._generate_visibility_patches(intent, blueprint))
        elif intent.type == IntentType.DELETE:
            patches.extend(self._generate_delete_patches(intent, blueprint))
        elif intent.type == IntentType.CREATE:
            patches.extend(self._generate_create_patches(intent, blueprint))
        
        return patches
    
    def _generate_resize_patches(self, intent: Any, blueprint: Dict[str, Any]) -> List[JSONPatch]:
        """Generate patches for resize intent."""
        patches: List[JSONPatch] = []
        
        if not intent.target:
            return patches
        
        # Find components matching target
        for idx, comp in enumerate(blueprint.get("components", [])):
            if comp.get("type") == intent.target:
                # Calculate new height based on value
                current_height = comp.get("visual", {}).get("height", 44)
                
                if intent.value == "larger":
                    new_height = int(current_height * 1.5)
                elif intent.value == "large":
                    new_height = int(current_height * 1.2)
                elif intent.value == "small":
                    new_height = int(current_height * 0.8)
                elif intent.value == "tiny":
                    new_height = int(current_height * 0.6)
                elif intent.value == "2x":
                    new_height = current_height * 2
                else:
                    continue
                
                # Enforce minimum height for CTAs
                if comp.get("type") == "button" or comp.get("role") == "cta":
                    new_height = max(new_height, 44)
                
                # Generate patch
                path = f"/components/{idx}/visual/height"
                patches.append(JSONPatch(op="replace", path=path, value=new_height))
        
        return patches
    
    def _generate_color_patches(self, intent: Any, blueprint: Dict[str, Any]) -> List[JSONPatch]:
        """Generate patches for color intent."""
        patches: List[JSONPatch] = []
        
        color_map = {
            "red": "#E63946",
            "blue": "#457B9D",
            "green": "#2A9D8F",
            "yellow": "#F4A261",
            "purple": "#7209B7",
            "orange": "#FF6B35",
            "black": "#000000",
            "white": "#FFFFFF",
            "primary": "#E63946",
            "accent": "#F1FAEE",
            "dark": "#1D3557",
            "light": "#F1FAEE",
        }
        
        hex_color = color_map.get(intent.value)
        if not hex_color:
            return patches
        
        if intent.target:
            # Apply to specific component type
            for idx, comp in enumerate(blueprint.get("components", [])):
                if comp.get("type") == intent.target:
                    if intent.value in ["primary", "accent"]:
                        # Primary/accent applies to background
                        path = f"/components/{idx}/visual/bg_color"
                    else:
                        # Other colors apply to text
                        path = f"/components/{idx}/visual/color"
                    
                    patches.append(JSONPatch(op="replace", path=path, value=hex_color))
        else:
            # Apply to tokens (primary token colors) OR first button (generic colors)
            if intent.value in ["primary", "accent"]:
                # Token-level colors (e.g., "Make it primary")
                token_key = f"{intent.value}_color"
                path = f"/tokens/{token_key}"
                patches.append(JSONPatch(op="replace", path=path, value=hex_color))
            else:
                # Generic colors (e.g., "Make it red") - apply to first button
                buttons = [c for c in blueprint.get("components", []) if c.get("type") == "button"]
                if buttons:
                    # Apply to first button's text color
                    idx = blueprint.get("components", []).index(buttons[0])
                    path = f"/components/{idx}/visual/color"
                    patches.append(JSONPatch(op="replace", path=path, value=hex_color))
        
        return patches
    
    def _generate_align_patches(self, intent: Any, blueprint: Dict[str, Any]) -> List[JSONPatch]:
        """Generate patches for align intent."""
        patches: List[JSONPatch] = []
        
        # Alignment affects bbox positioning
        if intent.value and intent.target:
            for idx, comp in enumerate(blueprint.get("components", [])):
                if comp.get("type") == intent.target:
                    bbox = comp.get("bbox", [0, 0, 480, 44])
                    
                    if intent.value == "center":
                        # Center horizontally: x = (480 - width) / 2
                        width = bbox[2] - bbox[0]
                        new_x = (480 - width) // 2
                        new_bbox = [new_x, bbox[1], new_x + width, bbox[3]]
                    elif intent.value == "left":
                        width = bbox[2] - bbox[0]
                        new_bbox = [10, bbox[1], 10 + width, bbox[3]]
                    elif intent.value == "right":
                        width = bbox[2] - bbox[0]
                        new_bbox = [470 - width, bbox[1], 470, bbox[3]]
                    else:
                        continue
                    
                    path = f"/components/{idx}/bbox"
                    patches.append(JSONPatch(op="replace", path=path, value=new_bbox))
        
        return patches
    
    def _generate_text_patches(self, intent: Any, blueprint: Dict[str, Any]) -> List[JSONPatch]:
        """Generate patches for text intent."""
        patches: List[JSONPatch] = []
        
        if intent.value and intent.target:
            for idx, comp in enumerate(blueprint.get("components", [])):
                if comp.get("type") == intent.target:
                    path = f"/components/{idx}/text"
                    patches.append(JSONPatch(op="replace", path=path, value=intent.value))
        
        return patches
    
    def _generate_style_patches(self, intent: Any, blueprint: Dict[str, Any]) -> List[JSONPatch]:
        """Generate patches for style intent."""
        patches: List[JSONPatch] = []
        
        style_map = {
            "bold": {"font_weight": "bold"},
            "italic": {"font_style": "italic"},
            "shadow": {"box_shadow": "0 4px 8px rgba(0,0,0,0.2)"},
            "rounded": {"border_radius": "12px"},
        }
        
        if intent.value not in style_map:
            return patches
        
        style_props = style_map[intent.value]
        
        if intent.target:
            for idx, comp in enumerate(blueprint.get("components", [])):
                if comp.get("type") == intent.target:
                    for prop, val in style_props.items():
                        path = f"/components/{idx}/visual/{prop}"
                        patches.append(JSONPatch(op="replace", path=path, value=val))
        
        return patches
    
    def _generate_position_patches(self, intent: Any, blueprint: Dict[str, Any]) -> List[JSONPatch]:
        """Generate patches for position intent."""
        # Position changes are complex - would need specific values
        return []
    
    def _generate_visibility_patches(self, intent: Any, blueprint: Dict[str, Any]) -> List[JSONPatch]:
        """Generate patches for visibility intent."""
        patches: List[JSONPatch] = []
        
        hidden = intent.value == "hide" or intent.type.value == "hide"
        
        if intent.target:
            for idx, comp in enumerate(blueprint.get("components", [])):
                if comp.get("type") == intent.target:
                    path = f"/components/{idx}/hidden"
                    patches.append(JSONPatch(op="replace", path=path, value=hidden))
        
        return patches
    
    def _generate_delete_patches(self, intent: Any, blueprint: Dict[str, Any]) -> List[JSONPatch]:
        """Generate patches for delete intent."""
        patches: List[JSONPatch] = []
        
        # Delete removes entire component
        if intent.target:
            indices_to_delete = []
            for idx, comp in enumerate(blueprint.get("components", [])):
                if comp.get("type") == intent.target:
                    indices_to_delete.append(idx)
            
            # Delete in reverse order to maintain indices
            for idx in sorted(indices_to_delete, reverse=True):
                path = f"/components/{idx}"
                patches.append(JSONPatch(op="remove", path=path))
        
        return patches
    
    def _generate_create_patches(self, intent: Any, blueprint: Dict[str, Any]) -> List[JSONPatch]:
        """Generate patches for create intent."""
        patches: List[JSONPatch] = []
        
        # Create new component
        new_component = {
            "id": f"new_{intent.target}",
            "type": intent.target or "container",
            "text": intent.value or f"New {intent.target or 'component'}",
            "bbox": [10, 10, 200, 44],
            "role": "content",
            "visual": {
                "color": "#000000",
                "bg_color": "#FFFFFF",
                "height": 44
            }
        }
        
        # Add to components array
        path = "/components/-"  # -1 means append
        patches.append(JSONPatch(op="add", path=path, value=new_component))
        
        return patches
    
    def apply_patches(self, blueprint: Dict[str, Any], patches: List[JSONPatch]) -> Dict[str, Any]:
        """
        Apply patches to blueprint (creates new copy, doesn't mutate original).
        
        Args:
            blueprint: Original blueprint (not modified)
            patches: List of JSONPatch operations
        
        Returns:
            New blueprint with patches applied
        """
        result = copy.deepcopy(blueprint)
        
        for patch in patches:
            try:
                if patch.op == "replace":
                    result = self._apply_replace(result, patch)
                elif patch.op == "add":
                    result = self._apply_add(result, patch)
                elif patch.op == "remove":
                    result = self._apply_remove(result, patch)
            except Exception:
                # Invalid patch, skip it
                continue
        
        return result
    
    def _apply_replace(self, obj: Dict, patch: JSONPatch) -> Dict:
        """Apply replace operation."""
        keys = patch.path.strip("/").split("/")
        current = obj
        
        for key in keys[:-1]:
            if key.isdigit():
                current = current[int(key)]
            else:
                current = current[key]
        
        final_key = keys[-1]
        if final_key.isdigit():
            current[int(final_key)] = patch.value
        else:
            current[final_key] = patch.value
        
        return obj
    
    def _apply_add(self, obj: Dict, patch: JSONPatch) -> Dict:
        """Apply add operation."""
        keys = patch.path.strip("/").split("/")
        current = obj
        
        for key in keys[:-1]:
            if key.isdigit():
                current = current[int(key)]
            else:
                current = current[key]
        
        final_key = keys[-1]
        if final_key == "-":
            current.append(patch.value)
        elif final_key.isdigit():
            current.insert(int(final_key), patch.value)
        else:
            current[final_key] = patch.value
        
        return obj
    
    def _apply_remove(self, obj: Dict, patch: JSONPatch) -> Dict:
        """Apply remove operation."""
        keys = patch.path.strip("/").split("/")
        current = obj
        
        for key in keys[:-1]:
            if key.isdigit():
                current = current[int(key)]
            else:
                current = current[key]
        
        final_key = keys[-1]
        if final_key.isdigit():
            del current[int(final_key)]
        else:
            del current[final_key]
        
        return obj
