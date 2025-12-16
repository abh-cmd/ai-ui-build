#!/usr/bin/env python3
"""
PHASE 10.3: Test Suite Runner
Execute comprehensive tests and generate reports.
"""

import sys
import json
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from backend.agent.phase_10_3.test_suite import Phase103TestSuite


def main():
    """Run test suite and generate report."""
    print("\n" + "="*80)
    print("PHASE 10.3: COMPREHENSIVE TEST EXECUTION")
    print("="*80)
    
    # Initialize test suite
    suite = Phase103TestSuite()
    
    # Run all tests
    results = suite.run_all_tests()
    
    # Print report
    print(suite.report())
    
    # Save results to file
    report_path = Path(__file__).parent / "TEST_RESULTS.json"
    with open(report_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to: {report_path}")
    
    # Save profiler report
    profiler_report_path = Path(__file__).parent / "PROFILER_REPORT.txt"
    with open(profiler_report_path, "w") as f:
        f.write(suite.profiler.report())
    print(f"Profiler report saved to: {profiler_report_path}")
    
    # Return exit code based on results
    pass_rate = results.get("pass_rate_percent", 0)
    return 0 if pass_rate >= 80 else 1


if __name__ == "__main__":
    sys.exit(main())
