"""
PHASE 10.1 STRESS TEST
Focused tests on known working commands with different blueprints
"""

from backend.agent import DesignEditAgent
import json

# Simpler blueprint that matches test pattern
simple_blueprint = {
    "screen_id": "app",
    "tokens": {
        "colors": {
            "white": "#FFFFFF",
            "black": "#000000",
            "blue": "#0000FF",
            "red": "#FF0000",
            "green": "#00FF00",
        }
    },
    "components": [
        {
            "id": "header",
            "type": "header",
            "text": "My App",
            "role": "hero",
            "bbox": [0, 0, 480, 50],
            "visual": {"color": "#000000", "height": 50}
        },
        {
            "id": "button_a",
            "type": "button",
            "text": "Action A",
            "role": "cta",
            "bbox": [10, 70, 220, 50],
            "visual": {"color": "#FFFFFF", "bg_color": "#0000FF", "height": 50}
        },
        {
            "id": "button_b",
            "type": "button",
            "text": "Action B",
            "role": "secondary",
            "bbox": [250, 70, 220, 50],
            "visual": {"color": "#000000", "bg_color": "#FFFFFF", "height": 50}
        },
        {
            "id": "content",
            "type": "text",
            "text": "Main Content",
            "role": "content",
            "bbox": [10, 140, 460, 150],
            "visual": {"color": "#333333", "height": 150}
        },
    ]
}

def test_rapid_edits():
    """Test rapid sequential edits"""
    print("\n" + "="*80)
    print("TEST: RAPID SEQUENTIAL EDITS")
    print("="*80)
    
    import copy
    agent = DesignEditAgent()
    working_bp = copy.deepcopy(simple_blueprint)
    
    commands = [
        "change header color to blue",
        "make button_a bigger",
        "change button_a text to Click Me",
        "change header color to green",
        "make content bigger",
        "make button_b bigger",
    ]
    
    successful = 0
    for i, cmd in enumerate(commands, 1):
        result = agent.edit(cmd, working_bp)
        status = "PASS" if result.success else "FAIL"
        print(f"[{status}] Edit {i:2d}: {cmd}")
        
        if result.success:
            working_bp = result.patched_blueprint
            successful += 1
    
    print(f"\nRapid Edits: {successful}/{len(commands)} PASS")
    return successful == len(commands)


def test_alternating_components():
    """Test editing different components alternately"""
    print("\n" + "="*80)
    print("TEST: ALTERNATING COMPONENT EDITS")
    print("="*80)
    
    import copy
    agent = DesignEditAgent()
    working_bp = copy.deepcopy(simple_blueprint)
    
    # Alternate between header, button_a, content
    commands = [
        "change header color to red",
        "make button_a bigger",
        "change content text to Updated",
        "change header color to white",
        "make button_a bigger",
    ]
    
    successful = 0
    for i, cmd in enumerate(commands, 1):
        result = agent.edit(cmd, working_bp)
        status = "PASS" if result.success else "FAIL"
        print(f"[{status}] {cmd}")
        
        if result.success:
            working_bp = result.patched_blueprint
            successful += 1
    
    print(f"\nAlternating Edits: {successful}/{len(commands)} PASS")
    return successful == len(commands)


def test_revert_sequence():
    """Test making and reverting changes"""
    print("\n" + "="*80)
    print("TEST: REVERT SEQUENCE")
    print("="*80)
    
    import copy
    agent = DesignEditAgent()
    bp = copy.deepcopy(simple_blueprint)
    result1 = agent.edit("change header color to red", working_bp)
    if result1.success:
        working_bp = result1.patched_blueprint
    
    result2 = agent.edit("make button_a bigger", working_bp)
    if result2.success:
        working_bp = result2.patched_blueprint
    
    # Revert changes
    result3 = agent.edit("change header color to black", working_bp)
    if result3.success:
        working_bp = result3.patched_blueprint
    
    result4 = agent.edit("make button_a smaller", working_bp)
    if result4.success:
        working_bp = result4.patched_blueprint
    
    # Check if we're back to original (approximately)
    final_header_color = working_bp['components'][0]['visual']['color']
    final_button_height = working_bp['components'][1]['visual']['height']
    
    color_reverted = final_header_color == orig_header_color
    
    print(f"[{'PASS' if color_reverted else 'FAIL'}] Header color reverted: {orig_header_color} -> {final_header_color}")
    print(f"Button height: {orig_button_height} -> {final_button_height}")
    
    return color_reverted


