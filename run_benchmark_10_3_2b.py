#!/usr/bin/env python
"""Run Phase 10.3.2b benchmark."""

import sys
sys.path.insert(0, '.')

import time
import json
from backend.agent.phase_10_3.benchmark_10_3_2b import Phase10_3_2b_Benchmark

print("Initializing Phase 10.3.2b benchmark...")
try:
    benchmark = Phase10_3_2b_Benchmark()
    print("[OK] Benchmark initialized")
except Exception as e:
    print(f"[FAIL] Initialization failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\nRunning benchmark suite (this may take 2-3 minutes)...")
try:
    start = time.time()
    results = benchmark.run_benchmark_suite(num_commands=5)
    elapsed = time.time() - start
    print(f"[OK] Benchmark completed in {elapsed:.1f}s")
except Exception as e:
    print(f"[FAIL] Benchmark failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\nGenerating report...")
try:
    report = benchmark.report(results)
    print(report)
except Exception as e:
    print(f"[FAIL] Report generation failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\nSaving results...")
try:
    with open('backend/agent/phase_10_3/BENCHMARK_10_3_2b.json', 'w') as f:
        json.dump(results, f, indent=2)
    print("[OK] Results saved to BENCHMARK_10_3_2b.json")
except Exception as e:
    print(f"[FAIL] Failed to save: {e}")
    sys.exit(1)

print("\n[OK] Phase 10.3.2b Benchmark Complete!")
