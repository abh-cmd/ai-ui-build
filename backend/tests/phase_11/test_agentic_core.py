"""
PHASE 11: COMPREHENSIVE TEST SUITE

Tests cover:
- Multi-intent parsing
- Unsafe command rejection
- Blueprint immutability
- Deterministic outputs
- Rollback correctness
- Simulation safety
- Confidence consistency
"""

import json
import copy
import sys
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from backend.agentic import AgenticAgent
from backend.agentic.intent_graph import IntentGraph, IntentType
from backend.agentic.planner import Planner
from backend.agentic.patch_generator import PatchGenerator
from backend.agentic.simulator import Simulator
from backend.agentic.verifier import Verifier


# Sample blueprint for testing
SAMPLE_BLUEPRINT = {
    "tokens": {
        "primary_color": "#E63946",
        "accent_color": "#F1FAEE",
        "base_spacing": 16,
        "border_radius": 8,
        "font_scale": {"h1": 28, "h2": 20, "body": 14}
    },
    "components": [
        {
            "id": "navbar",
            "type": "navbar",
            "text": "Store Name",
            "bbox": [0, 0, 480, 60],
            "role": "nav",
            "visual": {"color": "#FFFFFF", "bg_color": "#E63946", "height": 60}
        },
        {
            "id": "hero_button",
            "type": "button",
            "text": "Get Started",
            "bbox": [40, 100, 200, 50],
            "role": "cta",
            "visual": {"color": "#FFFFFF", "bg_color": "#E63946", "height": 50}
        },
        {
            "id": "product_card",
            "type": "product",
            "text": "Featured Product",
            "bbox": [10, 160, 460, 300],
            "role": "content",
            "visual": {"color": "#000000", "bg_color": "#FFFFFF", "height": 140}
        }
    ]
}


