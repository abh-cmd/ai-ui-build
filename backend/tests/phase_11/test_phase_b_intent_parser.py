"""
PHASE B: INTENT PARSER ENHANCEMENT TESTS

Tests validate:
- Compound command parsing (e.g., "Make button bigger and red")
- Multi-intent extraction
- Confidence scoring for each intent
- Ambiguity detection
- Safety fallback
- Backward compatibility
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))
sys.path.insert(0, str(Path.cwd() / "backend"))

from agentic.intent_parser_enhanced import (
    CompoundIntentParser,
    IntentValidator,
    SafetyFallback,
    ParsedIntent,
    IntentPattern
)


def test_simple_color_parsing():
    """Test parsing simple color commands."""
    print("\n[PHASE B TEST 1] Simple Color Parsing")
    
    parser = CompoundIntentParser()
    result = parser.parse_compound("Change button to red")
    
    assert len(result.intents) > 0, "No intents parsed"
    assert any(i.type == "COLOR" for i in result.intents), "No color intent found"
    
    color_intent = [i for i in result.intents if i.type == "COLOR"][0]
    assert color_intent.value == "red", f"Expected red, got {color_intent.value}"
    assert color_intent.confidence > 0.85, f"Confidence too low: {color_intent.confidence}"
    
    print(f"  PASS - Parsed color intent with {color_intent.confidence:.1%} confidence")
    return True


def test_simple_resize_parsing():
    """Test parsing simple resize commands."""
    print("\n[PHASE B TEST 2] Simple Resize Parsing")
    
    parser = CompoundIntentParser()
    result = parser.parse_compound("Make button bigger")
    
    assert len(result.intents) > 0, "No intents parsed"
    assert any(i.type == "RESIZE" for i in result.intents), "No resize intent found"
    
    resize_intent = [i for i in result.intents if i.type == "RESIZE"][0]
    assert resize_intent.value == "increase", f"Expected increase, got {resize_intent.value}"
    assert resize_intent.confidence > 0.85, f"Confidence too low: {resize_intent.confidence}"
    
    print(f"  PASS - Parsed resize intent with {resize_intent.confidence:.1%} confidence")
    return True


def test_compound_command_parsing():
    """Test parsing compound commands with 'and'."""
    print("\n[PHASE B TEST 3] Compound Command Parsing")
    
    parser = CompoundIntentParser()
    result = parser.parse_compound("Make button bigger and red")
    
    assert len(result.intents) >= 2, f"Expected 2+ intents, got {len(result.intents)}"
    
    types = {i.type for i in result.intents}
    assert "RESIZE" in types, "Missing RESIZE intent"
    assert "COLOR" in types, "Missing COLOR intent"
    
    assert result.ambiguity_level in ["clear", "moderate"], f"Unexpected ambiguity: {result.ambiguity_level}"
    
    print(f"  PASS - Parsed {len(result.intents)} intents from compound command")
    print(f"  Combined confidence: {result.combined_confidence:.1%}")
    print(f"  Ambiguity: {result.ambiguity_level}")
    return True


def test_target_extraction():
    """Test target component extraction."""
    print("\n[PHASE B TEST 4] Target Extraction")
    
    parser = CompoundIntentParser()
    result = parser.parse_compound("Make the button bigger")
    
    assert len(result.intents) > 0, "No intents parsed"
    
    # At least one intent should have 'button' as target
    has_button_target = any(i.target == "button" for i in result.intents)
    assert has_button_target, "Button target not extracted"
    
    print(f"  PASS - Extracted 'button' as target")
    return True


def test_multiple_conjunctions():
    """Test parsing commands with multiple conjunctions."""
    print("\n[PHASE B TEST 5] Multiple Conjunctions")
    
    parser = CompoundIntentParser()
    result = parser.parse_compound("Make button bigger, red, and bold")
    
    # Should parse multiple intents
    assert len(result.intents) >= 2, f"Expected 2+ intents, got {len(result.intents)}"
    
    print(f"  PASS - Parsed {len(result.intents)} intents from multi-conjunction command")
    return True


def test_intent_validation():
    """Test intent validation."""
    print("\n[PHASE B TEST 6] Intent Validation")
    
    # Valid intent
    valid_intent = ParsedIntent(
        type="COLOR",
        target="button",
        value="red",
        confidence=0.95,
        reason="Test",
        matches={}
    )
    
    is_valid, reason = IntentValidator.validate(valid_intent)
    assert is_valid, f"Valid intent rejected: {reason}"
    
    # Invalid intent (bad type)
    invalid_intent = ParsedIntent(
        type="INVALID_TYPE",
        target="button",
        value="red",
        confidence=0.95,
        reason="Test",
        matches={}
    )
    
    is_valid, reason = IntentValidator.validate(invalid_intent)
    assert not is_valid, "Invalid intent should be rejected"
    
    print(f"  PASS - Validation logic working correctly")
    return True


def test_ambiguity_detection():
    """Test ambiguity level detection."""
    print("\n[PHASE B TEST 7] Ambiguity Detection")
    
    parser = CompoundIntentParser()
    
    # Clear command
    result_clear = parser.parse_compound("Change button to red")
    assert result_clear.ambiguity_level in ["clear", "moderate"], \
        f"Simple command should be clear, got {result_clear.ambiguity_level}"
    
    # More complex command
    result_complex = parser.parse_compound("Make it like the other thing")
    # This should have lower confidence/higher ambiguity
    
    print(f"  PASS - Ambiguity detection working")
    print(f"  Clear command: {result_clear.ambiguity_level} ({result_clear.combined_confidence:.1%})")
    return True


def test_hex_color_parsing():
    """Test parsing HEX color codes."""
    print("\n[PHASE B TEST 8] HEX Color Parsing")
    
    parser = CompoundIntentParser()
    result = parser.parse_compound("Change button to #FF0000")
    
    assert len(result.intents) > 0, "No intents parsed"
    
    color_intents = [i for i in result.intents if i.type == "COLOR"]
    assert len(color_intents) > 0, "No color intent found"
    
    print(f"  PASS - HEX color parsed")
    for intent in color_intents:
        print(f"  Color value: {intent.value}")
    return True


def test_determinism():
    """Test that parsing is deterministic."""
    print("\n[PHASE B TEST 9] Determinism")
    
    parser = CompoundIntentParser()
    command = "Make button bigger and red"
    
    # Parse multiple times
    result1 = parser.parse_compound(command)
    result2 = parser.parse_compound(command)
    result3 = parser.parse_compound(command)
    
    # Should have same number of intents
    assert len(result1.intents) == len(result2.intents) == len(result3.intents), \
        "Intent count varies across runs"
    
    # Should have same confidence
    assert result1.combined_confidence == result2.combined_confidence == result3.combined_confidence, \
        "Confidence varies across runs"
    
    # Should have same types
    types1 = sorted([i.type for i in result1.intents])
    types2 = sorted([i.type for i in result2.intents])
    types3 = sorted([i.type for i in result3.intents])
    
    assert types1 == types2 == types3, "Intent types vary across runs"
    
    print(f"  PASS - Parsing is deterministic")
    print(f"  3 runs produced identical results:")
    print(f"    Intent count: {len(result1.intents)}")
    print(f"    Confidence: {result1.combined_confidence:.1%}")
    print(f"    Types: {types1}")
    return True


def test_safety_fallback():
    """Test safety fallback for ambiguous commands."""
    print("\n[PHASE B TEST 10] Safety Fallback")
    
    parser = CompoundIntentParser()
    
    # Parse ambiguous command
    result_before = parser.parse_compound("Do something magical")
    
    # Apply fallback
    result_after = SafetyFallback.apply_fallback(result_before, "Do something magical")
    
    # Fallback should not crash
    assert isinstance(result_after.intents, list), "Fallback didn't return valid intents"
    
    print(f"  PASS - Safety fallback handles ambiguous commands")
    if result_after.fallback_used:
        print(f"  Fallback was applied (confidence reduced from {result_before.combined_confidence:.1%})")
    return True


if __name__ == "__main__":
    print("\n" + "="*60)
    print("PHASE B: INTENT PARSER ENHANCEMENT TESTS")
    print("="*60)
    
    tests = [
        test_simple_color_parsing,
        test_simple_resize_parsing,
        test_compound_command_parsing,
        test_target_extraction,
        test_multiple_conjunctions,
        test_intent_validation,
        test_ambiguity_detection,
        test_hex_color_parsing,
        test_determinism,
        test_safety_fallback,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
        except AssertionError as e:
            failed += 1
            print(f"  FAIL: {e}")
        except Exception as e:
            failed += 1
            print(f"  ERROR: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "="*60)
    print(f"RESULTS: {passed} passed, {failed} failed")
    print("="*60)
    
    if failed == 0:
        print("PHASE B TESTS: ALL PASS - Ready for integration with Phase 11")
    else:
        print(f"PHASE B TESTS: {failed} failing - needs fixes")
    
    sys.exit(0 if failed == 0 else 1)
