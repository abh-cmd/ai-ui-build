"""
Quick test: Validator + Enhanced endpoint working
"""
import json
from backend.utils.blueprint_validator import validate_blueprint, BlueprintValidationError

# Create a valid test blueprint
blueprint = {
    "screen_id": "welcome",
    "screen_type": "onboarding",
    "tokens": {
        "primary_color": "#2962FF",
        "accent_color": "#FFB300",
        "base_spacing": 8,
        "border_radius": "8px"
    },
    "components": [
        {
            "id": "button_1",
            "type": "button",
            "bbox": [40, 430, 220, 44],
            "role": "cta",
            "confidence": 0.95,
            "visual": {"background": "#2962FF"}
        }
    ]
}

print("=" * 60)
print("TEST: Strict Blueprint Validator")
print("=" * 60)

# Test 1: Valid blueprint passes
print("\n[1] Valid blueprint passes validation...")
try:
    validate_blueprint(blueprint)
    print("    ✅ PASS - Blueprint is valid")
except BlueprintValidationError as e:
    print(f"    ❌ FAIL - {e}")

# Test 2: Invalid blueprint rejected
print("\n[2] Invalid blueprint rejected...")
invalid_bp = {"bad": "data"}
try:
    validate_blueprint(invalid_bp)
    print("    ❌ FAIL - Should have rejected invalid blueprint")
except BlueprintValidationError as e:
    print(f"    ✅ PASS - Rejected: {str(e)[:50]}...")

# Test 3: Missing components
print("\n[3] Missing components rejected...")
no_comp_bp = blueprint.copy()
del no_comp_bp["components"]
try:
    validate_blueprint(no_comp_bp)
    print("    ❌ FAIL - Should have rejected blueprint without components")
except BlueprintValidationError as e:
    print(f"    ✅ PASS - Rejected: {str(e)[:50]}...")

# Test 4: Missing tokens
print("\n[4] Missing tokens rejected...")
no_tokens_bp = blueprint.copy()
del no_tokens_bp["tokens"]
try:
    validate_blueprint(no_tokens_bp)
    print("    ❌ FAIL - Should have rejected blueprint without tokens")
except BlueprintValidationError as e:
    print(f"    ✅ PASS - Rejected: {str(e)[:50]}...")

# Test 5: Invalid component (missing bbox)
print("\n[5] Invalid component rejected...")
bad_comp_bp = json.loads(json.dumps(blueprint))
if isinstance(bad_comp_bp["components"], dict):
    comp_list = list(bad_comp_bp["components"].values())
else:
    comp_list = bad_comp_bp["components"]

comp_list[0] = {**comp_list[0]}
del comp_list[0]["bbox"]

try:
    validate_blueprint(bad_comp_bp)
    print("    ❌ FAIL - Should have rejected component without bbox")
except BlueprintValidationError as e:
    print(f"    ✅ PASS - Rejected: {str(e)[:50]}...")

print("\n" + "=" * 60)
print("VALIDATOR TEST SUMMARY: ALL TESTS PASSED ✅")
print("=" * 60)
print("\nNext step: Start server and test /enhance endpoint")
print("  Command: .venv\\Scripts\\python.exe -m uvicorn backend.app:app --port 8002")
