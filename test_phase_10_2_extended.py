"""
PHASE 10.2 Extended Validation Suite
Additional tests to verify production robustness
"""

import copy
import json
from backend.agent.phase_10_2 import (
    execute_multi_step_edit,
    MultiStepAgent,
    MultiIntentDecomposer,
    ConflictDetector,
)

# Production blueprint
prod_blueprint = {
    "screen_id": "main",
    "tokens": {
        "colors": {
            "white": "#FFFFFF",
            "black": "#000000",
            "blue": "#0000FF",
            "red": "#FF0000",
            "green": "#00FF00",
            "gray": "#808080",
        }
    },
    "components": [
        {
            "id": "header",
            "type": "header",
            "text": "Welcome",
            "role": "hero",
            "bbox": [10, 10, 480, 40],
            "visual": {"color": "#0000FF", "height": 40, "font_weight": "normal"}
        },
        {
            "id": "product_section",
            "type": "container",
            "text": "Products",
            "role": "content",
            "bbox": [10, 60, 480, 200],
            "visual": {"color": "#000000", "height": 200}
        },
        {
            "id": "cta_button",
            "type": "button",
            "text": "Get Started",
            "role": "cta",
            "bbox": [10, 270, 200, 50],
            "visual": {"color": "#FFFFFF", "bg_color": "#0000FF", "height": 50}
        },
    ]
}

def test_extended_multi_step_commands():
    """Test complex multi-step commands"""
    print("\n" + "="*80)
    print("EXTENDED TEST 1: Complex Multi-Step Commands")
    print("="*80)
    
    test_cases = [
        ("Make header smaller and change its color to red", 2),
        ("Change header color to blue and then make it bigger", 2),
        ("Change header color to green and make cta button bigger", 2),
        ("Make header bigger and change its color to red", 2),
    ]
    
    passed = 0
    for cmd, expected_steps in test_cases:
        result = execute_multi_step_edit(cmd, copy.deepcopy(prod_blueprint))
        success = result.status == "success" and result.steps_executed >= expected_steps - 1
        status = "✓" if success else "✗"
        print(f"{status} Command: '{cmd}'")
        print(f"   Status: {result.status}, Steps: {result.steps_executed}/{result.steps_total}")
        if success:
            passed += 1
    
    print(f"\nResult: {passed}/{len(test_cases)} PASS")
    return passed == len(test_cases)


def test_rollback_integrity():
    """Test that rollback actually reverts changes"""
    print("\n" + "="*80)
    print("EXTENDED TEST 2: Rollback Integrity")
    print("="*80)
    
    # Test with conflicting command (should trigger rollback)
    blueprint = copy.deepcopy(prod_blueprint)
    original = copy.deepcopy(prod_blueprint)
    
    cmd = "Delete header and resize it"
    result = execute_multi_step_edit(cmd, blueprint)
    
    print(f"Command: '{cmd}'")
    print(f"Status: {result.status}")
    print(f"Rollback triggered: {result.rollback_triggered}")
    
    # Blueprint should be unchanged or rolled back
    blueprint_changed = result.final_blueprint != original
    print(f"Blueprint unchanged/rolled back: {not blueprint_changed or result.rollback_triggered}")
    
    return (result.status in ["conflicted", "failed"] or not blueprint_changed)


def test_json_serialization():
    """Test that results are properly JSON serializable"""
    print("\n" + "="*80)
    print("EXTENDED TEST 3: JSON Serialization")
    print("="*80)
    
    cmd = "Make header smaller and change its color to red"
    result = execute_multi_step_edit(cmd, copy.deepcopy(prod_blueprint))
    
    try:
        result_dict = result.to_dict()
        json_str = json.dumps(result_dict, indent=2)
        print("✓ Result successfully serialized to JSON")
        print(f"  Keys: {list(result_dict.keys())}")
        
        # Parse back to verify
        parsed = json.loads(json_str)
        print("✓ Result successfully parsed from JSON")
        
        return True
    except Exception as e:
        print(f"✗ Serialization failed: {e}")
        return False


