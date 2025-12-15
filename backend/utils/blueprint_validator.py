"""
Strict Blueprint Validator

Ensures blueprints conform to schema and cannot be modified without validation.
All validation failures result in HTTP 400 - no auto-fixing.
"""

import re
from typing import Tuple, List, Optional


class BlueprintValidationError(Exception):
    """Raised when blueprint validation fails."""
    pass


class BlueprintValidator:
    """Strict blueprint validator with no auto-fixing."""
    
    # Allowed component types
    ALLOWED_TYPES = {
        "header", "title", "subtitle", "description", "text",
        "button", "cta", "image", "product_card", "container",
        "list", "card", "section", "hero", "footer", "divider"
    }
    
    # Required tokens
    REQUIRED_TOKENS = ["primary_color", "accent_color", "base_spacing", "border_radius"]
    
    @staticmethod
    def validate(blueprint: dict) -> None:
        """
        Validate blueprint strictly. Raises BlueprintValidationError on failure.
        
        Args:
            blueprint: Blueprint dictionary
            
        Raises:
            BlueprintValidationError: If validation fails
        """
        if not isinstance(blueprint, dict):
            raise BlueprintValidationError("Blueprint must be a dictionary")
        
        # Check top-level structure
        if "screen_id" not in blueprint or not isinstance(blueprint["screen_id"], str):
            raise BlueprintValidationError("Blueprint must have screen_id (string)")
        
        if "screen_type" not in blueprint or not isinstance(blueprint["screen_type"], str):
            raise BlueprintValidationError("Blueprint must have screen_type (string)")
        
        # Validate tokens
        if "tokens" not in blueprint:
            raise BlueprintValidationError("Blueprint must have tokens object")
        
        BlueprintValidator._validate_tokens(blueprint["tokens"])
        
        # Validate components
        if "components" not in blueprint:
            raise BlueprintValidationError("Blueprint must have components array")
        
        if not isinstance(blueprint["components"], list):
            raise BlueprintValidationError("Components must be an array")
        
        if len(blueprint["components"]) == 0:
            raise BlueprintValidationError("Components array cannot be empty")
        
        BlueprintValidator._validate_components(blueprint["components"])
    
    @staticmethod
    def _validate_tokens(tokens: dict) -> None:
        """Validate tokens object."""
        if not isinstance(tokens, dict):
            raise BlueprintValidationError("Tokens must be a dictionary")
        
        # Check required tokens
        for required in BlueprintValidator.REQUIRED_TOKENS:
            if required not in tokens:
                raise BlueprintValidationError(f"Missing required token: {required}")
        
        # Validate primary_color and accent_color are hex
        for color_key in ["primary_color", "accent_color"]:
            color_value = tokens.get(color_key)
            if not isinstance(color_value, str):
                raise BlueprintValidationError(f"{color_key} must be string")
            if not re.match(r"^#[0-9A-Fa-f]{6}$", color_value):
                raise BlueprintValidationError(f"{color_key} must be valid hex color (#RRGGBB)")
        
        # Validate base_spacing is integer
        if "base_spacing" in tokens:
            if not isinstance(tokens["base_spacing"], int):
                raise BlueprintValidationError("base_spacing must be integer")
            if tokens["base_spacing"] < 0:
                raise BlueprintValidationError("base_spacing cannot be negative")
        
        # Validate border_radius is string
        if "border_radius" in tokens:
            if not isinstance(tokens["border_radius"], str):
                raise BlueprintValidationError("border_radius must be string")
    
    @staticmethod
    def _validate_components(components: List[dict]) -> None:
        """Validate components array."""
        seen_ids = set()
        
        for i, component in enumerate(components):
            if not isinstance(component, dict):
                raise BlueprintValidationError(f"Component {i} must be a dictionary")
            
            # Validate required fields
            if "id" not in component or not isinstance(component["id"], str):
                raise BlueprintValidationError(f"Component {i} must have id (string)")
            
            component_id = component["id"]
            if component_id in seen_ids:
                raise BlueprintValidationError(f"Duplicate component id: {component_id}")
            seen_ids.add(component_id)
            
            if "type" not in component or not isinstance(component["type"], str):
                raise BlueprintValidationError(f"Component {component_id} must have type (string)")
            
            if component["type"] not in BlueprintValidator.ALLOWED_TYPES:
                raise BlueprintValidationError(
                    f"Component {component_id} has invalid type: {component['type']}. "
                    f"Allowed: {', '.join(BlueprintValidator.ALLOWED_TYPES)}"
                )
            
            if "bbox" not in component:
                raise BlueprintValidationError(f"Component {component_id} must have bbox")
            
            BlueprintValidator._validate_bbox(component["bbox"], component_id)
            
            if "role" in component:
                if not isinstance(component["role"], (str, type(None))):
                    raise BlueprintValidationError(f"Component {component_id} role must be string")
            
            if "confidence" not in component:
                raise BlueprintValidationError(f"Component {component_id} must have confidence")
            
            BlueprintValidator._validate_confidence(component["confidence"], component_id)
            
            if "visual" in component and component["visual"] is not None:
                if not isinstance(component["visual"], dict):
                    raise BlueprintValidationError(f"Component {component_id} visual must be dict")
    
    @staticmethod
    def _validate_bbox(bbox: any, component_id: str) -> None:
        """Validate bbox format."""
        if not isinstance(bbox, list):
            raise BlueprintValidationError(f"Component {component_id} bbox must be array")
        
        if len(bbox) != 4:
            raise BlueprintValidationError(f"Component {component_id} bbox must have 4 values [x, y, w, h]")
        
        if not all(isinstance(v, (int, float)) for v in bbox):
            raise BlueprintValidationError(f"Component {component_id} bbox values must be numbers")
        
        # Allow negative coordinates (off-screen), but not negative dimensions
        if bbox[2] <= 0 or bbox[3] <= 0:
            raise BlueprintValidationError(f"Component {component_id} bbox width and height must be positive")
    
    @staticmethod
    def _validate_confidence(confidence: any, component_id: str) -> None:
        """Validate confidence score."""
        if not isinstance(confidence, (int, float)):
            raise BlueprintValidationError(f"Component {component_id} confidence must be number")
        
        if not (0.0 <= confidence <= 1.0):
            raise BlueprintValidationError(f"Component {component_id} confidence must be 0.0-1.0")


def validate_blueprint(blueprint: dict) -> None:
    """
    Validate blueprint. Raises BlueprintValidationError if invalid.
    
    Args:
        blueprint: Blueprint to validate
        
    Raises:
        BlueprintValidationError: If validation fails
    """
    BlueprintValidator.validate(blueprint)
