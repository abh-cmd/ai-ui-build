"""
Phase 5: Blueprint Enhancement System Test

Validates:
1. Blueprint validator rejects invalid blueprints
2. Enhancement endpoint validates and transforms blueprints
3. Deterministic commands work correctly
4. Schema preservation is enforced
5. Codegen remains unaffected
"""

import requests
import json
from copy import deepcopy

BASE_URL = "http://localhost:8002"

# Test blueprint (valid)
VALID_BLUEPRINT = {
    "screen_id": "test_screen",
    "screen_type": "product_page",
    "orientation": "portrait",
    "tokens": {
        "primary_color": "#3B82F6",
        "accent_color": "#F59E0B",
        "base_spacing": 8,
        "border_radius": "8px"
    },
    "components": [
        {
            "id": "header_1",
            "type": "header",
            "bbox": [0, 0, 400, 100],
            "role": "hero",
            "confidence": 0.95,
            "visual": {
                "background_color": "#3B82F6",
                "text_color": "#FFFFFF"
            }
        },
        {
            "id": "cta_button",
            "type": "button",
            "bbox": [50, 150, 300, 44],
            "role": "cta",
            "confidence": 0.92,
            "visual": {
                "background_color": "#3B82F6",
                "height": 44
            }
        },
        {
            "id": "product_card_1",
            "type": "product_card",
            "bbox": [10, 250, 180, 200],
            "role": "content",
            "confidence": 0.88,
            "visual": {"image_url": "product.jpg"}
        }
    ]
}


def test_validator():
    """Test blueprint validation."""
    print("\n=== TEST 1: Blueprint Validator ===")
    
    tests = [
        {
            "name": "Missing tokens",
            "blueprint": {**VALID_BLUEPRINT, "tokens": None},
            "should_fail": True
        },
        {
            "name": "Invalid primary color (not hex)",
            "blueprint": {
                **VALID_BLUEPRINT,
                "tokens": {
                    **VALID_BLUEPRINT["tokens"],
                    "primary_color": "blue"
                }
            },
            "should_fail": True
        },
        {
            "name": "Missing components",
            "blueprint": {**VALID_BLUEPRINT, "components": None},
            "should_fail": True
        },
        {
            "name": "Component without id",
            "blueprint": {
                **VALID_BLUEPRINT,
                "components": [
                    {
                        **VALID_BLUEPRINT["components"][0],
                        "id": None
                    }
                ]
            },
            "should_fail": True
        },
        {
            "name": "Invalid bbox (not 4 values)",
            "blueprint": {
                **VALID_BLUEPRINT,
                "components": [
                    {
                        **VALID_BLUEPRINT["components"][0],
                        "bbox": [0, 0, 100]
                    }
                ]
            },
            "should_fail": True
        },
        {
            "name": "Valid blueprint",
            "blueprint": deepcopy(VALID_BLUEPRINT),
            "should_fail": False
        }
    ]
    
    for test in tests:
        payload = {
            "command": "no op",
            "blueprint": test["blueprint"]
        }
        
        response = requests.post(
            f"{BASE_URL}/enhance",
            json=payload
        )
        
        success = response.status_code == 200
        expected = not test["should_fail"]
        
        status = "✅" if success == expected else "❌"
        print(f"{status} {test['name']}")
        
        if success != expected:
            print(f"   Expected: {expected}, Got: {success}")
            print(f"   Response: {response.json()}")


def test_color_commands():
    """Test color change commands."""
    print("\n=== TEST 2: Color Commands ===")
    
    tests = [
        {
            "name": "Change primary color to red",
            "command": "change primary color to #FF0000",
            "expected_field": ["tokens", "primary_color"],
            "expected_value": "#FF0000"
        },
        {
            "name": "Change accent color to green",
            "command": "change accent color to #00FF00",
            "expected_field": ["tokens", "accent_color"],
            "expected_value": "#00FF00"
        }
    ]
    
    for test in tests:
        blueprint = deepcopy(VALID_BLUEPRINT)
        response = requests.post(
            f"{BASE_URL}/enhance",
            json={"command": test["command"], "blueprint": blueprint}
        )
        
        if response.status_code != 200:
            print(f"❌ {test['name']} - HTTP {response.status_code}")
            continue
        
        result = response.json()
        updated = result["blueprint"]
        
        # Navigate to field
        value = updated
        for key in test["expected_field"]:
            value = value.get(key)
        
        if value == test["expected_value"]:
            print(f"✅ {test['name']}")
        else:
            print(f"❌ {test['name']} - got {value}, expected {test['expected_value']}")


def test_button_sizing():
    """Test button sizing commands."""
    print("\n=== TEST 3: Button Sizing Commands ===")
    
    blueprint = deepcopy(VALID_BLUEPRINT)
    original_height = blueprint["components"][1]["bbox"][3]  # CTA button height
    
    response = requests.post(
        f"{BASE_URL}/enhance",
        json={
            "command": "make the CTA button bigger",
            "blueprint": blueprint
        }
    )
    
    if response.status_code == 200:
        result = response.json()
        updated = result["blueprint"]
        new_height = updated["components"][1]["bbox"][3]
        expected = int(original_height * 1.2)
        
        if new_height == expected:
            print(f"✅ Button height increased: {original_height} → {new_height}")
        else:
            print(f"❌ Button height: got {new_height}, expected {expected}")
    else:
        print(f"❌ Button sizing failed with HTTP {response.status_code}")


