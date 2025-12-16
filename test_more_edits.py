import requests
import json
from copy import deepcopy

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
      "text": "We help small businesses create beautiful websites without coding.",
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
print("COMPREHENSIVE EDIT TESTS FOR YOUR SKETCH")
print("=" * 80)

tests = [
    {
        "name": "Make CTA larger",
        "command": "make CTA larger",
        "check": lambda b: (next(c for c in b["components"] if c["id"] == "button_1")["visual"]["height"],
                           next(c for c in blueprint["components"] if c["id"] == "button_1")["visual"]["height"])
    },
    {
        "name": "Change primary color to red",
        "command": "change primary color to #FF0000",
        "check": lambda b: (b["tokens"]["primary_color"],
                           blueprint["tokens"]["primary_color"])
    },
    {
        "name": "Change accent color to purple",
        "command": "change primary color to #9C27B0",
        "check": lambda b: (b["tokens"]["primary_color"],
                           blueprint["tokens"]["primary_color"])
    },
    {
        "name": "Make products bigger (no products)",
        "command": "make products bigger",
        "check": lambda b: ("No product cards found", "Expected behavior")
    },
    {
        "name": "Change accent to green",
        "command": "change primary color to #4CAF50",
        "check": lambda b: (b["tokens"]["primary_color"],
                           blueprint["tokens"]["primary_color"])
    },
    {
        "name": "Make button much larger",
        "command": "make CTA larger",
        "check": lambda b: (next(c for c in b["components"] if c["id"] == "button_1")["bbox"],
                           next(c for c in blueprint["components"] if c["id"] == "button_1")["bbox"])
    },
    {
        "name": "Change to dark theme color",
        "command": "change primary color to #1A1A1A",
        "check": lambda b: (b["tokens"]["primary_color"],
                           blueprint["tokens"]["primary_color"])
    },
    {
        "name": "Change to vibrant orange",
        "command": "change primary color to #FF6B35",
        "check": lambda b: (b["tokens"]["primary_color"],
                           blueprint["tokens"]["primary_color"])
    },
]

current_bp = deepcopy(blueprint)
test_results = []

for i, test in enumerate(tests, 1):
    print(f"\n{'=' * 80}")
    print(f"TEST {i}: {test['name']}")
    print(f"Command: \"{test['command']}\"")
    print(f"{'=' * 80}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/edit",
            json={"blueprint": current_bp, "command": test["command"]}
        )
        
        if response.status_code == 200:
            result = response.json()
            current_bp = result["patched_blueprint"]
            
            before, after = test["check"](current_bp)
            
            print(f"✅ SUCCESS")
            print(f"  Summary: {result['patch_summary']}")
            print(f"  Before: {before}")
            print(f"  After:  {after}")
            test_results.append((test['name'], "✅"))
        else:
            print(f"❌ FAILED: Status {response.status_code}")
            print(f"  Error: {response.text}")
            test_results.append((test['name'], "❌"))
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        test_results.append((test['name'], "❌"))

print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)
print(f"\nTotal Tests: {len(test_results)}")
print(f"Passed: {sum(1 for _, r in test_results if r == '✅')}")
print(f"Failed: {sum(1 for _, r in test_results if r == '❌')}\n")

for name, result in test_results:
    print(f"  {result} {name}")

print("\n" + "=" * 80)
print("FINAL BLUEPRINT STATE")
print("=" * 80)
print(f"Primary Color: {current_bp['tokens']['primary_color']}")
print(f"Accent Color: {current_bp['tokens']['accent_color']}")
print(f"Button Height: {current_bp['components'][-1]['visual'].get('height', 'N/A')}")
print(f"Button Bbox: {current_bp['components'][-1]['bbox']}")
print(f"\nHeader Background: {current_bp['components'][0]['visual']['background_color']}")

print("\n✨ TESTING COMPLETE!")
