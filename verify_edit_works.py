#!/usr/bin/env python3
"""
Quick verification that /edit endpoint works
Shows before and after blueprint changes
"""
import requests

BASE_URL = "http://localhost:8002"

def test_command(name, blueprint, command):
    """Test a command and show before/after"""
    print(f"\n{'='*60}")
    print(f"TEST: {name}")
    print(f"COMMAND: {command}")
    print(f"{'='*60}")
    
    print("\n📋 BEFORE:")
    if "components" in blueprint:
        for c in blueprint["components"]:
            if "visual" in c:
                print(f"  {c.get('id')}: height={c['visual'].get('height')}")
            elif "bbox" in c:
                print(f"  {c.get('id')}: bbox={c.get('bbox')}")
    
    if "tokens" in blueprint:
        print(f"  tokens: {blueprint['tokens']}")
    
    # Send to /edit
    payload = {"command": command, "blueprint": blueprint}
    response = requests.post(f"{BASE_URL}/edit", json=payload)
    
    if response.status_code != 200:
        print(f"\n❌ FAILED: {response.status_code}")
        return False
    
    result = response.json()
    updated = result["patched_blueprint"]
    summary = result["patch_summary"]
    
    print(f"\n✅ AFTER ({summary}):")
    if "components" in updated:
        for c in updated["components"]:
            if "visual" in c:
                print(f"  {c.get('id')}: height={c['visual'].get('height')}")
            elif "bbox" in c:
                print(f"  {c.get('id')}: bbox={c.get('bbox')}")
    
    if "tokens" in updated:
        print(f"  tokens: {updated['tokens']}")
    
    return blueprint != updated

if __name__ == "__main__":
    print("\n╔══════════════════════════════════════════════════════════╗")
    print("║        VERIFY /edit ENDPOINT WORKS                      ║")
    print("╚══════════════════════════════════════════════════════════╝")
    
    try:
        health = requests.get(f"{BASE_URL}/health", timeout=2)
        print(f"\n🔗 Server: ✅ Running")
    except:
        print(f"\n🔗 Server: ❌ Not responding")
        exit(1)
    
    # Test 1
    r1 = test_command(
        "Make CTA Bigger",
        {"components": [{"id": "btn", "role": "cta", "visual": {"height": 40}}], "tokens": {}},
        "make CTA larger"
    )
    
    # Test 2
    r2 = test_command(
        "Change Color",
        {"components": [], "tokens": {"primary_color": "#0066FF"}},
        "change primary color to #FF5733"
    )
    
    # Test 3
    r3 = test_command(
        "Make Products Bigger",
        {"components": [{"id": "p1", "type": "product_card", "bbox": [0, 0, 100, 150]}], "tokens": {}},
        "make products bigger"
    )
    
    # Summary
    results = [("Make CTA Bigger", r1), ("Change Color", r2), ("Make Products Bigger", r3)]
    passed = sum(1 for _, r in results if r)
    
    print(f"\n{'='*60}")
    print(f"RESULTS: {passed}/3 tests passed")
    print(f"{'='*60}")
    
    for name, result in results:
        print(f"{'✅' if result else '❌'} {name}")
    
    if passed == 3:
        print("\n🎉 SUCCESS! The /edit endpoint is working!")
        print("\nHow to test with real designs:")
        print("1. Upload a sketch via POST /upload")
        print("2. Gemini extracts blueprint from the sketch")
        print("3. Send blueprint + command to POST /edit")
        print("4. Get back modified blueprint")
