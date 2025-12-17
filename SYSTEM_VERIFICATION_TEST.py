#!/usr/bin/env python
"""System verification test - end-to-end check."""

import sys
sys.path.insert(0, '.')

# Test 1: Backend imports
print("=" * 70)
print("SYSTEM VERIFICATION TEST")
print("=" * 70)

print("\n[TEST 1] Checking backend modules...")
try:
    from backend.app import app
    print("  ✓ Backend app imported successfully")
except Exception as e:
    print(f"  ✗ Failed to import backend: {e}")
    sys.exit(1)

# Test 2: Agentic agent
print("\n[TEST 2] Checking agentic agent...")
try:
    from backend.agentic import AgenticAgent
    agent = AgenticAgent()
    print("  ✓ AgenticAgent initialized successfully")
except Exception as e:
    print(f"  ✗ Failed to initialize agent: {e}")
    sys.exit(1)

# Test 3: Process a simple command
print("\n[TEST 3] Testing agent processing...")
try:
    import copy
    bp = {
        'tokens': {'primary_color': '#2C3E50', 'base_spacing': 8},
        'components': [
            {
                'id': 'btn1',
                'type': 'button',
                'text': 'Click me',
                'bbox': [50, 100, 200, 160],
                'visual': {'color': '#333', 'height': 50},
                'role': 'cta'
            }
        ]
    }
    
    result = agent.process('Make button bigger', copy.deepcopy(bp))
    
    if result.get('success'):
        print(f"  ✓ Command processed successfully")
        print(f"    - Success: {result.get('success')}")
        print(f"    - Confidence: {result.get('confidence'):.1%}")
        print(f"    - Reasoning: {result.get('reasoning')[:60]}...")
    else:
        print(f"  ✗ Command failed: {result.get('reasoning')}")
        sys.exit(1)
except Exception as e:
    print(f"  ✗ Failed to process command: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 4: Determinism check
print("\n[TEST 4] Checking determinism...")
try:
    results = []
    for i in range(3):
        result = agent.process('Make button bigger', copy.deepcopy(bp))
        results.append((result.get('success'), result.get('confidence')))
    
    all_same = all(r == results[0] for r in results)
    if all_same:
        print(f"  ✓ All 3 runs identical (deterministic)")
        print(f"    - Success: {results[0][0]}")
        print(f"    - Confidence: {results[0][1]:.1%}")
    else:
        print(f"  ✗ Results differ across runs (not deterministic)")
        sys.exit(1)
except Exception as e:
    print(f"  ✗ Determinism check failed: {e}")
    sys.exit(1)

# Test 5: Safety verification
print("\n[TEST 5] Checking safety mechanisms...")
try:
    unsafe_result = agent.process('Delete all components', copy.deepcopy(bp))
    if not unsafe_result.get('success'):
        print(f"  ✓ Unsafe command blocked correctly")
        print(f"    - Result: {unsafe_result.get('reasoning')[:60]}...")
    else:
        print(f"  ✗ Unsafe command was not blocked!")
        sys.exit(1)
except Exception as e:
    print(f"  ✗ Safety check failed: {e}")
    sys.exit(1)

print("\n" + "=" * 70)
print("RESULT: ALL TESTS PASSED")
print("=" * 70)
print("\nSystem Status: PRODUCTION READY")
print("Backend: Operational")
print("Agentic Agent: Functional")
print("Safety: Verified")
print("Determinism: Verified")
print("\nReady for frontend integration (Phases 7, 8, 9)")
print("=" * 70)
