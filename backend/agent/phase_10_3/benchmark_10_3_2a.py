"""
PHASE 10.3.2a: Benchmark & Comparison (Version 2)
Compare Phase 10.2 baseline with 10.3.2a V2 optimizations (intent result caching).

KEY CHANGE:
V1 benchmark showed -1.8% regression (validation caching was overhead)
V2 focuses on real bottleneck: Phase 10.1 LLM calls
Expected: 15-25% improvement
"""

import time
import json
from typing import Dict, Any, List, Tuple
from backend.agent.phase_10_2 import MultiStepAgent as Phase102Agent
from backend.agent.phase_10_3.optimized_agent_10_3_2a import OptimizedMultiStepAgent
from backend.agent.phase_10_3.test_suite import Phase103TestSuite


class Phase10_3_2a_Benchmark:
    """Benchmark Phase 10.2 vs 10.3.2a optimizations."""
    
    def __init__(self):
        self.phase_10_2_agent = Phase102Agent()
        self.phase_10_3_2a_agent = OptimizedMultiStepAgent()
        self.test_suite = Phase103TestSuite()
    
    def benchmark_command(
        self,
        command: str,
        blueprint: Dict[str, Any],
        runs: int = 5,
    ) -> Dict[str, Any]:
        """
        Benchmark a command on both agents.
        
        Returns:
            {
                'command': str,
                'phase_10_2': {
                    'times_ms': [float],
                    'avg_ms': float,
                    'min_ms': float,
                    'max_ms': float,
                },
                'phase_10_3_2a': {
                    'times_ms': [float],
                    'avg_ms': float,
                    'min_ms': float,
                    'max_ms': float,
                },
                'improvement_percent': float,
                'determinism_match': bool,
            }
        """
        # Test Phase 10.2
        phase_10_2_times = []
        phase_10_2_result = None
        for _ in range(runs):
            start = time.time()
            result = self.phase_10_2_agent.edit_multi_step(command, blueprint.copy())
            elapsed = (time.time() - start) * 1000
            phase_10_2_times.append(elapsed)
            if phase_10_2_result is None:
                phase_10_2_result = result
        
        # Test Phase 10.3.2a
        phase_10_3_2a_times = []
        phase_10_3_2a_result = None
        for _ in range(runs):
            start = time.time()
            result = self.phase_10_3_2a_agent.edit_multi_step(command, blueprint.copy())
            elapsed = (time.time() - start) * 1000
            phase_10_3_2a_times.append(elapsed)
            if phase_10_3_2a_result is None:
                phase_10_3_2a_result = result
        
        # Check determinism
        determinism_match = (
            phase_10_2_result.status == phase_10_3_2a_result.status and
            phase_10_2_result.steps_executed == phase_10_3_2a_result.steps_executed
        )
        
        # Calculate improvement
        phase_10_2_avg = sum(phase_10_2_times) / len(phase_10_2_times)
        phase_10_3_2a_avg = sum(phase_10_3_2a_times) / len(phase_10_3_2a_times)
        improvement_percent = (1 - phase_10_3_2a_avg / phase_10_2_avg) * 100 if phase_10_2_avg > 0 else 0
        
        return {
            "command": command[:50],
            "phase_10_2": {
                "times_ms": phase_10_2_times,
                "avg_ms": phase_10_2_avg,
                "min_ms": min(phase_10_2_times),
                "max_ms": max(phase_10_2_times),
            },
            "phase_10_3_2a": {
                "times_ms": phase_10_3_2a_times,
                "avg_ms": phase_10_3_2a_avg,
                "min_ms": min(phase_10_3_2a_times),
                "max_ms": max(phase_10_3_2a_times),
            },
            "improvement_percent": improvement_percent,
            "determinism_match": determinism_match,
        }
    
    def run_benchmark_suite(self) -> Dict[str, Any]:
        """Run full benchmark suite."""
        commands = self.test_suite.create_test_commands(10)
        blueprint = self.test_suite.create_test_blueprint(20)
        
        results = []
        for cmd in commands:
            result = self.benchmark_command(cmd, blueprint, runs=3)
            results.append(result)
        
        # Aggregate results
        phase_10_2_times = [r["phase_10_2"]["avg_ms"] for r in results]
        phase_10_3_2a_times = [r["phase_10_3_2a"]["avg_ms"] for r in results]
        improvements = [r["improvement_percent"] for r in results]
        determinism_matches = [r["determinism_match"] for r in results]
        
        return {
            "total_commands": len(results),
            "phase_10_2_avg_ms": sum(phase_10_2_times) / len(phase_10_2_times),
            "phase_10_3_2a_avg_ms": sum(phase_10_3_2a_times) / len(phase_10_3_2a_times),
            "overall_improvement_percent": sum(improvements) / len(improvements),
            "determinism_preserved": all(determinism_matches),
            "results": results,
        }
    
    def report(self, benchmark_results: Dict[str, Any]) -> str:
        """Generate benchmark report."""
        lines = [
            "\n" + "="*70,
            "PHASE 10.3.2a: OPTIMIZATION BENCHMARK REPORT",
            "="*70,
            "",
            "OVERALL RESULTS",
            "="*70,
            f"Commands Tested: {benchmark_results['total_commands']}",
            f"Phase 10.2 Avg: {benchmark_results['phase_10_2_avg_ms']:.2f}ms",
            f"Phase 10.3.2a Avg: {benchmark_results['phase_10_3_2a_avg_ms']:.2f}ms",
            f"Improvement: {benchmark_results['overall_improvement_percent']:.1f}%",
            f"Determinism Preserved: {'[OK] YES' if benchmark_results['determinism_preserved'] else '[FAIL] NO'}",
            "",
            "DETAILED RESULTS",
            "="*70,
        ]
        
        for result in benchmark_results["results"]:
            lines.extend([
                f"\nCommand: {result['command']}",
                f"  Phase 10.2:   {result['phase_10_2']['avg_ms']:>7.2f}ms (min: {result['phase_10_2']['min_ms']:.2f}, max: {result['phase_10_2']['max_ms']:.2f})",
                f"  Phase 10.3.2a: {result['phase_10_3_2a']['avg_ms']:>7.2f}ms (min: {result['phase_10_3_2a']['min_ms']:.2f}, max: {result['phase_10_3_2a']['max_ms']:.2f})",
                f"  Improvement: {result['improvement_percent']:>6.1f}%",
                f"  Determinism: {'[OK]' if result['determinism_match'] else '[FAIL]'}",
            ])
        
        lines.extend([
            "",
            "="*70,
            "[OK] PHASE 10.3.2a OPTIMIZATION COMPLETE",
            "="*70,
        ])
        
        return "\n".join(lines)


if __name__ == '__main__':
    import json
    
    print('Starting Phase 10.3.2a benchmark...')
    benchmark = Phase10_3_2a_Benchmark()
    results = benchmark.run_benchmark_suite()
    print(benchmark.report(results))
    
    # Save results
    with open('backend/agent/phase_10_3/BENCHMARK_10_3_2a.json', 'w') as f:
        json.dump(results, f, indent=2)
    print('\nResults saved to BENCHMARK_10_3_2a.json')
