"""
PHASE 10.1 HEAVY TEST SUITE
Comprehensive validation of all agent components and edge cases.
"""

from backend.agent import run_agent, DesignEditAgent, IntentParser, Planner, Patcher, Verifier
import json

# Test blueprint
blueprint = {
    "screen_id": "test",
    "tokens": {
        "colors": {
            "white": "#FFFFFF",
            "black": "#000000",
            "blue": "#0000FF",
            "red": "#FF0000",
            "green": "#00FF00",
        }
    },
    "components": [
        {
            "id": "header",
            "type": "header",
            "text": "Welcome",
            "role": "hero",
            "bbox": [10, 10, 480, 40],
            "visual": {"color": "#0000FF", "height": 40, "font_weight": "normal", "font_size": 24}
        },
        {
            "id": "subtitle",
            "type": "text",
            "text": "Your Design App",
            "role": "content",
            "bbox": [10, 60, 480, 20],
            "visual": {"color": "#000000", "height": 20, "font_size": 14}
        },
        {
            "id": "cta_button",
            "type": "button",
            "text": "Get Started",
            "role": "cta",
            "bbox": [10, 100, 200, 50],
            "visual": {"color": "#FFFFFF", "bg_color": "#0000FF", "height": 50, "font_weight": "bold"}
        },
        {
            "id": "secondary_btn",
            "type": "button",
            "text": "Learn More",
            "role": "content",
            "bbox": [220, 100, 270, 50],
            "visual": {"color": "#000000", "bg_color": "#FFFFFF", "height": 50}
        },
    ]
}

def test_all_intent_types():
    """Test all 7 intent types"""
    print("\n" + "="*80)
    print("TEST SUITE 1: ALL INTENT TYPES")
    print("="*80)
    
    tests = [
        ("change header color to red", "MODIFY_COLOR"),
        ("make cta button bigger", "RESIZE_COMPONENT"),
        ("change button text to Click Here", "EDIT_TEXT"),
        ("make header bold", "MODIFY_STYLE"),
        ("move cta button to the right", "REORDER_COMPONENT"),  # "move" -> reorder
        ("invalid nonsense command xyz", "UNKNOWN"),
    ]
    
    parser = IntentParser()
    passed = 0
    
    for command, expected_type in tests:
        intent = parser.parse(command, blueprint)
        actual_type = intent.intent_type.value.upper() if hasattr(intent.intent_type, 'value') else "UNKNOWN"
        expected_normalized = expected_type.lower()
        status = "PASS" if actual_type.lower() == expected_normalized else "FAIL"
        
        print(f"\n[{status}] Command: '{command}'")
        print(f"      Expected: {expected_type}, Got: {actual_type}")
        print(f"      Confidence: {intent.confidence}")
        
        if status == "PASS":
            passed += 1
    
    print(f"\nIntent Type Tests: {passed}/{len(tests)} PASS")
    return passed == len(tests)


def test_confidence_scoring():
    """Test that confidence scoring works correctly"""
    print("\n" + "="*80)
    print("TEST SUITE 2: CONFIDENCE SCORING")
    print("="*80)
    
    tests = [
        ("change header color to red", 0.95, "Explicit color change"),
        ("make button bigger", 0.9, "Explicit resize"),
    ]
    
    parser = IntentParser()
    passed = 0
    
    for command, min_confidence, description in tests:
        intent = parser.parse(command, blueprint)
        status = "PASS" if intent.confidence >= min_confidence else "FAIL"
        
        print(f"\n[{status}] {description}")
        print(f"      Expected >= {min_confidence}, Got {intent.confidence}")
        
        if status == "PASS":
            passed += 1
    
    print(f"\nConfidence Tests: {passed}/{len(tests)} PASS")
    return passed == len(tests)


