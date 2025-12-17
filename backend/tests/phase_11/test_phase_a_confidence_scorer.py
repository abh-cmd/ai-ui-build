"""
TEST: Confidence Scorer - Phase A Enhancement Tests

Tests verify:
- Deterministic scoring (same input = same output)
- Weighted stage calculation
- Penalty/boost application
- Confidence stability across runs
- Immutability of inputs
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))
sys.path.insert(0, str(Path.cwd() / "backend"))

from agentic.confidence_scorer import ConfidenceScorer, ConfidenceStage, StageConfidence
from agentic.intent_graph import IntentType, Intent
from agentic.patch_generator import JSONPatch


def test_deterministic_scoring():
    """CRITICAL: Confidence scoring must be deterministic."""
    print("\n[PHASE A TEST 1] Deterministic Scoring")
    
    scorer = ConfidenceScorer()
    
    # Create test data
    intents = [
        Intent(
            type=IntentType.COLOR,
            target="button",
            value="red",
            params=None,
            confidence=0.95
        )
    ]
    
    blueprint = {
        "tokens": {"primary_color": "#3B82F6"},
        "components": [
            {
                "id": "btn_1",
                "type": "button",
                "bbox": [10, 10, 100, 44],
                "visual": {"color": "#000000"}
            }
        ]
    }
    
    patches = [JSONPatch(op="replace", path="/components/0/visual/color", value="#E63946")]
    
    # Score same input multiple times
    report1 = scorer.score("Change button to red", intents, blueprint, blueprint, patches)
    report2 = scorer.score("Change button to red", intents, blueprint, blueprint, patches)
    report3 = scorer.score("Change button to red", intents, blueprint, blueprint, patches)
    
    # Verify identical scores
    assert report1.final_score == report2.final_score == report3.final_score, \
        f"Determinism failed: {report1.final_score} vs {report2.final_score} vs {report3.final_score}"
    
    # Verify stage scores identical
    for s1, s2, s3 in zip(report1.stage_scores, report2.stage_scores, report3.stage_scores):
        assert s1.score == s2.score == s3.score, \
            f"Stage {s1.stage.value} not deterministic: {s1.score} vs {s2.score} vs {s3.score}"
    
    print(f"  PASS - Scoring deterministic across 3 runs")
    print(f"  Score: {report1.final_score:.1%} (consistent)")
    return True


def test_single_intent_boost():
    """Single-intent commands should get confidence boost."""
    print("\n[PHASE A TEST 2] Single-Intent Boost")
    
    scorer = ConfidenceScorer()
    
    single_intent = [
        Intent(
            type=IntentType.COLOR,
            target="button",
            value="red",
            params=None,
            confidence=0.90
        )
    ]
    
    multi_intent = [
        Intent(
            type=IntentType.COLOR,
            target="button",
            value="red",
            params=None,
            confidence=0.90
        ),
        Intent(
            type=IntentType.RESIZE,
            target="button",
            value=None,
            params={"height": 60},
            confidence=0.85
        )
    ]
    
    blueprint = {
        "tokens": {"primary_color": "#3B82F6"},
        "components": [
            {
                "id": "btn_1",
                "type": "button",
                "bbox": [10, 10, 100, 44],
                "visual": {"color": "#000000"}
            }
        ]
    }
    
    patches = [JSONPatch(op="replace", path="/components/0/visual/color", value="#E63946")]
    
    report_single = scorer.score("Change button to red", single_intent, blueprint, blueprint, patches)
    report_multi = scorer.score("Change button and resize", multi_intent, blueprint, blueprint, patches)
    
    # Single intent should score higher
    assert report_single.final_score > report_multi.final_score, \
        f"Single-intent boost failed: {report_single.final_score} should be > {report_multi.final_score}"
    
    # Verify boost was applied
    single_boosts = [b[0] for b in report_single.boosts]
    assert any("single-intent" in b.lower() for b in single_boosts), \
        f"Single-intent boost not found in {single_boosts}"
    
    print(f"  PASS - Single-intent boost applied")
    print(f"  Single-intent: {report_single.final_score:.1%} > Multi-intent: {report_multi.final_score:.1%}")
    return True


def test_ambiguous_targeting_penalty():
    """Ambiguous targeting should apply penalty."""
    print("\n[PHASE A TEST 3] Ambiguous Targeting Penalty")
    
    scorer = ConfidenceScorer()
    
    ambiguous_intent = [
        Intent(
            type=IntentType.COLOR,
            target=None,  # Ambiguous - no target
            value="red",
            params=None,
            confidence=0.80
        )
    ]
    
    exact_intent = [
        Intent(
            type=IntentType.COLOR,
            target="button",  # Exact target
            value="red",
            params=None,
            confidence=0.95
        )
    ]
    
    blueprint = {
        "tokens": {"primary_color": "#3B82F6"},
        "components": [
            {
                "id": "btn_1",
                "type": "button",
                "bbox": [10, 10, 100, 44],
                "visual": {"color": "#000000"}
            }
        ]
    }
    
    patches = [JSONPatch(op="replace", path="/components/0/visual/color", value="#E63946")]
    
    report_ambiguous = scorer.score("Change color to red", ambiguous_intent, blueprint, blueprint, patches)
    report_exact = scorer.score("Change button to red", exact_intent, blueprint, blueprint, patches)
    
    # Exact should score higher (due to ambiguous penalty)
    assert report_exact.final_score > report_ambiguous.final_score, \
        f"Ambiguous penalty failed: {report_exact.final_score} should be > {report_ambiguous.final_score}"
    
    # Verify penalty exists
    assert len(report_ambiguous.penalties) > 0, "No penalties applied to ambiguous intent"
    
    print(f"  PASS - Ambiguous targeting penalty applied")
    print(f"  Exact: {report_exact.final_score:.1%} > Ambiguous: {report_ambiguous.final_score:.1%}")
    return True


def test_stage_weights():
    """Verify stage weights are properly applied."""
    print("\n[PHASE A TEST 4] Stage Weight Application")
    
    scorer = ConfidenceScorer()
    
    # Verify weights sum to 1.0
    total_weight = sum(scorer.WEIGHTS.values())
    assert abs(total_weight - 1.0) < 0.001, f"Weights don't sum to 1.0: {total_weight}"
    
    print(f"  PASS - Weights properly configured")
    print(f"  Weights: {scorer.WEIGHTS}")
    print(f"  Total: {total_weight:.2f}")
    
    # Verify each weight is positive
    for stage, weight in scorer.WEIGHTS.items():
        assert weight > 0, f"Negative weight for {stage}: {weight}"
        assert weight <= 1.0, f"Weight exceeds 1.0 for {stage}: {weight}"
    
    print(f"  PASS - All weights valid (0 < w <= 1.0)")
    return True


def test_input_immutability():
    """Verify scorer doesn't modify input objects."""
    print("\n[PHASE A TEST 5] Input Immutability")
    
    scorer = ConfidenceScorer()
    
    original_intent = Intent(
        type=IntentType.COLOR,
        target="button",
        value="red",
        params=None,
        confidence=0.90
    )
    
    intents = [original_intent]
    
    blueprint = {
        "tokens": {"primary_color": "#3B82F6"},
        "components": [
            {
                "id": "btn_1",
                "type": "button",
                "bbox": [10, 10, 100, 44],
                "visual": {"color": "#000000"}
            }
        ]
    }
    
    patches = [JSONPatch(op="replace", path="/components/0/visual/color", value="#E63946")]
    
    # Record original state
    original_target = original_intent.target
    original_value = original_intent.value
    original_confidence = original_intent.confidence
    
    # Run scorer
    scorer.score("Change button to red", intents, blueprint, blueprint, patches)
    
    # Verify no mutations
    assert original_intent.target == original_target, "Intent target was mutated"
    assert original_intent.value == original_value, "Intent value was mutated"
    assert original_intent.confidence == original_confidence, "Intent confidence was mutated"
    
    print(f"  PASS - No mutations to input objects")
    return True


