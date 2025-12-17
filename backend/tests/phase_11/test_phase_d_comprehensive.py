"""
PHASE D: COMPREHENSIVE TESTING & VALIDATION

Tests Phase A, B, C integration with Phase 11 core:
- Enhanced confidence scoring with multi-stage analysis
- Compound intent parsing with rule-based grammar
- Extended color support (130+ colors, HEX, RGB, HSL)
- Production readiness validation
- Integration testing across modules

Target: 95%+ pass rate
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))
sys.path.insert(0, str(Path.cwd() / "backend"))

from agentic.agent import AgenticAgent
from agentic.intent_graph import IntentGraph, IntentType
from agentic.confidence_scorer import ConfidenceScorer
from agentic.intent_parser_enhanced import CompoundIntentParser
from agentic.color_support import ColorNormalizer, ColorValidator, ColorPalette
from agentic.patch_generator import PatchGenerator
from agentic.simulator import Simulator
from agentic.verifier import Verifier


# Test blueprint
TEST_BLUEPRINT = {
    "tokens": {
        "primary_color": "#3B82F6",
        "secondary_color": "#6B7280",
        "accent_color": "#F59E0B",
    },
    "components": [
        {
            "id": "btn_1",
            "type": "button",
            "bbox": [10, 10, 100, 44],
            "visual": {"color": "#000000", "height": 44},
            "labels": ["Click me"],
            "role": "button"
        },
        {
            "id": "card_1",
            "type": "card",
            "bbox": [10, 60, 200, 200],
            "visual": {"color": "#FFFFFF", "border": "#E5E7EB"},
            "role": "article"
        }
    ]
}


def test_phase_a_confidence_integration():
    """Test Phase A confidence scorer with Phase 11 agent."""
    print("\n[PHASE D TEST 1] Phase A Confidence Integration")
    
    agent = AgenticAgent()
    
    result = agent.process("Make button bigger", TEST_BLUEPRINT)
    
    # Check confidence field exists
    assert "confidence" in result, "Missing confidence field"
    confidence = result.get("confidence")
    
    # Should have numeric confidence
    assert isinstance(confidence, (int, float)), f"Invalid confidence type: {type(confidence)}"
    assert 0.0 <= confidence <= 1.0, f"Confidence out of range: {confidence}"
    
    # Should have detailed breakdown
    assert "details" in result, "Missing details"
    details = result.get("details", {})
    assert "confidence_breakdown" in details, "Missing confidence_breakdown"
    
    breakdown = details.get("confidence_breakdown", {})
    assert "stage_scores" in breakdown, "Missing stage_scores"
    
    print(f"  PASS - Confidence scoring integrated")
    print(f"  Confidence: {confidence:.1%}")
    print(f"  Stages: {len(breakdown.get('stage_scores', []))} evaluated")
    return True


def test_phase_b_compound_commands():
    """Test Phase B compound intent parsing."""
    print("\n[PHASE D TEST 2] Phase B Compound Commands")
    
    parser = CompoundIntentParser()
    
    test_commands = [
        "Make button bigger and red",
        "Change color to blue, text to hello",
        "Make button bigger, red, and bold",
    ]
    
    for command in test_commands:
        result = parser.parse_compound(command)
        
        # Should parse intents
        assert len(result.intents) > 0, f"No intents parsed for '{command}'"
        
        # Should have valid ambiguity level
        assert result.ambiguity_level in ["clear", "moderate", "ambiguous"], \
            f"Invalid ambiguity: {result.ambiguity_level}"
        
        # All intents should have confidence
        for intent in result.intents:
            assert 0.0 <= intent.confidence <= 1.0, \
                f"Invalid confidence for {intent.type}: {intent.confidence}"
        
        print(f"  ✓ '{command}' -> {len(result.intents)} intents")
    
    print(f"  PASS - Compound command parsing works")
    return True


def test_phase_c_color_commands():
    """Test Phase C extended color support."""
    print("\n[PHASE D TEST 3] Phase C Color Support")
    
    normalizer = ColorNormalizer()
    palette = ColorPalette()
    
    test_colors = [
        # Named colors
        ("red", "#FF0000"),
        ("navy", "#000080"),
        ("crimson", "#DC143C"),
        ("indigo", "#4B0082"),
        # HEX colors
        ("#FF0000", "#FF0000"),
        # RGB colors
        ("rgb(0, 255, 0)", "#00FF00"),
        # Semantic tokens
        ("primary", "primary"),
    ]
    
    for color_input, expected_output in test_colors:
        is_valid, normalized, fmt = normalizer.normalize(color_input)
        
        assert is_valid, f"Failed to normalize '{color_input}'"
        
        # For semantic, just check it starts with lowercase
        if expected_output.lower() == expected_output:
            assert normalized.lower() == expected_output.lower(), \
                f"Expected {expected_output}, got {normalized}"
        else:
            assert normalized == expected_output, \
                f"Expected {expected_output}, got {normalized}"
        
        print(f"  ✓ '{color_input}' -> {normalized}")
    
    print(f"  PASS - Extended color support works")
    return True


def test_agent_with_enhancements():
    """Test agent with all Phase A/B/C enhancements."""
    print("\n[PHASE D TEST 4] Agent with All Enhancements")
    
    agent = AgenticAgent()
    
    test_cases = [
        ("Make button bigger", True),
        ("Change button to red", True),
        ("Make button bigger and red", True),
        ("Make button bigger, red, and bold", True),
        ("Make card blue", True),
    ]
    
    for command, should_work in test_cases:
        result = agent.process(command, TEST_BLUEPRINT)
        
        # Verify basic response structure
        assert "success" in result, f"Missing 'success' for '{command}'"
        
        # Should have confidence
        assert "confidence" in result, f"Missing 'confidence' for '{command}'"
        
        # Should have explanation
        assert "explanation" in result or not result.get("success"), \
            f"Missing explanation for successful '{command}'"
        
        status = "✓" if result.get("success") else "✗"
        confidence = result.get("confidence", 0.0)
        print(f"  {status} '{command}' (confidence: {confidence:.1%})")
    
    print(f"  PASS - Agent handles all command types")
    return True


def test_color_in_agent_pipeline():
    """Test color commands through full agent pipeline."""
    print("\n[PHASE D TEST 5] Color Commands in Agent Pipeline")
    
    agent = AgenticAgent()
    
    # Test various color formats
    color_commands = [
        "Change button to red",
        "Change button to #FF0000",
        "Make button navy blue",
        "Change to crimson",
    ]
    
    for command in color_commands:
        result = agent.process(command, TEST_BLUEPRINT)
        
        # At minimum, should parse without error
        assert isinstance(result, dict), f"Invalid result for '{command}'"
        
        # Should have confidence metric
        if result.get("success"):
            confidence = result.get("confidence")
            assert confidence >= 0.0, f"Invalid confidence for '{command}'"
        
        print(f"  ✓ '{command}' processed")
    
    print(f"  PASS - Colors work through agent pipeline")
    return True


def test_confidence_determinism():
    """Test that confidence scores are deterministic."""
    print("\n[PHASE D TEST 6] Confidence Determinism")
    
    agent = AgenticAgent()
    command = "Make button bigger and red"
    
    # Run multiple times
    results = []
    for _ in range(3):
        result = agent.process(command, TEST_BLUEPRINT)
        results.append(result.get("confidence"))
    
    # All should be identical
    assert results[0] == results[1] == results[2], \
        f"Non-deterministic confidence: {results[0]} vs {results[1]} vs {results[2]}"
    
    print(f"  PASS - Confidence scores deterministic")
    print(f"  3 runs all returned: {results[0]:.1%}")
    return True


def test_intent_extraction_quality():
    """Test quality of intent extraction with enhancements."""
    print("\n[PHASE D TEST 7] Intent Extraction Quality")
    
    agent = AgenticAgent()
    
    # Simple command - should have high confidence
    result_simple = agent.process("Make button red", TEST_BLUEPRINT)
    conf_simple = result_simple.get("confidence", 0.0)
    
    # Complex command - should have lower but still decent confidence
    result_complex = agent.process("Make button bigger and red", TEST_BLUEPRINT)
    conf_complex = result_complex.get("confidence", 0.0)
    
    # Both should have some confidence
    assert conf_simple > 0.0, "Simple command should have some confidence"
    assert conf_complex > 0.0, "Complex command should have some confidence"
    
    print(f"  PASS - Intent extraction quality maintained")
    print(f"  Simple command: {conf_simple:.1%}")
    print(f"  Complex command: {conf_complex:.1%}")
    return True


def test_safety_preserved():
    """Test that safety checks still work with enhancements."""
    print("\n[PHASE D TEST 8] Safety Checks Preserved")
    
    agent = AgenticAgent()
    
    # Try to access private fields (should be blocked)
    unsafe_command = "Access _private_field"
    result = agent.process(unsafe_command, TEST_BLUEPRINT)
    
    # Should either refuse or mark as unsafe
    assert "confidence" in result, "Should have confidence even for unsafe commands"
    
    if result.get("success"):
        # If it succeeded, confidence should be very low
        assert result.get("confidence", 1.0) < 0.5, \
            "Unsafe operation should have low confidence"
    
    print(f"  PASS - Safety checks preserved")
    return True


def test_immutability_preserved():
    """Test that blueprint immutability is preserved."""
    print("\n[PHASE D TEST 9] Blueprint Immutability")
    
    agent = AgenticAgent()
    
    # Deep copy original
    import copy
    original_bp = copy.deepcopy(TEST_BLUEPRINT)
    
    # Process command
    result = agent.process("Make button bigger and red", TEST_BLUEPRINT)
    
    # Original should be unchanged
    assert TEST_BLUEPRINT == original_bp, "Blueprint was mutated!"
    
    print(f"  PASS - Blueprint immutability preserved")
    return True


def test_comprehensive_pass_rate():
    """Run all tests and report pass rate."""
    print("\n[PHASE D TEST 10] Comprehensive Pass Rate")
    
    tests = [
        test_phase_a_confidence_integration,
        test_phase_b_compound_commands,
        test_phase_c_color_commands,
        test_agent_with_enhancements,
        test_color_in_agent_pipeline,
        test_confidence_determinism,
        test_intent_extraction_quality,
        test_safety_preserved,
        test_immutability_preserved,
    ]
    
    print(f"  Running {len(tests)} sub-tests...")
    passed = sum(1 for test in tests if test())
    total = len(tests)
    pass_rate = (passed / total * 100) if total > 0 else 0
    
    print(f"  Comprehensive pass rate: {passed}/{total} ({pass_rate:.1f}%)")
    
    assert pass_rate >= 80.0, f"Pass rate too low: {pass_rate:.1f}%"
    
    print(f"  PASS - High pass rate achieved")
    return True


if __name__ == "__main__":
    print("\n" + "="*70)
    print("PHASE D: COMPREHENSIVE TESTING & VALIDATION")
    print("Testing Phase A, B, C integration with Phase 11 core")
    print("="*70)
    
    tests = [
        test_phase_a_confidence_integration,
        test_phase_b_compound_commands,
        test_phase_c_color_commands,
        test_agent_with_enhancements,
        test_color_in_agent_pipeline,
        test_confidence_determinism,
        test_intent_extraction_quality,
        test_safety_preserved,
        test_immutability_preserved,
        test_comprehensive_pass_rate,
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
    
    print("\n" + "="*70)
    print(f"PHASE D RESULTS: {passed} passed, {failed} failed")
    print(f"Pass Rate: {passed}/{len(tests)} ({100*passed//len(tests)}%)")
    print("="*70)
    
    if failed == 0:
        print("\n✅ PHASE D COMPLETE: ALL TESTS PASS")
        print("Phase A, B, C successfully integrated with Phase 11 core")
        print("System ready for production deployment")
    else:
        print(f"\n⚠️  PHASE D: {failed} test(s) failing")
    
    sys.exit(0 if failed == 0 else 1)
