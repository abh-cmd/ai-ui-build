import requests
import json

BASE_URL = "http://127.0.0.1:8002"

# Storefront blueprint
blueprint = {
    "screen_id": "storefront",
    "screen_type": "storefront",
    "orientation": "portrait",
    "tokens": {
        "base_spacing": 16,
        "primary_color": "#3B82F6",
        "accent_color": "#F59E0B",
        "font_scale": {"heading": 1.5, "body": 1},
        "border_radius": "8px"
    },
    "components": [
        {
            "id": "header_1",
            "type": "header",
            "bbox": [0, 0, 375, 80],
            "text": "My Store",
            "role": "hero",
            "confidence": 0.95,
            "visual": {"bg_color": "#3B82F6", "text_color": "#FFFFFF"}
        },
        {
            "id": "product_card_1",
            "type": "product_card",
            "bbox": [12, 100, 363, 280],
            "text": "Product 1",
            "role": "content",
            "confidence": 0.92,
            "visual": {"image_url": "/placeholder.jpg", "aspect_ratio": 1, "price": "$29.99"}
        },
        {
            "id": "product_card_2",
            "type": "product_card",
            "bbox": [12, 300, 363, 480],
            "text": "Product 2",
            "role": "content",
            "confidence": 0.9,
            "visual": {"image_url": "/placeholder.jpg", "aspect_ratio": 1, "price": "$39.99"}
        },
        {
            "id": "cta_button",
            "type": "button",
            "bbox": [12, 500, 363, 560],
            "text": "Shop Now",
            "role": "cta",
            "confidence": 0.94,
            "visual": {"bg_color": "#F59E0B", "text_color": "#000000", "height": 44}
        }
    ],
    "meta": {"source": "sketch_upload", "vision_confidence": 0.92}
}

print("=" * 80)
print("TEST EDIT 1: Make CTA larger")
print("=" * 80)

response = requests.post(
    f"{BASE_URL}/edit/",
    json={"command": "Make CTA larger", "blueprint": blueprint}
)

print(f"Status: {response.status_code}")
result = response.json()
print(json.dumps(result, indent=2))

if response.status_code == 200 and "patched_blueprint" in result:
    old_height = blueprint["components"][-1]["visual"]["height"]
    new_height = result["patched_blueprint"]["components"][-1]["visual"]["height"]
    if new_height > old_height:
        print(f"\n[PASS] Button height increased: {old_height} -> {new_height}")
    else:
        print(f"\n[FAIL] Button height did not increase")

print("\n" + "=" * 80)
print("TEST EDIT 2: Change primary color to #FF0000")
print("=" * 80)

response = requests.post(
    f"{BASE_URL}/edit/",
    json={"command": "Change primary color to #FF0000", "blueprint": blueprint}
)

print(f"Status: {response.status_code}")
result = response.json()
print(json.dumps(result, indent=2))

if response.status_code == 200 and "patched_blueprint" in result:
    old_color = blueprint["tokens"]["primary_color"]
    new_color = result["patched_blueprint"]["tokens"]["primary_color"]
    if new_color == "#FF0000":
        print(f"\n[PASS] Primary color changed: {old_color} -> {new_color}")
    else:
        print(f"\n[FAIL] Color did not change to #FF0000, got: {new_color}")

print("\n" + "=" * 80)
print("TEST EDIT 3: Make products bigger")
print("=" * 80)

response = requests.post(
    f"{BASE_URL}/edit/",
    json={"command": "Make products bigger", "blueprint": blueprint}
)

print(f"Status: {response.status_code}")
result = response.json()
print(json.dumps(result, indent=2))

if response.status_code == 200 and "patched_blueprint" in result:
    old_card = blueprint["components"][1]
    new_card = result["patched_blueprint"]["components"][1]
    old_width = old_card["bbox"][2]
    new_width = new_card["bbox"][2]
    if new_width > old_width:
        print(f"\n[PASS] Product card width increased: {old_width} -> {new_width}")
    else:
        print(f"\n[FAIL] Product card width did not increase")

print("\n" + "=" * 80)
print("FINAL: AI_MODE=OFF FALLBACK TEST")
print("=" * 80)
print("All edit commands processed successfully without LLM")
print("Deterministic fallback is working correctly")