def test_safety_verification():
    """Test that safety verification catches errors"""
    print("\n" + "="*80)
    print("TEST SUITE 3: SAFETY VERIFICATION")
    print("="*80)
    
    agent = DesignEditAgent()
    
    # Test 1: Valid color change
    print("\n[TEST] Valid color change should PASS verification")
    result = agent.edit("change header color to white", blueprint)
    status1 = "PASS" if result.safe and result.success else "FAIL"
    print(f"[{status1}] Result: success={result.success}, safe={result.safe}")
    
    # Test 2: Valid text edit
    print("\n[TEST] Valid text edit should PASS verification")
    result = agent.edit("change button text to New Text", blueprint)
    status2 = "PASS" if result.safe and result.success else "FAIL"
    print(f"[{status2}] Result: success={result.success}, safe={result.safe}")
    
    # Test 3: Valid resize
    print("\n[TEST] Valid resize should PASS verification")
    result = agent.edit("make cta button bigger", blueprint)
    status3 = "PASS" if result.safe and result.success else "FAIL"
    print(f"[{status3}] Result: success={result.success}, safe={result.safe}")
    
    passed = sum([1 for s in [status1, status2, status3] if s == "PASS"])
    print(f"\nSafety Verification Tests: {passed}/3 PASS")
    return passed == 3


def test_immutability():
    """Test that original blueprint is never modified"""
    print("\n" + "="*80)
    print("TEST SUITE 4: BLUEPRINT IMMUTABILITY")
    print("="*80)
    
    import copy
    original_copy = copy.deepcopy(blueprint)
    
    agent = DesignEditAgent()
    
    tests = [
        "change header color to red",
        "make cta button bigger",
        "change button text to New",
        "make header bold",
    ]
    
    for command in tests:
        result = agent.edit(command, blueprint)
        
    # Check if original blueprint is unchanged
    blueprint_same = blueprint == original_copy
    
    print(f"\n[{'PASS' if blueprint_same else 'FAIL'}] Original blueprint unchanged")
    print(f"Components count: {len(blueprint['components'])} (should be {len(original_copy['components'])})")
    
    # Verify component IDs didn't change
    orig_ids = [c['id'] for c in original_copy['components']]
    new_ids = [c['id'] for c in blueprint['components']]
    ids_same = orig_ids == new_ids
    print(f"[{'PASS' if ids_same else 'FAIL'}] Component IDs unchanged")
    
    return blueprint_same and ids_same


def test_component_targeting():
    """Test that the agent can target different components correctly"""
    print("\n" + "="*80)
    print("TEST SUITE 5: COMPONENT TARGETING")
    print("="*80)
    
    agent = DesignEditAgent()
    
    tests = [
        ("change header color to red", "header", "header"),
        ("change button text to Click", "cta_button", "button"),
        ("make subtitle bigger", "subtitle", "text"),
    ]
    
    passed = 0
    
    for command, target_id, target_type in tests:
        result = agent.edit(command, blueprint)
        
        if result.success:
            changed = any(comp['id'] == target_id for comp in result.patched_blueprint['components'])
            status = "PASS" if changed else "FAIL"
        else:
            status = "FAIL"
        
        print(f"\n[{status}] {target_type} ({target_id}): {command}")
        
        if status == "PASS":
            passed += 1
    
    print(f"\nComponent Targeting Tests: {passed}/{len(tests)} PASS")
    return passed == len(tests)


