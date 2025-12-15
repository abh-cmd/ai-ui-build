"""
Strict Blueprint Validator
- Rejects invalid blueprints
- No auto-fix
- Returns specific error messages
"""

def validate_blueprint(blueprint):
    """
    Validate blueprint structure. Raises ValueError if invalid.
    
    Returns: None (validation passed) or raises ValueError
    """
    
    if not isinstance(blueprint, dict):
        raise ValueError("Blueprint must be a dictionary")
    
    if not blueprint:
        raise ValueError("Blueprint cannot be empty")
    
    # Check tokens exist
    if "tokens" not in blueprint:
        raise ValueError("Blueprint must have 'tokens' object")
    
    tokens = blueprint["tokens"]
    if not isinstance(tokens, dict):
        raise ValueError("tokens must be an object")
    
    # Check components exist
    if "components" not in blueprint:
        raise ValueError("Blueprint must have 'components' array")
    
    components = blueprint["components"]
    if not isinstance(components, (list, dict)):
        raise ValueError("components must be an array or object")
    
    # Convert dict components to list for validation
    if isinstance(components, dict):
        comp_list = list(components.values())
    else:
        comp_list = components
    
    if not comp_list:
        raise ValueError("components cannot be empty")
    
    # Validate each component
    for i, comp in enumerate(comp_list):
        if not isinstance(comp, dict):
            raise ValueError(f"component {i} must be an object")
        
        # Required fields
        if "id" not in comp:
            raise ValueError(f"component {i} missing 'id'")
        if not isinstance(comp["id"], str):
            raise ValueError(f"component {i} 'id' must be string")
        
        if "type" not in comp:
            raise ValueError(f"component {i} missing 'type'")
        if not isinstance(comp["type"], str):
            raise ValueError(f"component {i} 'type' must be string")
        
        if "bbox" not in comp:
            raise ValueError(f"component {i} missing 'bbox'")
        bbox = comp["bbox"]
        if not isinstance(bbox, (list, tuple)) or len(bbox) != 4:
            raise ValueError(f"component {i} 'bbox' must be [x, y, width, height]")
        if not all(isinstance(v, (int, float)) for v in bbox):
            raise ValueError(f"component {i} 'bbox' must contain numbers")
        
        if "role" not in comp:
            raise ValueError(f"component {i} missing 'role'")
        
        if "confidence" not in comp:
            raise ValueError(f"component {i} missing 'confidence'")
        
        if "visual" not in comp:
            raise ValueError(f"component {i} missing 'visual'")
        if not isinstance(comp["visual"], dict):
            raise ValueError(f"component {i} 'visual' must be object")


def validate_enhanced_blueprint(blueprint):
    """Validate blueprint after enhancement"""
    validate_blueprint(blueprint)