def test_all_modifications():
    """Test all types of modifications in sequence"""
    print("\n" + "="*80)
    print("TEST: ALL MODIFICATION TYPES")
    print("="*80)
    
    agent = DesignEditAgent()
    working_bp = simple_blueprint
    
    tests = [
        ("change header color to red", "color change"),
        ("make button_a bigger", "resize"),
        ("change button_a text to New Action", "text edit"),
        ("make content bold", "style change"),
    ]
    
    successful = 0
    for cmd, mod_type in tests:
        result = agent.edit(cmd, working_bp)
        status = "PASS" if result.success else "FAIL"
        print(f"[{status}] {mod_type:20s}: {cmd}")
        
        if result.success:
            working_bp = result.patched_blueprint
            successful += 1
    
    print(f"\nModification Types: {successful}/{len(tests)} PASS")
    return successful == len(tests)


def test_reasoning_capture():
    """Test that reasoning is captured for all edits"""
    print("\n" + "="*80)
    print("TEST: REASONING CAPTURE")
    print("="*80)
    
    agent = DesignEditAgent()
    
    commands = [
        "change header color to blue",
        "make button_a bigger",
        "change button_a text to Click",
    ]
    
    all_ok = True
    for cmd in commands:
        result = agent.edit(cmd, simple_blueprint)
        
        if result.success:
            has_reasoning = len(result.reasoning) > 5
            has_steps = any('STEP' in line for line in result.reasoning)
            
            status = "PASS" if (has_reasoning and has_steps) else "FAIL"
            print(f"[{status}] {cmd}")
            print(f"      Reasoning lines: {len(result.reasoning)}, Has STEPS: {has_steps}")
            
            if not (has_reasoning and has_steps):
                all_ok = False
        else:
            print(f"[FAIL] {cmd} - edit failed")
            all_ok = False
    
    return all_ok


def test_safety_consistency():
    """Test that safety checks are consistent"""
    print("\n" + "="*80)
    print("TEST: SAFETY CONSISTENCY")
    print("="*80)
    
    agent = DesignEditAgent()
    
    # Run same command multiple times
    command = "change header color to red"
    
    results = []
    for i in range(3):
        result = agent.edit(command, simple_blueprint)
        results.append(result)
    
    # Check consistency
    all_safe = all(r.safe for r in results)
    all_success = all(r.success for r in results)
    same_summary = all(r.summary == results[0].summary for r in results)
    
    print(f"[{'PASS' if all_safe else 'FAIL'}] All results safe: {[r.safe for r in results]}")
    print(f"[{'PASS' if all_success else 'FAIL'}] All results success: {[r.success for r in results]}")
    print(f"[{'PASS' if same_summary else 'FAIL'}] Consistent summaries")
    
    return all_safe and all_success and same_summary


def test_blueprint_integrity():
    """Test that blueprint structure is never corrupted"""
    print("\n" + "="*80)
    print("TEST: BLUEPRINT INTEGRITY")
    print("="*80)
    
    agent = DesignEditAgent()
    working_bp = simple_blueprint
    
    commands = [
        "change header color to red",
        "make button_a bigger",
        "change content text to New",
        "make button_b bigger",
    ]
    
    for cmd in commands:
        result = agent.edit(cmd, working_bp)
        if result.success:
            # Check structure
            new_bp = result.patched_blueprint
            has_screen_id = 'screen_id' in new_bp
            has_components = 'components' in new_bp
            correct_count = len(new_bp['components']) == 4
            all_have_id = all('id' in c for c in new_bp['components'])
            
            if not (has_screen_id and has_components and correct_count and all_have_id):
                print(f"[FAIL] Structure corrupted in: {cmd}")
                return False
            
            working_bp = new_bp
    
    print(f"[PASS] All edits maintained blueprint integrity")
    return True


if __name__ == "__main__":
    print("\n" + "="*80)
    print("PHASE 10.1 STRESS TESTING")
    print("="*80)
    
    tests = {
        "Rapid Sequential Edits": test_rapid_edits(),
        "Alternating Components": test_alternating_components(),
        "Revert Sequence": test_revert_sequence(),
        "All Modification Types": test_all_modifications(),
        "Reasoning Capture": test_reasoning_capture(),
        "Safety Consistency": test_safety_consistency(),
        "Blueprint Integrity": test_blueprint_integrity(),
    }
    
    print("\n" + "="*80)
    print("STRESS TEST RESULTS")
    print("="*80)
    
    passed = sum(1 for v in tests.values() if v)
    total = len(tests)
    
    for test_name, result in tests.items():
        status = "PASS" if result else "FAIL"
        print(f"[{status}] {test_name}")
    
    print(f"\nTOTAL: {passed}/{total} STRESS TESTS PASSED")
    
    if passed == total:
        print("\nPHASE 10.1 AGENT PASSES HEAVY STRESS TESTING")
    else:
        print(f"\n{total - passed} tests failed")