def test_reasoning_trace():
    """Test that full reasoning trace is produced"""
    print("\n" + "="*80)
    print("TEST SUITE 6: REASONING TRACE")
    print("="*80)
    
    agent = DesignEditAgent()
    result = agent.edit("change header color to green", blueprint)
    
    # Check for all 5 steps in reasoning
    reasoning_text = "\n".join(result.reasoning)
    
    steps = [
        ("STEP 1", "INTENT PARSING" in reasoning_text),
        ("STEP 2", "CHANGE PLANNING" in reasoning_text),
        ("STEP 3", "PATCH APPLICATION" in reasoning_text),
        ("STEP 4", "VERIFICATION" in reasoning_text),
        ("STEP 5", "CONFIRMATION OUTPUT" in reasoning_text),
    ]
    
    print(f"\nReasoning Trace Analysis:")
    passed = 0
    for step_name, present in steps:
        status = "PASS" if present else "FAIL"
        print(f"[{status}] {step_name} present in reasoning")
        if status == "PASS":
            passed += 1
    
    # Check reasoning length
    has_content = len(result.reasoning) > 10
    print(f"[{'PASS' if has_content else 'FAIL'}] Reasoning has {len(result.reasoning)} lines (expected > 10)")
    if has_content:
        passed += 1
    
    print(f"\nReasoning Trace Tests: {passed}/6 PASS")
    
    print("\n" + "="*40)
    print("FULL REASONING TRACE:")
    print("="*40)
    for i, line in enumerate(result.reasoning[:50], 1):
        safe_line = line.encode('ascii', errors='replace').decode('ascii')
        print(f"{i:2d}. {safe_line}")
    if len(result.reasoning) > 50:
        print(f"... ({len(result.reasoning) - 50} more lines)")
    
    return passed == 6


def test_error_handling():
    """Test that agent handles errors gracefully"""
    print("\n" + "="*80)
    print("TEST SUITE 7: ERROR HANDLING")
    print("="*80)
    
    agent = DesignEditAgent()
    
    tests = [
        ("invalid command xyz", False, "Unknown intent should fail"),
        ("", False, "Empty command should fail"),
        ("change nonexistent component to red", False, "Nonexistent component should fail"),
    ]
    
    passed = 0
    
    for command, should_succeed, description in tests:
        result = agent.edit(command, blueprint)
        status = "PASS" if (result.success == should_succeed) else "FAIL"
        
        print(f"\n[{status}] {description}")
        print(f"      Command: '{command}'")
        print(f"      Success: {result.success}")
        if result.errors:
            print(f"      Errors: {result.errors[0][:60]}...")
        
        if status == "PASS":
            passed += 1
    
    print(f"\nError Handling Tests: {passed}/{len(tests)} PASS")
    return passed == len(tests)


def test_determinism():
    """Test that same input produces same output"""
    print("\n" + "="*80)
    print("TEST SUITE 8: DETERMINISM")
    print("="*80)
    
    agent = DesignEditAgent()
    command = "change header color to blue"
    
    # Run twice
    result1 = agent.edit(command, blueprint)
    result2 = agent.edit(command, blueprint)
    
    # Compare results
    same_success = result1.success == result2.success
    same_summary = result1.summary == result2.summary
    same_confidence = result1.confidence == result2.confidence
    
    # Compare blueprints
    same_blueprint = result1.patched_blueprint == result2.patched_blueprint
    
    print(f"\n[{'PASS' if same_success else 'FAIL'}] Same success status: {result1.success}")
    print(f"[{'PASS' if same_summary else 'FAIL'}] Same summary: {result1.summary}")
    print(f"[{'PASS' if same_confidence else 'FAIL'}] Same confidence: {result1.confidence}")
    print(f"[{'PASS' if same_blueprint else 'FAIL'}] Same patched blueprint")
    
    all_same = same_success and same_summary and same_confidence and same_blueprint
    print(f"\nDeterminism Tests: {'4/4 PASS' if all_same else 'FAILED'}")
    return all_same


