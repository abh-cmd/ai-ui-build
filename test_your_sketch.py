import requests
import json

# Your extracted blueprint
blueprint = {
  "screen_id": "welcome",
  "screen_type": "onboarding",
  "orientation": "portrait",
  "tokens": {
    "base_spacing": 8,
    "primary_color": "#2962FF",
    "accent_color": "#FFB300",
    "font_scale": {
      "heading": 1.4,
      "body": 1
    },
    "border_radius": "8px"
  },
  "components": [
    {
      "id": "header_1",
      "type": "header",
      "bbox": [40, 15, 220, 30],
      "text": "ABOUT OUR COMPANY",
      "role": "hero",
      "confidence": 0.95,
      "visual": {
        "text_color": "#FFFFFF",
        "background_color": "#2962FF",
        "font_size": "16px"
      }
    },
    {
      "id": "title_1",
      "type": "text",
      "bbox": [40, 60, 240, 70],
      "text": "Welcome to Our Platform",
      "role": "hero",
      "confidence": 0.98,
      "visual": {
        "font_size": "28px",
        "font_weight": "bold"
      }
    },
    {
      "id": "description_1",
      "type": "text",
      "bbox": [40, 140, 240, 110],
      "text": "We help small businesses create beautiful websites without coding. Our tools are simple, fast, and designed for everyone.",
      "role": "content",
      "confidence": 0.96,
      "visual": {
        "font_size": "16px",
        "line_height": "20px"
      }
    },
    {
      "id": "subtitle_1",
      "type": "text",
      "bbox": [40, 260, 180, 30],
      "text": "Why Choose Us?",
      "role": "content",
      "confidence": 0.97,
      "visual": {
        "font_size": "20px",
        "font_weight": "bold"
      }
    },
    {
      "id": "list_1",
      "type": "list",
      "bbox": [40, 300, 240, 120],
      "text": "Easy to use Mobile friendly designs Fast setup No technical skills required",
      "role": "content",
      "confidence": 0.9,
      "visual": {
        "list_style": "bullet",
        "font_size": "16px"
      }
    },
    {
      "id": "button_1",
      "type": "button",
      "bbox": [40, 430, 220, 50],
      "text": "LEARN MORE",
      "role": "cta",
      "confidence": 0.99,
      "visual": {
        "background_color": "#FFB300",
        "text_color": "#000000",
        "border_radius": "8px",
        "font_weight": "bold",
        "height": 44
      }
    }
  ],
  "meta": {
    "source": "llm_analysis"
  }
}

BASE_URL = "http://localhost:8002"

print("=" * 80)
print("TESTING YOUR SKETCH BLUEPRINT")
print("=" * 80)

print("\n📋 EXTRACTED BLUEPRINT SUMMARY:")
print(f"  Screen: {blueprint['screen_id']} ({blueprint['screen_type']})")
print(f"  Primary Color: {blueprint['tokens']['primary_color']}")
print(f"  Accent Color: {blueprint['tokens']['accent_color']}")
print(f"  Components: {len(blueprint['components'])}")
for comp in blueprint['components']:
    print(f"    - {comp['id']}: {comp['type']} ({comp['role']})")

print("\n" + "=" * 80)
print("TEST 1: Make the CTA button larger")
print("=" * 80)

response = requests.post(
    f"{BASE_URL}/edit",
    json={"blueprint": blueprint, "command": "make CTA larger"}
)

if response.status_code == 200:
    result = response.json()
    edited_bp = result["patched_blueprint"]
    button = next(c for c in edited_bp["components"] if c["id"] == "button_1")
    original_button = next(c for c in blueprint["components"] if c["id"] == "button_1")
    
    print(f"✅ Success!")
    print(f"  Summary: {result['patch_summary']}")
    print(f"  Original button bbox: {original_button['bbox']}")
    print(f"  Modified button bbox: {button['bbox']}")
    print(f"  Height changed: {original_button['visual']['height']} → {button['visual'].get('height', 'N/A')}")
else:
    print(f"❌ Error: {response.status_code}")
    print(response.text)

print("\n" + "=" * 80)
print("TEST 2: Change primary color to vibrant red")
print("=" * 80)

response = requests.post(
    f"{BASE_URL}/edit",
    json={"blueprint": blueprint, "command": "change primary color to #FF6B35"}
)

if response.status_code == 200:
    result = response.json()
    edited_bp = result["patched_blueprint"]
    
    print(f"✅ Success!")
    print(f"  Summary: {result['patch_summary']}")
    print(f"  Original primary color: {blueprint['tokens']['primary_color']}")
    print(f"  Modified primary color: {edited_bp['tokens']['primary_color']}")
    print(f"  Header background now: {edited_bp['components'][0]['visual']['background_color']}")
else:
    print(f"❌ Error: {response.status_code}")
    print(response.text)

print("\n" + "=" * 80)
print("TEST 3: Make products bigger (testing fallback)")
print("=" * 80)

response = requests.post(
    f"{BASE_URL}/edit",
    json={"blueprint": blueprint, "command": "make products bigger"}
)

if response.status_code == 200:
    result = response.json()
    print(f"✅ Success!")
    print(f"  Summary: {result['patch_summary']}")
    print(f"  (Note: No products in this sketch, command completed anyway)")
else:
    print(f"❌ Error: {response.status_code}")
    print(response.text)

print("\n" + "=" * 80)
print("✨ ALL TESTS COMPLETED!")
print("=" * 80)
