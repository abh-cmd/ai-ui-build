#!/usr/bin/env python
"""
PHASE 10.1 MANUAL TEST & DEMO
Quick validation of all 5 steps
"""

from backend.agent import DesignEditAgent
import json

# Sample blueprint
blueprint = {
    "screen_id": "test",
    "tokens": {
        "colors": {
            "primary": "#0000FF",
            "background": "#FFFFFF",
            "white": "#FFFFFF",
            "black": "#000000",
        }
    },
    "components": [
        {
            "id": "header",
            "type": "header",
            "text": "PANCHAKATTU DOSA",
            "role": "hero",
            "bbox": [95, 41, 337, 30],
            "visual": {
                "color": "#0000FF",
                "bg_color": "#FFFFFF",
                "height": 30,
                "font_weight": "normal"
            }
        },
        {
            "id": "order_button",
            "type": "button",
            "text": "order now!",
            "role": "cta",
            "bbox": [95, 195, 145, 45],
            "visual": {
                "color": "#0000FF",
                "bg_color": "#FFFFFF",
                "height": 45,
                "font_weight": "normal"
            }
        }
    ]
}

# Initialize agent
agent = DesignEditAgent()

print("=" * 80)
print("PHASE 10.1 - AGENTIC AI CORE")
print("Design Edit Agent - Full 5-Step Pipeline Demo")
print("=" * 80)

# Test 1: Color Change
print("\n\n[OK] TEST 1: COLOR CHANGE")
print("-" * 80)
response1 = agent.edit("change order button color to white", blueprint)

for line in response1.reasoning:
    # Encode to ASCII, replacing Unicode characters
    safe_line = line.encode('ascii', errors='replace').decode('ascii')
    print(safe_line)

print(f"\n[OK] SUCCESS: {response1.success}")
print(f"[OK] SAFE: {response1.safe}")
print(f"[OK] CONFIDENCE: {response1.confidence}")
print(f"[OK] SUMMARY: {response1.summary}")

# Test 2: Resize
print("\n\n[OK] TEST 2: RESIZE")
print("-" * 80)
response2 = agent.edit("make order button bigger", blueprint)

for line in response2.reasoning[:30]:  # Show first 30 lines
    safe_line = line.encode('ascii', errors='replace').decode('ascii')
    print(safe_line)

print(f"\n[OK] SUCCESS: {response2.success}")
print(f"[OK] SUMMARY: {response2.summary}")

# Test 3: Text Edit
print("\n\n[OK] TEST 3: TEXT EDIT")
print("-" * 80)
response3 = agent.edit("change button text to Buy Now", blueprint)

for line in response3.reasoning[:30]:  # Show first 30 lines
    safe_line = line.encode('ascii', errors='replace').decode('ascii')
    print(safe_line)

print(f"\n[OK] SUCCESS: {response3.success}")
print(f"[OK] SUMMARY: {response3.summary}")

# Test 4: Verify changes are correct
print("\n\n[OK] TEST 4: VERIFY CHANGES")
print("-" * 80)

button1 = response1.patched_blueprint["components"][1]
print(f"Color change: {button1['visual']['color']} (should be #FFFFFF)")
assert button1['visual']['color'] == '#FFFFFF', "Color not changed!"

button2 = response2.patched_blueprint["components"][1]
print(f"Resize: {button2['visual']['height']}px (should be > 45)")
assert button2['visual']['height'] > 45, "Size not changed!"

button3 = response3.patched_blueprint["components"][1]
print(f"Text change: '{button3['text']}' (should be 'buy now')")
assert button3['text'] == 'buy now', "Text not changed!"

print("\n" + "=" * 80)
print("[OK] ALL TESTS PASSED")
print("[OK] PHASE 10.1 AGENT IS FULLY FUNCTIONAL")
print("=" * 80)