def test_confidence_range():
    """Verify confidence scores stay in valid range [0.0, 1.0]."""
    print("\n[PHASE A TEST 6] Confidence Range Validation")
    
    scorer = ConfidenceScorer()
    
    # Test various scenarios
    test_cases = [
        ("Single color change", [Intent(IntentType.COLOR, "button", "red", None, 0.95)]),
        ("Low confidence intent", [Intent(IntentType.COLOR, None, "red", None, 0.50)]),
        ("Multi-intent", [
            Intent(IntentType.COLOR, "button", "red", None, 0.90),
            Intent(IntentType.RESIZE, "button", None, {"height": 60}, 0.85)
        ]),
    ]
    
    blueprint = {
        "tokens": {"primary_color": "#3B82F6"},
        "components": [
            {
                "id": "btn_1",
                "type": "button",
                "bbox": [10, 10, 100, 44],
                "visual": {"color": "#000000", "height": 44}
            }
        ]
    }
    
    patches = [JSONPatch(op="replace", path="/components/0/visual/color", value="#E63946")]
    
    for name, intents in test_cases:
        report = scorer.score(name, intents, blueprint, blueprint, patches)
        
        assert 0.0 <= report.final_score <= 1.0, \
            f"Score out of range for '{name}': {report.final_score}"
        
        for stage in report.stage_scores:
            assert 0.0 <= stage.score <= 1.0, \
                f"Stage score out of range for '{name}' stage {stage.stage.value}: {stage.score}"
        
        print(f"  [{name}] Score: {report.final_score:.1%} - VALID RANGE")
    
    print(f"  PASS - All scores in valid range [0.0, 1.0]")
    return True


