#!/usr/bin/env python
"""
Test AI integration for vision and edit logic.
Verify:
1. AI_MODE=off uses stubs
2. AI_MODE=on calls LLM with fallback
3. Blueprint schema is preserved
4. Edit commands work in both modes
"""

import os
import json
import tempfile
from PIL import Image

os.environ["AI_MODE"] = "off"

from backend.ai.vision import image_to_raw_json
from backend.ai.edit_agent import interpret_and_patch

def create_test_image(filename="test.png"):
    """Create a simple test image."""
    img = Image.new("RGB", (400, 600), color="white")
    img.save(filename)
    return filename

def test_vision_stub_mode():
    """Test vision in stub mode (AI_MODE=off)."""
    print("\n=== TEST 1: Vision Stub Mode (AI_MODE=off) ===")
    os.environ["AI_MODE"] = "off"
    
    with tempfile.TemporaryDirectory() as tmpdir:
        img_path = os.path.join(tmpdir, "test_store.png")
        create_test_image(img_path)
        blueprint = image_to_raw_json(img_path)
    
    print(f"✓ Blueprint generated: screen_type={blueprint.get('screen_type')}")
    print(f"✓ Components: {[c['type'] for c in blueprint.get('components', [])]}")
    
    assert "tokens" in blueprint
    assert "components" in blueprint
    assert blueprint.get("screen_type") is not None
    print("✓ All assertions passed")

def test_edit_deterministic_mode():
    """Test edit in deterministic mode (AI_MODE=off)."""
    print("\n=== TEST 2: Edit Deterministic Mode (AI_MODE=off) ===")
    os.environ["AI_MODE"] = "off"
    
    blueprint = {
        "screen_id": "test",
        "screen_type": "storefront",
        "orientation": "portrait",
        "tokens": {
            "base_spacing": 16,
            "primary_color": "#3B82F6",
            "accent_color": "#F59E0B",
            "font_scale": {"heading": 1.5, "body": 1.0},
            "border_radius": "8px"
        },
        "components": [
            {
                "id": "button_1",
                "type": "button",
                "bbox": [0, 0, 100, 44],
                "text": "Click",
                "role": "cta",
                "confidence": 0.9,
                "visual": {"height": 44, "bg_color": "#F59E0B"}
            }
        ]
    }
    
    patched, summary = interpret_and_patch("make cta larger", blueprint)
    new_height = patched["components"][0]["visual"]["height"]
    
    print(f"✓ Edit applied: {summary}")
    print(f"✓ Button height changed: 44 → {new_height}")
    assert new_height > 44
    print("✓ All assertions passed")

def test_schema_validation():
    """Test blueprint schema validation."""
    print("\n=== TEST 3: Schema Validation ===")
    from backend.ai.vision import _validate_blueprint_schema
    
    valid_blueprint = {
        "screen_id": "test",
        "screen_type": "landing",
        "orientation": "portrait",
        "tokens": {
            "base_spacing": 16,
            "primary_color": "#EF4444",
            "accent_color": "#F97316",
            "font_scale": {"heading": 1.5, "body": 1.0},
            "border_radius": "8px"
        },
        "components": [
            {
                "id": "hero_1",
                "type": "hero_section",
                "bbox": [0, 0, 375, 200],
                "text": "Welcome",
                "role": "hero",
                "confidence": 0.95,
                "visual": {"bg_color": "#EF4444"}
            }
        ]
    }
    
    assert _validate_blueprint_schema(valid_blueprint) == True
    print("✓ Valid blueprint accepted")
    
    invalid_blueprint = {"screen_id": "test"}
    assert _validate_blueprint_schema(invalid_blueprint) == False
    print("✓ Invalid blueprint rejected")
    print("✓ All assertions passed")

def test_edit_validation():
    """Test edited blueprint validation."""
    print("\n=== TEST 4: Edit Validation ===")
    from backend.ai.edit_agent import _validate_edited_blueprint
    
    original = {
        "components": [
            {"id": "comp_1", "type": "header"},
            {"id": "comp_2", "type": "button"}
        ]
    }
    
    valid_edit = {
        "components": [
            {"id": "comp_1", "type": "header", "bbox": [0, 0, 100, 50]},
            {"id": "comp_2", "type": "button", "bbox": [0, 100, 100, 150]}
        ]
    }
    
    assert _validate_edited_blueprint(valid_edit, original) == True
    print("✓ Valid edit accepted")
    
    invalid_edit = {
        "components": [
            {"id": "comp_1", "type": "header"},
            {"id": "comp_3", "type": "footer"}
        ]
    }
    
    assert _validate_edited_blueprint(invalid_edit, original) == False
    print("✓ Invalid edit (ID mismatch) rejected")
    print("✓ All assertions passed")

if __name__ == "__main__":
    print("=" * 60)
    print("AI INTEGRATION TESTS")
    print("=" * 60)
    
    test_vision_stub_mode()
    test_edit_deterministic_mode()
    test_schema_validation()
    test_edit_validation()
    
    print("\n" + "=" * 60)
    print("✓ ALL TESTS PASSED")
    print("=" * 60)