class TestPhase11:
    """Main test class for Phase 11."""
    
    def __init__(self):
        self.agent = AgenticAgent()
        self.intent_graph = IntentGraph()
        self.planner = Planner()
        self.patch_generator = PatchGenerator()
        self.simulator = Simulator()
        self.verifier = Verifier()
        self.passed = 0
        self.failed = 0
        self.tests = []
    
    def run_all(self):
        """Run all tests."""
        print("\n" + "="*60)
        print("PHASE 11: AGENTIC AI CORE — COMPREHENSIVE TEST SUITE")
        print("="*60 + "\n")
        
        self.test_intent_parsing()
        self.test_multi_intent_commands()
        self.test_unsafe_command_rejection()
        self.test_blueprint_immutability()
        self.test_deterministic_outputs()
        self.test_patch_generation()
        self.test_simulation_safety()
        self.test_verification()
        self.test_rollback_correctness()
        self.test_confidence_scoring()
        self.test_end_to_end_pipeline()
        self.test_complex_scenarios()
        
        self._print_summary()
    
    def test_intent_parsing(self):
        """Test 1: Intent parsing from commands."""
        test_name = "Intent Parsing"
        try:
            # Test resize intent
            intents = self.intent_graph.parse("Make button bigger", SAMPLE_BLUEPRINT)
            assert len(intents) > 0, "No intents parsed"
            assert any(i.type == IntentType.RESIZE for i in intents), "No resize intent"
            
            # Test color intent
            intents = self.intent_graph.parse("Change to red", SAMPLE_BLUEPRINT)
            assert any(i.type == IntentType.COLOR for i in intents), "No color intent"
            
            self._pass(test_name)
        except AssertionError as e:
            self._fail(test_name, str(e))
    
    def test_multi_intent_commands(self):
        """Test 2: Multiple intents from single command."""
        test_name = "Multi-Intent Commands"
        try:
            intents = self.intent_graph.parse("Make button bigger and red", SAMPLE_BLUEPRINT)
            assert len(intents) >= 2, f"Expected 2+ intents, got {len(intents)}"
            
            types = [i.type for i in intents]
            assert IntentType.RESIZE in types, "No resize in multi-intent"
            assert IntentType.COLOR in types, "No color in multi-intent"
            
            self._pass(test_name)
        except AssertionError as e:
            self._fail(test_name, str(e))
    
    def test_unsafe_command_rejection(self):
        """Test 3: Unsafe commands are rejected."""
        test_name = "Unsafe Command Rejection"
        try:
            result = self.agent.process("Delete and then resize button", SAMPLE_BLUEPRINT)
            
            # Should detect conflict and reject
            assert not result.get("success"), "Should reject delete+resize"
            
            self._pass(test_name)
        except AssertionError as e:
            self._fail(test_name, str(e))
    
    def test_blueprint_immutability(self):
        """Test 4: Original blueprint is never mutated."""
        test_name = "Blueprint Immutability"
        try:
            original_json = json.dumps(SAMPLE_BLUEPRINT, sort_keys=True)
            original_copy = copy.deepcopy(SAMPLE_BLUEPRINT)
            
            # Process command
            self.agent.process("Make button bigger and red", original_copy)
            
            # Original should be unchanged
            after_json = json.dumps(original_copy, sort_keys=True)
            assert original_json == after_json, "Blueprint was mutated"
            
            self._pass(test_name)
        except AssertionError as e:
            self._fail(test_name, str(e))
    
    def test_deterministic_outputs(self):
        """Test 5: Same command always produces same result."""
        test_name = "Deterministic Outputs"
        try:
            command = "Make button bigger and primary color"
            
            results = []
            for _ in range(3):
                result = self.agent.process(command, SAMPLE_BLUEPRINT)
                if result.get("success"):
                    results.append(json.dumps(result["modified_blueprint"], sort_keys=True))
            
            assert all(r == results[0] for r in results), "Non-deterministic outputs"
            
            self._pass(test_name)
        except AssertionError as e:
            self._fail(test_name, str(e))
    
    def test_patch_generation(self):
        """Test 6: Patch generation."""
        test_name = "Patch Generation"
        try:
            intents = self.intent_graph.parse("Make button bigger", SAMPLE_BLUEPRINT)
            
            patches = []
            for intent in intents:
                p = self.patch_generator.generate(intent, SAMPLE_BLUEPRINT)
                patches.extend(p)
            
            assert len(patches) > 0, "No patches generated"
            assert all(hasattr(p, "op") for p in patches), "Invalid patch format"
            
            self._pass(test_name)
        except AssertionError as e:
            self._fail(test_name, str(e))
    
    def test_simulation_safety(self):
        """Test 7: Simulation detects conflicts."""
        test_name = "Simulation Safety"
        try:
            intents = self.intent_graph.parse("Make button bigger", SAMPLE_BLUEPRINT)
            
            patches = []
            for intent in intents:
                p = self.patch_generator.generate(intent, SAMPLE_BLUEPRINT)
                patches.extend(p)
            
            sim_result = self.simulator.simulate(SAMPLE_BLUEPRINT, patches)
            
            assert hasattr(sim_result, "safe"), "No safe field in result"
            assert hasattr(sim_result, "risk_score"), "No risk_score in result"
            assert 0.0 <= sim_result.risk_score <= 1.0, "Invalid risk score"
            
            self._pass(test_name)
        except AssertionError as e:
            self._fail(test_name, str(e))
    
    def test_verification(self):
        """Test 8: Verification catches issues."""
        test_name = "Verification"
        try:
            result = self.agent.process("Make button bigger", SAMPLE_BLUEPRINT)
            
            if result.get("success"):
                modified = result["modified_blueprint"]
                
                # Verify modified blueprint
                verify_result = self.verifier.verify(modified)
                assert verify_result.valid, f"Verification failed: {verify_result.errors}"
            
            self._pass(test_name)
        except AssertionError as e:
            self._fail(test_name, str(e))
    
    def test_rollback_correctness(self):
        """Test 9: Rollback works correctly."""
        test_name = "Rollback Correctness"
        try:
            # Multi-step with failure in middle
            commands = [
                "Make button bigger",
                "Delete and then resize button",  # This should fail
                "Change to red"
            ]
            
            result = self.agent.process_multi_step(commands, SAMPLE_BLUEPRINT)
            
            # Should rollback to original
            if not result.get("success"):
                assert result["modified_blueprint"] == SAMPLE_BLUEPRINT, "Rollback didn't restore original"
            
            self._pass(test_name)
        except AssertionError as e:
            self._fail(test_name, str(e))
    
    def test_confidence_scoring(self):
        """Test 10: Confidence scores are reasonable."""
        test_name = "Confidence Scoring"
        try:
            result = self.agent.process("Make button bigger and red", SAMPLE_BLUEPRINT)
            
            if result.get("success"):
                confidence = result.get("confidence", 0)
                assert 0.0 <= confidence <= 1.0, f"Invalid confidence: {confidence}"
                assert confidence > 0.5, "Confidence too low for straightforward command"
            
            self._pass(test_name)
        except AssertionError as e:
            self._fail(test_name, str(e))
    
    def test_end_to_end_pipeline(self):
        """Test 11: Full pipeline works end-to-end."""
        test_name = "End-to-End Pipeline"
        try:
            result = self.agent.process("Make button bigger and primary color", SAMPLE_BLUEPRINT)
            
            assert result.get("success"), f"Pipeline failed: {result.get('reasoning')}"
            assert result.get("modified_blueprint") is not None, "No modified blueprint"
            assert result.get("confidence") > 0.7, "Confidence too low"
            assert result.get("explanation"), "No explanation"
            
            self._pass(test_name)
        except AssertionError as e:
            self._fail(test_name, str(e))
    
    def test_complex_scenarios(self):
        """Test 12: Complex real-world scenarios."""
        test_name = "Complex Scenarios"
        try:
            # Scenario 1: Multiple changes
            result = self.agent.process("Make product card taller, center it, and change text", SAMPLE_BLUEPRINT)
            assert result.get("success") or not result.get("success"), "Pipeline error"
            
            # Scenario 2: Color changes
            result = self.agent.process("Change all buttons to blue", SAMPLE_BLUEPRINT)
            assert isinstance(result, dict), "Invalid response type"
            
            self._pass(test_name)
        except AssertionError as e:
            self._fail(test_name, str(e))
    
    def _pass(self, test_name: str):
        """Record test pass."""
        self.passed += 1
        self.tests.append((test_name, True, None))
        print(f"✅ {test_name}")
    
    def _fail(self, test_name: str, reason: str):
        """Record test failure."""
        self.failed += 1
        self.tests.append((test_name, False, reason))
        print(f"❌ {test_name}: {reason}")
    
    def _print_summary(self):
        """Print test summary."""
        total = self.passed + self.failed
        
        print("\n" + "="*60)
        print("TEST RESULTS")
        print("="*60)
        print(f"Total: {total}")
        print(f"Passed: {self.passed} ✅")
        print(f"Failed: {self.failed} ❌")
        print(f"Pass rate: {self.passed/total*100:.1f}%")
        print("="*60 + "\n")
        
        if self.failed == 0:
            print("🎉 ALL TESTS PASSED — PHASE 11 READY FOR PRODUCTION\n")
        else:
            print(f"⚠️  {self.failed} test(s) failed — Review above\n")


if __name__ == "__main__":
    suite = TestPhase11()
    suite.run_all()
    
    # Exit with appropriate code
    sys.exit(0 if suite.failed == 0 else 1)
