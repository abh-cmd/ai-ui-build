def improve_blueprint(raw_json: dict) -> tuple:
    """
    Apply deterministic rules to improve blueprint spacing, alignment, tokens.
    
    Rules:
    1. Round numeric spacing to nearest multiple of 8 (base = 8px)
    2. Ensure CTA/button minimum height 44px
    3. Normalize product card aspect_ratio to 1.0
    
    Args:
        raw_json: Raw blueprint dict from vision module
    
    Returns:
        tuple: (improved_blueprint, change_log: List[str])
    """
    import copy

    # Basic validation
    if not isinstance(raw_json, dict) or "tokens" not in raw_json or "components" not in raw_json:
        raise ValueError("Invalid blueprint: missing tokens or components")

    improved = copy.deepcopy(raw_json)
    changelog = []
    
    # Rule 1: Snap spacing values to base 8
    base_spacing = 8
    if "tokens" in improved and "base_spacing" in improved["tokens"]:
        old_spacing = improved["tokens"]["base_spacing"]
        new_spacing = round(old_spacing / base_spacing) * base_spacing
        if old_spacing != new_spacing:
            improved["tokens"]["base_spacing"] = new_spacing
            changelog.append(f"Snapped base_spacing {old_spacing} → {new_spacing}")
    
    # Rule 2: Ensure CTA minimum height 44px
    if "components" in improved:
        for comp in improved["components"]:
            if comp.get("role") == "cta" and "visual" in comp:
                old_height = comp["visual"].get("height", 40)
                new_height = max(44, old_height)
                if old_height != new_height:
                    comp["visual"]["height"] = new_height
                    changelog.append(f"CTA height {old_height} → {new_height}")
            
            # Rule 3: Normalize product card aspect ratio to 1.0
            if comp.get("type") == "product_card" and "visual" in comp:
                old_ratio = comp["visual"].get("aspect_ratio", 1.0)
                new_ratio = 1.0
                if old_ratio != new_ratio:
                    comp["visual"]["aspect_ratio"] = new_ratio
                    changelog.append(f"Product aspect_ratio {old_ratio} → {new_ratio}")
    
    return improved, changelog