def test_explanation_generation():
    """Verify explanation text is generated correctly."""
    print("\n[PHASE A TEST 7] Explanation Generation")
    
    scorer = ConfidenceScorer()
    
    intents = [
        Intent(
            type=IntentType.COLOR,
            target="button",
            value="red",
            params=None,
            confidence=0.95
        )
    ]
    
    blueprint = {
        "tokens": {"primary_color": "#3B82F6"},
        "components": [
            {
                "id": "btn_1",
                "type": "button",
                "bbox": [10, 10, 100, 44],
                "visual": {"color": "#000000"}
            }
        ]
    }
    
    patches = [JSONPatch(op="replace", path="/components/0/visual/color", value="#E63946")]
    
    report = scorer.score("Change button to red", intents, blueprint, blueprint, patches)
    
    # Verify explanation has required parts
    assert "Confidence Score:" in report.explanation, "Missing confidence score in explanation"
    assert "Pipeline Stage Analysis:" in report.explanation, "Missing stage analysis in explanation"
    assert "Assessment:" in report.explanation, "Missing assessment in explanation"
    
    print(f"  PASS - Explanation properly formatted")
    print(f"  Sample:\n{report.explanation[:200]}...")
    return True


if __name__ == "__main__":
    print("\n" + "="*60)
    print("PHASE A: CONFIDENCE SCORER UNIT TESTS")
    print("="*60)
    
    tests = [
        test_deterministic_scoring,
        test_single_intent_boost,
        test_ambiguous_targeting_penalty,
        test_stage_weights,
        test_input_immutability,
        test_confidence_range,
        test_explanation_generation,
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
    
    print("\n" + "="*60)
    print(f"RESULTS: {passed} passed, {failed} failed")
    print("="*60)
    
    if failed == 0:
        print("PHASE A TESTS: ALL PASS - Confidence scorer production-ready")
    else:
        print(f"PHASE A TESTS: {failed} failing - needs fixes")
    
    sys.exit(0 if failed == 0 else 1)
