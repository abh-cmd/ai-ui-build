#!/usr/bin/env python
"""Quick test of 10.3.2a imports and execution."""

import sys
sys.path.insert(0, '.')

print("Testing imports...")
try:
    from backend.agent.phase_10_2 import MultiStepAgent as Phase102Agent
    print("[OK] Phase102Agent imported")
except Exception as e:
    print(f"[FAIL] Phase102Agent: {e}")
    sys.exit(1)

try:
    from backend.agent.phase_10_3.optimized_agent_10_3_2a import OptimizedMultiStepAgent
    print("[OK] OptimizedMultiStepAgent imported")
except Exception as e:
    print(f"[FAIL] OptimizedMultiStepAgent: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

try:
    from backend.agent.phase_10_3.test_suite import Phase103TestSuite
    print("[OK] Phase103TestSuite imported")
except Exception as e:
    print(f"[FAIL] Phase103TestSuite: {e}")
    sys.exit(1)

# Try creating instances
print("\nCreating agent instances...")
try:
    agent_10_2 = Phase102Agent()
    print("[OK] Phase102Agent instance created")
except Exception as e:
    print(f"[FAIL] Phase102Agent instance: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

try:
    agent_10_3_2a = OptimizedMultiStepAgent()
    print("[OK] OptimizedMultiStepAgent instance created")
except Exception as e:
    print(f"[FAIL] OptimizedMultiStepAgent instance: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n[OK] All imports and instances successful!")
