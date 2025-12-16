#!/usr/bin/env python3
"""Test menu blueprint code generation."""
import json
from backend.ai.codegen import generate_code

# Your menu blueprint
blueprint = {
    "screen_id": "menu",
    "screen_type": "information",
    "orientation": "portrait",
    "tokens": {
        "base_spacing": 8,
        "primary_color": "#FFFFFF",
        "accent_color": "#0000FF",
        "font_scale": {
            "heading": 1.2,
            "body": 1
        },
        "border_radius": "4px"
    },
    "components": [
        {
            "id": "header_title",
            "type": "text",
            "bbox": [96, 38, 345, 35],
            "text": "PANCHAKATTU DOSA",
            "role": "header",
            "confidence": 0.95,
            "visual": {
                "font_size": "24px",
                "font_weight": "bold",
                "text_alignment": "center"
            }
        },
        {
            "id": "section_title",
            "type": "text",
            "bbox": [96, 73, 177, 20],
            "text": "Our Specials:",
            "role": "content",
            "confidence": 0.9,
            "visual": {
                "font_size": "16px",
                "font_weight": "medium"
            }
        },
        {
            "id": "menu_item_1",
            "type": "text",
            "bbox": [96, 100, 256, 30],
            "text": "1. Podi idly : 100 ruppees",
            "role": "content",
            "confidence": 0.9,
            "visual": {
                "font_size": "16px"
            }
        },
        {
            "id": "menu_item_2",
            "type": "text",
            "bbox": [96, 140, 278, 30],
            "text": "2. Kaaram Dosa: 150ruppees",
            "role": "content",
            "confidence": 0.9,
            "visual": {
                "font_size": "16px"
            }
        },
        {
            "id": "order_button",
            "type": "button",
            "bbox": [96, 193, 144, 34],
            "text": "order now!",
            "role": "cta",
            "confidence": 0.95,
            "visual": {
                "border": "1px solid #0000FF",
                "text_alignment": "center",
                "height": 44
            }
        },
        {
            "id": "branches_button",
            "type": "button",
            "bbox": [270, 193, 157, 34],
            "text": "our branches",
            "role": "cta",
            "confidence": 0.95,
            "visual": {
                "border": "1px solid #0000FF",
                "text_alignment": "center",
                "height": 44
            }
        }
    ],
    "meta": {
        "source": "llm_analysis"
    }
}

# Generate code
result = generate_code(blueprint)

if result.get("success"):
    print("✅ Code generated successfully!\n")
    files = result.get("files", {})
    
    print(f"📁 Generated {len(files)} files:\n")
    for filename in sorted(files.keys()):
        print(f"  📄 {filename}")
    
    print("\n" + "="*60)
    print("📋 App.jsx:")
    print("="*60)
    print(files.get("src/App.jsx", "NOT FOUND"))
    
    print("\n" + "="*60)
    print("📋 Text.jsx:")
    print("="*60)
    print(files.get("src/components/Text.jsx", "NOT FOUND"))
    
    print("\n" + "="*60)
    print("📋 CTAButton.jsx:")
    print("="*60)
    print(files.get("src/components/CTAButton.jsx", "NOT FOUND"))
else:
    print("❌ Generation failed:")
    print(json.dumps(result, indent=2))