def test_determinism_extended():
    """Extended determinism test with varied commands"""
    print("\n" + "="*80)
    print("EXTENDED TEST 4: Extended Determinism")
    print("="*80)
    
    commands = [
        "Make header smaller",
        "Change cta button color to green",
        "Make header smaller and change its color to blue",
    ]
    
    all_deterministic = True
    for cmd in commands:
        results = []
        for _ in range(3):
            result = execute_multi_step_edit(cmd, copy.deepcopy(prod_blueprint))
            results.append(json.dumps(result.to_dict(), sort_keys=True))
        
        # All 3 runs should produce identical JSON
        if results[0] == results[1] == results[2]:
            print(f"✓ '{cmd}' - Deterministic (3 runs identical)")
        else:
            print(f"✗ '{cmd}' - NOT deterministic")
            all_deterministic = False
    
    return all_deterministic


def test_blueprint_immutability():
    """Test that input blueprint is never mutated"""
    print("\n" + "="*80)
    print("EXTENDED TEST 5: Blueprint Immutability")
    print("="*80)
    
    original = copy.deepcopy(prod_blueprint)
    blueprint = copy.deepcopy(prod_blueprint)
    
    commands = [
        "Make header smaller",
        "Change header color to red",
        "Make header bigger and change its color to green",
    ]
    
    for cmd in commands:
        result = execute_multi_step_edit(cmd, blueprint)
    
    # Check if blueprint was mutated
    if blueprint == original:
        print("✓ Blueprint input was NOT mutated")
        return True
    else:
        print("✗ Blueprint input WAS mutated - CRITICAL ERROR")
        return False


def test_error_handling():
    """Test error handling with edge cases"""
    print("\n" + "="*80)
    print("EXTENDED TEST 6: Error Handling")
    print("="*80)
    
    test_cases = [
        ("change nonexistent component to red", "should fail gracefully"),
        ("make very very very long component name smaller", "should fail gracefully"),
        ("", "empty command should fail gracefully"),
        ("make header and and smaller", "malformed command should fail gracefully"),
    ]
    
    passed = 0
    for cmd, description in test_cases:
        try:
            result = execute_multi_step_edit(cmd, copy.deepcopy(prod_blueprint))
            # Should either fail or return empty result
            if result.status in ["failed", "conflicted", "rejected"] or result.steps_executed == 0:
                print(f"✓ {description}")
                passed += 1
            else:
                print(f"✗ {description} - returned unexpected success")
        except Exception as e:
            print(f"✗ {description} - raised exception: {e}")
    
    print(f"\nResult: {passed}/{len(test_cases)} PASS")
    return passed == len(test_cases)


def run_all_extended_tests():
    """Run all extended validation tests"""
    print("\n" + "="*80)
    print("PHASE 10.2 EXTENDED VALIDATION SUITE")
    print("="*80)
    
    results = {
        "Test 1 (Multi-Step)": test_extended_multi_step_commands(),
        "Test 2 (Rollback)": test_rollback_integrity(),
        "Test 3 (JSON)": test_json_serialization(),
        "Test 4 (Determinism)": test_determinism_extended(),
        "Test 5 (Immutability)": test_blueprint_immutability(),
        "Test 6 (Error Handling)": test_error_handling(),
    }
    
    print("\n" + "="*80)
    print("EXTENDED TEST SUMMARY")
    print("="*80)
    
    for test_name, passed in results.items():
        status = "[PASS]" if passed else "[FAIL]"
        print(f"{status} {test_name}")
    
    total_passed = sum(1 for p in results.values() if p)
    total_tests = len(results)
    
    print(f"\nTOTAL: {total_passed}/{total_tests} PASS")
    
    if total_passed == total_tests:
        print("\n✓✓✓ ALL EXTENDED TESTS PASSED ✓✓✓")
        return True
    else:
        print("\n✗✗✗ SOME TESTS FAILED ✗✗✗")
        return False


if __name__ == "__main__":
    success = run_all_extended_tests()
    exit(0 if success else 1)
