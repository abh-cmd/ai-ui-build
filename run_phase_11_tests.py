#!/usr/bin/env python3
"""
Quick Phase 11 test runner to verify Phase A integration.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))

from backend.tests.phase_11.test_agentic_core import TestPhase11

if __name__ == "__main__":
    print("\n" + "="*80)
    print("RUNNING PHASE 11 TESTS TO VERIFY PHASE A INTEGRATION")
    print("="*80)
    
    suite = TestPhase11()
    suite.run_all()
    
    print("\n" + "="*80)
    if suite.failed == 0:
        print(f"SUCCESS: All Phase 11 tests pass ({suite.passed}/{suite.total})")
        print("Phase A integration is SAFE - no breaking changes")
    else:
        print(f"FAILURE: {suite.failed}/{suite.total} tests failed")
        print("Phase A may have introduced regressions")
    print("="*80)
    
    sys.exit(0 if suite.failed == 0 else 1)