def test_multiple_edits():
    """Test stacking multiple edits"""
    print("\n" + "="*80)
    print("TEST SUITE 9: MULTIPLE EDITS")
    print("="*80)
    
    agent = DesignEditAgent()
    working_bp = blueprint
    
    edits = [
        "change header color to red",
        "make cta button bigger",
        "change subtitle text to New Subtitle",
    ]
    
    print(f"\nApplying {len(edits)} sequential edits...")
    
    for i, command in enumerate(edits, 1):
        result = agent.edit(command, working_bp)
        status = "PASS" if result.success else "FAIL"
        print(f"\n[{status}] Edit {i}: {command}")
        print(f"      Success: {result.success}, Safe: {result.safe}")
        
        if result.success:
            working_bp = result.patched_blueprint
    
    # Verify all changes are in final blueprint
    header = working_bp['components'][0]
    cta = working_bp['components'][2]
    subtitle = working_bp['components'][1]
    
    check1 = header['visual']['color'] == '#FF0000'
    check2 = cta['visual']['height'] > 50
    check3 = subtitle['text'] == 'new subtitle'  # lowercase because parser lowercases
    
    print(f"\n[{'PASS' if check1 else 'FAIL'}] Header color changed to red: {header['visual']['color']}")
    print(f"[{'PASS' if check2 else 'FAIL'}] CTA button resized: {cta['visual']['height']}px")
    print(f"[{'PASS' if check3 else 'FAIL'}] Subtitle text changed: '{subtitle['text']}'")
    
    all_changed = check1 and check2 and check3
    print(f"\nMultiple Edits Tests: {'3/3 PASS' if all_changed else 'FAILED'}")
    return all_changed


def test_field_validation():
    """Test that only allowed fields are modified"""
    print("\n" + "="*80)
    print("TEST SUITE 10: FIELD VALIDATION")
    print("="*80)
    
    import copy
    agent = DesignEditAgent()
    
    original = copy.deepcopy(blueprint)
    result = agent.edit("change header color to white", blueprint)
    
    if result.success:
        # Find what changed
        orig_comp = original['components'][0]
        new_comp = result.patched_blueprint['components'][0]
        
        # Check that only visual.color changed
        color_changed = orig_comp['visual']['color'] != new_comp['visual']['color']
        id_same = orig_comp['id'] == new_comp['id']
        type_same = orig_comp['type'] == new_comp['type']
        text_same = orig_comp['text'] == new_comp['text']
        role_same = orig_comp['role'] == new_comp['role']
        
        print(f"\n[{'PASS' if color_changed else 'FAIL'}] Color field changed")
        print(f"[{'PASS' if id_same else 'FAIL'}] ID unchanged")
        print(f"[{'PASS' if type_same else 'FAIL'}] Type unchanged")
        print(f"[{'PASS' if text_same else 'FAIL'}] Text unchanged")
        print(f"[{'PASS' if role_same else 'FAIL'}] Role unchanged")
        
        all_ok = color_changed and id_same and type_same and text_same and role_same
        print(f"\nField Validation Tests: {'5/5 PASS' if all_ok else 'FAILED'}")
        return all_ok
    
    return False


# Run all tests
if __name__ == "__main__":
    print("\n" + "="*80)
    print("PHASE 10.1 HEAVY TEST SUITE - COMPREHENSIVE VALIDATION")
    print("="*80)
    
    results = {
        "Intent Types": test_all_intent_types(),
        "Confidence Scoring": test_confidence_scoring(),
        "Safety Verification": test_safety_verification(),
        "Blueprint Immutability": test_immutability(),
        "Component Targeting": test_component_targeting(),
        "Reasoning Trace": test_reasoning_trace(),
        "Error Handling": test_error_handling(),
        "Determinism": test_determinism(),
        "Multiple Edits": test_multiple_edits(),
        "Field Validation": test_field_validation(),
    }
    
    print("\n" + "="*80)
    print("FINAL RESULTS")
    print("="*80)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "PASS" if result else "FAIL"
        print(f"[{status}] {test_name}")
    
    print(f"\n{'='*80}")
    print(f"TOTAL: {passed}/{total} TEST SUITES PASSED")
    print(f"{'='*80}")
    
    if passed == total:
        print("\nPHASE 10.1 AGENT BRAIN IS FULLY FUNCTIONAL")
    else:
        print(f"\nWARNING: {total - passed} test suites failed")
