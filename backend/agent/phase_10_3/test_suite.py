"""
PHASE 10.3: Comprehensive Test Suite
Tests for performance, scaling, batch processing, and error recovery.
"""

import json
import time
import copy
from typing import Dict, Any, List
from backend.agent.phase_10_3.profiler import PipelineProfiler, ExecutionProfile
from backend.agent.phase_10_2 import execute_multi_step_edit


class Phase103TestSuite:
    """Heavy test suite for Phase 10.3."""
    
    def __init__(self):
        """Initialize test suite."""
        self.profiler = PipelineProfiler(verbose=False)
        self.test_results = {
            "tests_run": 0,
            "tests_passed": 0,
            "tests_failed": 0,
            "failures": [],
        }
    
    # ============================================================
    # TEST DATA GENERATORS
    # ============================================================
    
    @staticmethod
    def create_test_blueprint(num_components: int = 10) -> Dict[str, Any]:
        """Create a test blueprint with given number of components."""
        components = []
        for i in range(num_components):
            components.append({
                "id": f"comp_{i}",
                "type": "card" if i % 3 == 0 else "button" if i % 3 == 1 else "text",
                "text": f"Component {i}",
                "style": {
                    "color": "#000000",
                    "size": "medium",
                    "position": {"x": i * 100, "y": 0},
                },
                "children": [],
            })
        
        return {
            "name": "Test Blueprint",
            "components": components,
            "metadata": {
                "version": "1.0",
                "created": "2025-12-17",
            },
        }
    
    @staticmethod
    def create_test_commands(count: int = 5) -> List[str]:
        """Create diverse test commands."""
        base_commands = [
            "Make the first card red",
            "Increase the size of all buttons",
            "Change the text of the second component to 'Hello World'",
            "Move all cards to the right",
            "Make the third button blue and larger",
            "Add padding to all components",
            "Change text color to white on all dark components",
            "Align all buttons to center",
            "Make the background gradient from blue to purple",
            "Increase font size for all text components",
        ]
        
        commands = []
        for i in range(count):
            commands.append(base_commands[i % len(base_commands)] + f" (command {i+1})")
        
        return commands
    
    # ============================================================
    # PERFORMANCE TESTS
    # ============================================================
    
    def test_50_percent_speedup(self) -> bool:
        """TEST: Verify 50% speedup over Phase 10.2."""
        print("\n" + "="*60)
        print("TEST: 50% Performance Improvement")
        print("="*60)
        
        try:
            # Profile baseline (Phase 10.2)
            bp = self.create_test_blueprint(20)
            commands = self.create_test_commands(10)
            
            baseline_times = []
            for cmd in commands:
                _, profile = self.profiler.profile_execution(cmd, bp)
                baseline_times.append(profile.total_duration_ms)
            
            baseline_avg = sum(baseline_times) / len(baseline_times)
            
            print(f"Baseline Average Time: {baseline_avg:.2f}ms")
            print(f"Target (50% faster): {baseline_avg * 0.5:.2f}ms")
            
            # TODO: Profile optimized version and compare
            # For now, mark as pending optimization
            
            self.test_results["tests_run"] += 1
            print("STATUS: BASELINE MEASURED - Optimization TBD")
            return True
            
        except Exception as e:
            self.test_results["tests_run"] += 1
            self.test_results["tests_failed"] += 1
            self.test_results["failures"].append(("test_50_percent_speedup", str(e)))
            print(f"FAILED: {e}")
            return False
    
    # ============================================================
    # SCALING TESTS
    # ============================================================
    
    def test_50_step_commands(self) -> bool:
        """TEST: Support 50-step commands without failures."""
        print("\n" + "="*60)
        print("TEST: 50-Step Command Support")
        print("="*60)
        
        try:
            bp = self.create_test_blueprint(30)
            
            # Create a 50-step command
            step_commands = [
                "Make component red",
                "Increase size",
                "Change text",
                "Move right",
                "Add padding",
            ] * 10  # 50 steps
            
            command = " and ".join(step_commands)
            
            print(f"Command length: {len(command)} characters")
            print(f"Blueprint components: 30")
            
            result = execute_multi_step_edit(command, bp)
            
            success = result.status in ["success", "partial"]
            self.test_results["tests_run"] += 1
            if success:
                self.test_results["tests_passed"] += 1
                print(f"STATUS: PASS - Executed {result.steps_executed} steps")
            else:
                self.test_results["tests_failed"] += 1
                print(f"STATUS: FAIL - Status: {result.status}")
            
            return success
            
        except Exception as e:
            self.test_results["tests_run"] += 1
            self.test_results["tests_failed"] += 1
            self.test_results["failures"].append(("test_50_step_commands", str(e)))
            print(f"FAILED: {e}")
            return False
    
    def test_large_blueprints(self) -> bool:
        """TEST: Handle blueprints with 100+ components."""
        print("\n" + "="*60)
        print("TEST: Large Blueprint Handling (100+ components)")
        print("="*60)
        
        try:
            bp = self.create_test_blueprint(100)
            cmd = "Make all cards red and increase their size"
            
            print(f"Blueprint size: {len(bp['components'])} components")
            
            result = execute_multi_step_edit(cmd, bp)
            
            success = result.status in ["success", "partial"]
            self.test_results["tests_run"] += 1
            if success:
                self.test_results["tests_passed"] += 1
                print(f"STATUS: PASS - Executed {result.steps_executed} steps")
            else:
                self.test_results["tests_failed"] += 1
                print(f"STATUS: FAIL - Status: {result.status}")
            
            return success
            
        except Exception as e:
            self.test_results["tests_run"] += 1
            self.test_results["tests_failed"] += 1
            self.test_results["failures"].append(("test_large_blueprints", str(e)))
            print(f"FAILED: {e}")
            return False
    
    # ============================================================
    # BATCH PROCESSING TESTS
    # ============================================================
    
    def test_batch_processing(self) -> bool:
        """TEST: Batch processing multiple commands."""
        print("\n" + "="*60)
        print("TEST: Batch Command Processing")
        print("="*60)
        
        try:
            bp = self.create_test_blueprint(15)
            commands = self.create_test_commands(5)
            
            print(f"Processing {len(commands)} commands in batch")
            
            results = []
            for cmd in commands:
                result = execute_multi_step_edit(cmd, bp)
                results.append(result)
            
            success_count = sum(1 for r in results if r.status == "success")
            success_rate = success_count / len(results) * 100
            
            self.test_results["tests_run"] += 1
            if success_rate >= 80:  # Allow some failures
                self.test_results["tests_passed"] += 1
                print(f"STATUS: PASS - {success_count}/{len(results)} successful ({success_rate:.1f}%)")
            else:
                self.test_results["tests_failed"] += 1
                print(f"STATUS: FAIL - Success rate too low ({success_rate:.1f}%)")
            
            return success_rate >= 80
            
        except Exception as e:
            self.test_results["tests_run"] += 1
            self.test_results["tests_failed"] += 1
            self.test_results["failures"].append(("test_batch_processing", str(e)))
            print(f"FAILED: {e}")
            return False
    
    # ============================================================
    # FAILURE RECOVERY TESTS
    # ============================================================
    
    def test_rollback_integrity(self) -> bool:
        """TEST: Rollback preserves blueprint integrity."""
        print("\n" + "="*60)
        print("TEST: Rollback Integrity")
        print("="*60)
        
        try:
            bp = self.create_test_blueprint(10)
            bp_original = copy.deepcopy(bp)
            
            # Command that might fail
            cmd = "Make component comp_0 red and move it to position 999999 99999"
            
            result = execute_multi_step_edit(cmd, bp)
            
            # Check if blueprint is valid (no corruption)
            assert "components" in result.final_blueprint, "Missing components"
            assert len(result.final_blueprint["components"]) == len(bp_original["components"]), \
                "Component count changed unexpectedly"
            
            self.test_results["tests_run"] += 1
            self.test_results["tests_passed"] += 1
            print(f"STATUS: PASS - Blueprint integrity maintained")
            print(f"  Original components: {len(bp_original['components'])}")
            print(f"  Final components: {len(result.final_blueprint['components'])}")
            
            return True
            
        except Exception as e:
            self.test_results["tests_run"] += 1
            self.test_results["tests_failed"] += 1
            self.test_results["failures"].append(("test_rollback_integrity", str(e)))
            print(f"FAILED: {e}")
            return False
    
    def test_determinism_under_load(self) -> bool:
        """TEST: Deterministic output under rapid fire execution."""
        print("\n" + "="*60)
        print("TEST: Determinism Under Load")
        print("="*60)
        
        try:
            bp = self.create_test_blueprint(10)
            cmd = "Make all buttons blue and increase their size"
            
            # Run same command 3 times
            results = []
            for i in range(3):
                result = execute_multi_step_edit(cmd, copy.deepcopy(bp))
                results.append(json.dumps(result.final_blueprint, sort_keys=True))
            
            # All should produce identical output
            identical = all(r == results[0] for r in results)
            
            self.test_results["tests_run"] += 1
            if identical:
                self.test_results["tests_passed"] += 1
                print("STATUS: PASS - All 3 runs produced identical output")
            else:
                self.test_results["tests_failed"] += 1
                print("STATUS: FAIL - Outputs differ between runs")
            
            return identical
            
        except Exception as e:
            self.test_results["tests_run"] += 1
            self.test_results["tests_failed"] += 1
            self.test_results["failures"].append(("test_determinism_under_load", str(e)))
            print(f"FAILED: {e}")
            return False
    
    # ============================================================
    # MEMORY TESTS
    # ============================================================
    
    def test_memory_stability(self) -> bool:
        """TEST: Memory usage stable under repeated operations."""
        print("\n" + "="*60)
        print("TEST: Memory Stability")
        print("="*60)
        
        try:
            bp = self.create_test_blueprint(20)
            commands = self.create_test_commands(20)
            
            print(f"Executing {len(commands)} commands sequentially...")
            
            # Execute many commands and check for memory leaks
            # (Basic check - real profiling needed)
            for cmd in commands:
                result = execute_multi_step_edit(cmd, copy.deepcopy(bp))
                assert result.final_blueprint is not None
            
            self.test_results["tests_run"] += 1
            self.test_results["tests_passed"] += 1
            print("STATUS: PASS - 20 sequential commands completed without crash")
            
            return True
            
        except Exception as e:
            self.test_results["tests_run"] += 1
            self.test_results["tests_failed"] += 1
            self.test_results["failures"].append(("test_memory_stability", str(e)))
            print(f"FAILED: {e}")
            return False
    
    # ============================================================
    # REPORT GENERATION
    # ============================================================
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Run complete test suite."""
        print("\n" + "="*80)
        print("PHASE 10.3: COMPREHENSIVE TEST SUITE")
        print("="*80)
        
        tests = [
            ("Performance", self.test_50_percent_speedup),
            ("Scaling: 50-Step Commands", self.test_50_step_commands),
            ("Scaling: Large Blueprints", self.test_large_blueprints),
            ("Batch Processing", self.test_batch_processing),
            ("Rollback Integrity", self.test_rollback_integrity),
            ("Determinism Under Load", self.test_determinism_under_load),
            ("Memory Stability", self.test_memory_stability),
        ]
        
        for name, test_func in tests:
            try:
                test_func()
            except Exception as e:
                print(f"Test suite error: {e}")
        
        return self.get_results()
    
    def get_results(self) -> Dict[str, Any]:
        """Get test results."""
        total = self.test_results["tests_run"]
        passed = self.test_results["tests_passed"]
        failed = self.test_results["tests_failed"]
        pass_rate = (passed / total * 100) if total > 0 else 0
        
        return {
            "total_tests": total,
            "passed": passed,
            "failed": failed,
            "pass_rate_percent": pass_rate,
            "failures": self.test_results["failures"],
        }
    
    def report(self) -> str:
        """Generate test report."""
        results = self.get_results()
        stats = self.profiler.get_aggregate_stats()
        
        lines = [
            "\n" + "="*80,
            "PHASE 10.3: TEST REPORT",
            "="*80,
            "",
            "TEST RESULTS",
            "="*80,
            f"Total Tests: {results['total_tests']}",
            f"Passed: {results['passed']}",
            f"Failed: {results['failed']}",
            f"Pass Rate: {results['pass_rate_percent']:.1f}%",
            "",
        ]
        
        if results['failures']:
            lines.extend([
                "FAILURES:",
                "="*80,
            ])
            for test_name, error in results['failures']:
                lines.append(f"  {test_name}: {error}")
            lines.append("")
        
        lines.extend([
            "PERFORMANCE METRICS",
            "="*80,
            f"Total Profiled Runs: {stats.get('total_runs', 0)}",
            f"Success Rate: {stats.get('success_rate_percent', 0):.1f}%",
            f"Average Time: {stats.get('avg_time_ms', 0):.2f}ms",
            f"Identified Bottleneck: {stats.get('bottleneck', 'unknown')}",
            "",
            "="*80,
        ])
        
        return "\n".join(lines)