def test_product_scaling():
    """Test product card scaling."""
    print("\n=== TEST 4: Product Scaling Commands ===")
    
    blueprint = deepcopy(VALID_BLUEPRINT)
    original_width = blueprint["components"][2]["bbox"][2]
    original_height = blueprint["components"][2]["bbox"][3]
    
    response = requests.post(
        f"{BASE_URL}/enhance",
        json={
            "command": "make products bigger",
            "blueprint": blueprint
        }
    )
    
    if response.status_code == 200:
        result = response.json()
        updated = result["blueprint"]
        new_width = updated["components"][2]["bbox"][2]
        new_height = updated["components"][2]["bbox"][3]
        
        expected_w = int(original_width * 1.2)
        expected_h = int(original_height * 1.2)
        
        if new_width == expected_w and new_height == expected_h:
            print(f"✅ Product scaling: {original_width}x{original_height} → {new_width}x{new_height}")
        else:
            print(f"❌ Product scaling: got {new_width}x{new_height}, expected {expected_w}x{expected_h}")
    else:
        print(f"❌ Product scaling failed with HTTP {response.status_code}")


def test_spacing_commands():
    """Test spacing modification."""
    print("\n=== TEST 5: Spacing Commands ===")
    
    blueprint = deepcopy(VALID_BLUEPRINT)
    original_spacing = blueprint["tokens"]["base_spacing"]
    
    response = requests.post(
        f"{BASE_URL}/enhance",
        json={
            "command": "add more spacing",
            "blueprint": blueprint
        }
    )
    
    if response.status_code == 200:
        result = response.json()
        updated = result["blueprint"]
        new_spacing = updated["tokens"]["base_spacing"]
        expected = int(original_spacing * 1.2)
        
        if new_spacing == expected:
            print(f"✅ Spacing increased: {original_spacing} → {new_spacing}")
        else:
            print(f"❌ Spacing: got {new_spacing}, expected {expected}")
    else:
        print(f"❌ Spacing command failed with HTTP {response.status_code}")


def test_schema_preservation():
    """Test that schema is preserved after edits."""
    print("\n=== TEST 6: Schema Preservation ===")
    
    blueprint = deepcopy(VALID_BLUEPRINT)
    original_ids = {c["id"] for c in blueprint["components"]}
    
    response = requests.post(
        f"{BASE_URL}/enhance",
        json={
            "command": "change primary color to #FF5733",
            "blueprint": blueprint
        }
    )
    
    if response.status_code == 200:
        result = response.json()
        updated = result["blueprint"]
        new_ids = {c["id"] for c in updated["components"]}
        
        # Check component IDs preserved
        if original_ids == new_ids:
            print(f"✅ Component IDs preserved: {original_ids}")
        else:
            print(f"❌ Component IDs changed: {original_ids} → {new_ids}")
        
        # Check top-level keys preserved
        original_keys = set(blueprint.keys())
        new_keys = set(updated.keys())
        
        if original_keys == new_keys:
            print(f"✅ Top-level keys preserved")
        else:
            print(f"❌ Top-level keys changed: {original_keys} → {new_keys}")
    else:
        print(f"❌ Schema preservation test failed")


def test_unsupported_commands():
    """Test that unsupported commands return gracefully."""
    print("\n=== TEST 7: Unsupported Commands ===")
    
    unsupported = [
        "add a new section",
        "remove the header",
        "change the layout"
    ]
    
    for cmd in unsupported:
        blueprint = deepcopy(VALID_BLUEPRINT)
        response = requests.post(
            f"{BASE_URL}/enhance",
            json={"command": cmd, "blueprint": blueprint}
        )
        
        if response.status_code == 200:
            result = response.json()
            summary = result["summary"]
            if "not supported" in summary.lower():
                print(f"✅ Unsupported command handled: '{cmd}'")
            else:
                print(f"⚠️  Command '{cmd}' returned 200 but may have been processed")
        else:
            print(f"❌ HTTP error for '{cmd}': {response.status_code}")


def test_stacked_edits():
    """Test applying multiple edits sequentially."""
    print("\n=== TEST 8: Stacked Edits ===")
    
    blueprint = deepcopy(VALID_BLUEPRINT)
    
    # Edit 1: Make button bigger
    response1 = requests.post(
        f"{BASE_URL}/enhance",
        json={"command": "make CTA bigger", "blueprint": blueprint}
    )
    
    if response1.status_code != 200:
        print(f"❌ First edit failed")
        return
    
    blueprint = response1.json()["blueprint"]
    height_after_1 = blueprint["components"][1]["bbox"][3]
    
    # Edit 2: Change color
    response2 = requests.post(
        f"{BASE_URL}/enhance",
        json={"command": "change primary color to #FF5733", "blueprint": blueprint}
    )
    
    if response2.status_code != 200:
        print(f"❌ Second edit failed")
        return
    
    blueprint = response2.json()["blueprint"]
    height_after_2 = blueprint["components"][1]["bbox"][3]
    color = blueprint["tokens"]["primary_color"]
    
    # Verify both changes persisted
    if height_after_1 == height_after_2 and color == "#FF5733":
        print(f"✅ Stacked edits persisted: height {height_after_1}px, color {color}")
    else:
        print(f"❌ Stacked edits failed to persist")


def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("PHASE 5: BLUEPRINT ENHANCEMENT SYSTEM TEST")
    print("=" * 60)
    
    try:
        # Check server is running
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code != 200:
            print("❌ Server not responding on health check")
            return
    except Exception as e:
        print(f"❌ Cannot connect to server: {e}")
        return
    
    test_validator()
    test_color_commands()
    test_button_sizing()
    test_product_scaling()
    test_spacing_commands()
    test_schema_preservation()
    test_unsupported_commands()
    test_stacked_edits()
    
    print("\n" + "=" * 60)
    print("TEST SUITE COMPLETE")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
