#!/usr/bin/env python3
"""CLI script to validate blueprint JSON locally.

Usage:
    python tools/check_blueprint.py PATH_TO_BLUEPRINT_JSON

Checks:
    - base_spacing is multiple of 8
    - all CTA heights >= 44
    - all product aspect_ratios == 1.0

Exit codes:
    0 = All validations passed (OK)
    1 = Validation failed (error printed)
"""
import json
import sys


def main():
    if len(sys.argv) != 2:
        print("Usage: python tools/check_blueprint.py <blueprint.json>")
        sys.exit(1)
    
    filepath = sys.argv[1]
    
    try:
        with open(filepath, "r") as f:
            blueprint = json.load(f)
    except FileNotFoundError:
        print(f"ERROR: File not found: {filepath}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON: {e}")
        sys.exit(1)
    
    # Extract tokens and components
    tokens = blueprint.get("tokens", {})
    components = blueprint.get("components", [])
    
    # Check base_spacing
    base_spacing = tokens.get("base_spacing")
    print(f"base_spacing: {base_spacing}")
    if base_spacing is None or base_spacing % 8 != 0:
        print(f"ERROR: base_spacing must be multiple of 8, got {base_spacing}")
        sys.exit(1)
    
    # Check CTA heights
    cta_heights = []
    for comp in components:
        if comp.get("role") == "cta":
            visual = comp.get("visual", {})
            height = visual.get("height")
            if height is not None:
                cta_heights.append(height)
            if height is None or height < 44:
                print(f"ERROR: CTA {comp.get('id')} height must be >= 44, got {height}")
                sys.exit(1)
    print(f"cta_heights: {cta_heights}")
    
    # Check product aspect_ratios
    product_aspect_ratios = []
    for comp in components:
        if comp.get("type") == "product_card":
            visual = comp.get("visual", {})
            aspect_ratio = visual.get("aspect_ratio")
            if aspect_ratio is not None:
                product_aspect_ratios.append(aspect_ratio)
            if aspect_ratio is None or abs(aspect_ratio - 1.0) > 1e-6:
                print(f"ERROR: Product {comp.get('id')} aspect_ratio must be 1.0, got {aspect_ratio}")
                sys.exit(1)
    print(f"product_aspect_ratios: {product_aspect_ratios}")
    
    print("OK")
    sys.exit(0)


if __name__ == "__main__":
    main()
