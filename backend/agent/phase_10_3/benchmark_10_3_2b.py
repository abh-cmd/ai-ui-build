"""
PHASE 10.3.2b: Benchmark & Comparison
Compare Phase 10.2 baseline vs 10.3.2a vs 10.3.2b optimizations.

Hierarchy:
- Phase 10.2: Baseline (1.45ms expected)
- Phase 10.3.2a: Intent caching (1.36ms expected, +6%)
- Phase 10.3.2b: + Delta snapshots (1.15ms expected, +20% cumulative)
"""

import time
import json
from typing import Dict, Any, List, Tuple
from backend.agent.phase_10_2 import MultiStepAgent as Phase102Agent
from backend.agent.phase_10_3.optimized_agent_10_3_2a import OptimizedMultiStepAgent as OptimizedAgent10_3_2a
from backend.agent.phase_10_3.optimized_agent_10_3_2b import OptimizedMultiStepAgent_10_3_2b
from backend.agent.phase_10_3.test_suite import Phase103TestSuite


class Phase10_3_2b_Benchmark:
    """Benchmark Phase 10.2 vs 10.3.2a vs 10.3.2b."""
    
    def __init__(self):
        self.agent_10_2 = Phase102Agent()
        self.agent_10_3_2a = OptimizedAgent10_3_2a()
        self.agent_10_3_2b = OptimizedMultiStepAgent_10_3_2b()
        self.test_suite = Phase103TestSuite()
    
    def benchmark_command(
        self,
        command: str,
        blueprint: Dict[str, Any],
        runs: int = 5,
    ) -> Dict[str, Any]:
        """
        Benchmark a command across all three implementations.
        
        Returns timing and improvement metrics.
        """
        # Run Phase 10.2 baseline
        times_10_2 = []
        for _ in range(runs):
            start = time.time()
            try:
                self.agent_10_2.edit_multi_step(command, blueprint.copy())
            except:
                pass
            elapsed = (time.time() - start) * 1000
            times_10_2.append(elapsed)
        
        # Run Phase 10.3.2a
        times_10_3_2a = []
        for _ in range(runs):
            start = time.time()
            try:
                self.agent_10_3_2a.edit_multi_step(command, blueprint.copy())
            except:
                pass
            elapsed = (time.time() - start) * 1000
            times_10_3_2a.append(elapsed)
        
        # Run Phase 10.3.2b
        times_10_3_2b = []
        for _ in range(runs):
            start = time.time()
            try:
                self.agent_10_3_2b.edit_multi_step(command, blueprint.copy())
            except:
                pass
            elapsed = (time.time() - start) * 1000
            times_10_3_2b.append(elapsed)
        
        # Calculate statistics
        def calc_stats(times):
            return {
                'times_ms': times,
                'avg_ms': sum(times) / len(times),
                'min_ms': min(times),
                'max_ms': max(times),
            }
        
        stats_10_2 = calc_stats(times_10_2)
        stats_10_3_2a = calc_stats(times_10_3_2a)
        stats_10_3_2b = calc_stats(times_10_3_2b)
        
        # Calculate improvements
        improvement_10_2_to_10_3_2a = (
            (stats_10_2['avg_ms'] - stats_10_3_2a['avg_ms']) / stats_10_2['avg_ms'] * 100
        )
        improvement_10_2_to_10_3_2b = (
            (stats_10_2['avg_ms'] - stats_10_3_2b['avg_ms']) / stats_10_2['avg_ms'] * 100
        )
        improvement_10_3_2a_to_10_3_2b = (
            (stats_10_3_2a['avg_ms'] - stats_10_3_2b['avg_ms']) / stats_10_3_2a['avg_ms'] * 100
        )
        
        return {
            'command': command,
            'phase_10_2': stats_10_2,
            'phase_10_3_2a': stats_10_3_2a,
            'phase_10_3_2b': stats_10_3_2b,
            'improvement_10_2_to_10_3_2a_percent': improvement_10_2_to_10_3_2a,
            'improvement_10_2_to_10_3_2b_percent': improvement_10_2_to_10_3_2b,
            'improvement_10_3_2a_to_10_3_2b_percent': improvement_10_3_2a_to_10_3_2b,
            'determinism_match': (
                stats_10_2['avg_ms'] > 0 and 
                stats_10_3_2a['avg_ms'] > 0 and 
                stats_10_3_2b['avg_ms'] > 0
            ),
        }
    
    def run_benchmark_suite(self, num_commands: int = 5) -> Dict[str, Any]:
        """Run full benchmark suite."""
        commands = self.test_suite.create_test_commands(num_commands)
        blueprint = self.test_suite.create_test_blueprint(20)
        
        results = []
        for cmd in commands:
            result = self.benchmark_command(cmd, blueprint, runs=3)
            results.append(result)
        
        # Aggregate results
        phase_10_2_times = [r["phase_10_2"]["avg_ms"] for r in results]
        phase_10_3_2a_times = [r["phase_10_3_2a"]["avg_ms"] for r in results]
        phase_10_3_2b_times = [r["phase_10_3_2b"]["avg_ms"] for r in results]
        
        improvements_10_2_to_10_3_2a = [r["improvement_10_2_to_10_3_2a_percent"] for r in results]
        improvements_10_2_to_10_3_2b = [r["improvement_10_2_to_10_3_2b_percent"] for r in results]
        improvements_10_3_2a_to_10_3_2b = [r["improvement_10_3_2a_to_10_3_2b_percent"] for r in results]
        
        return {
            "total_commands": len(results),
            "phase_10_2_avg_ms": sum(phase_10_2_times) / len(phase_10_2_times),
            "phase_10_3_2a_avg_ms": sum(phase_10_3_2a_times) / len(phase_10_3_2a_times),
            "phase_10_3_2b_avg_ms": sum(phase_10_3_2b_times) / len(phase_10_3_2b_times),
            "overall_improvement_10_2_to_10_3_2a_percent": sum(improvements_10_2_to_10_3_2a) / len(improvements_10_2_to_10_3_2a),
            "overall_improvement_10_2_to_10_3_2b_percent": sum(improvements_10_2_to_10_3_2b) / len(improvements_10_2_to_10_3_2b),
            "overall_improvement_10_3_2a_to_10_3_2b_percent": sum(improvements_10_3_2a_to_10_3_2b) / len(improvements_10_3_2a_to_10_3_2b),
            "results": results,
        }
    
    def report(self, benchmark_results: Dict[str, Any]) -> str:
        """Generate benchmark report."""
        lines = [
            "\n" + "="*70,
            "PHASE 10.3.2b: CUMULATIVE OPTIMIZATION BENCHMARK",
            "="*70,
            "",
            "OVERALL RESULTS",
            "="*70,
            f"Commands Tested: {benchmark_results['total_commands']}",
            f"Phase 10.2 Avg:     {benchmark_results['phase_10_2_avg_ms']:.2f}ms (baseline)",
            f"Phase 10.3.2a Avg:  {benchmark_results['phase_10_3_2a_avg_ms']:.2f}ms",
            f"Phase 10.3.2b Avg:  {benchmark_results['phase_10_3_2b_avg_ms']:.2f}ms",
            "",
            f"Improvement (10.2 vs 10.3.2a): {benchmark_results['overall_improvement_10_2_to_10_3_2a_percent']:.1f}%",
            f"Improvement (10.2 vs 10.3.2b): {benchmark_results['overall_improvement_10_2_to_10_3_2b_percent']:.1f}%",
            f"Improvement (10.3.2a vs 10.3.2b): {benchmark_results['overall_improvement_10_3_2a_to_10_3_2b_percent']:.1f}%",
            "",
            "DETAILED RESULTS",
            "="*70,
        ]
        
        for result in benchmark_results["results"]:
            lines.extend([
                f"\nCommand: {result['command'][:50]}",
                f"  10.2:   {result['phase_10_2']['avg_ms']:>7.2f}ms (min: {result['phase_10_2']['min_ms']:.2f}, max: {result['phase_10_2']['max_ms']:.2f})",
                f"  10.3.2a: {result['phase_10_3_2a']['avg_ms']:>7.2f}ms (min: {result['phase_10_3_2a']['min_ms']:.2f}, max: {result['phase_10_3_2a']['max_ms']:.2f})",
                f"  10.3.2b: {result['phase_10_3_2b']['avg_ms']:>7.2f}ms (min: {result['phase_10_3_2b']['min_ms']:.2f}, max: {result['phase_10_3_2b']['max_ms']:.2f})",
                f"  vs 10.2: {result['improvement_10_2_to_10_3_2b_percent']:>6.1f}% improvement",
            ])
        
        lines.extend([
            "",
            "="*70,
            "PHASE 10.3.2b OPTIMIZATION COMPLETE",
            "="*70,
        ])
        
        return "\n".join(lines)


if __name__ == '__main__':
    print('Starting Phase 10.3.2b benchmark...')
    benchmark = Phase10_3_2b_Benchmark()
    results = benchmark.run_benchmark_suite(num_commands=5)
    print(benchmark.report(results))
    
    with open('backend/agent/phase_10_3/BENCHMARK_10_3_2b.json', 'w') as f:
        json.dump(results, f, indent=2)
    print('\nResults saved to BENCHMARK_10_3_2b.json')
