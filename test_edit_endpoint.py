#!/usr/bin/env python3
"""Test the /edit endpoint"""
import requests
import json

BASE_URL = "http://localhost:8002"

def test_health():
    """Test /health endpoint"""
    print("Testing /health...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}\n")
    assert response.status_code == 200

def test_edit_make_cta_larger():
    """Test /edit with 'make CTA larger' command"""
    print("Testing /edit - make CTA larger...")
    payload = {
        "command": "make CTA larger",
        "blueprint": {
            "components": [
                {
                    "id": "btn_1",
                    "role": "cta",
                    "bbox": [100, 200, 150, 40],
                    "visual": {"height": 40}
                }
            ],
            "tokens": {"primary_color": "#1967D2"}
        }
    }
    response = requests.post(f"{BASE_URL}/edit", json=payload)
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Patch summary: {result.get('patch_summary')}")
    print(f"New height: {result['patched_blueprint']['components'][0]['visual']['height']}")
    assert response.status_code == 200
    assert result['patched_blueprint']['components'][0]['visual']['height'] == 48
    print("✅ Height correctly increased from 40 to 48 (20%)\n")

def test_edit_change_color():
    """Test /edit with 'change primary color' command"""
    print("Testing /edit - change primary color...")
    payload = {
        "command": "change primary color to #FF5733",
        "blueprint": {
            "components": [],
            "tokens": {"primary_color": "#1967D2"}
        }
    }
    response = requests.post(f"{BASE_URL}/edit", json=payload)
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Patch summary: {result.get('patch_summary')}")
    print(f"New color: {result['patched_blueprint']['tokens']['primary_color']}")
    assert response.status_code == 200
    assert result['patched_blueprint']['tokens']['primary_color'] == "#FF5733"
    print("✅ Color correctly changed to #FF5733\n")

def test_edit_make_products_bigger():
    """Test /edit with 'make products bigger' command"""
    print("Testing /edit - make products bigger...")
    payload = {
        "command": "make products bigger",
        "blueprint": {
            "components": [
                {
                    "id": "product_1",
                    "type": "product_card",
                    "bbox": [0, 0, 200, 250]
                }
            ],
            "tokens": {}
        }
    }
    response = requests.post(f"{BASE_URL}/edit", json=payload)
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Patch summary: {result.get('patch_summary')}")
    new_bbox = result['patched_blueprint']['components'][0]['bbox']
    print(f"Old bbox: [0, 0, 200, 250]")
    print(f"New bbox: {new_bbox}")
    assert response.status_code == 200
    assert new_bbox[2] == 240  # 200 * 1.2
    assert new_bbox[3] == 300  # 250 * 1.2
    print("✅ Product size correctly increased by 20%\n")

if __name__ == "__main__":
    print("=" * 50)
    print("Testing /edit Enhancement Endpoint")
    print("=" * 50 + "\n")
    
    try:
        test_health()
        test_edit_make_cta_larger()
        test_edit_change_color()
        test_edit_make_products_bigger()
        
        print("=" * 50)
        print("✅ All tests passed!")
        print("=" * 50)
    except AssertionError as e:
        print(f"❌ Test failed: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")
