"""
PHASE 10.1 ADVANCED EDGE CASE TESTING
Testing complex scenarios and boundary conditions
"""

from backend.agent import run_agent, DesignEditAgent
import json

# Complex blueprint with more components
complex_blueprint = {
    "screen_id": "dashboard",
    "tokens": {
        "colors": {
            "white": "#FFFFFF",
            "black": "#000000",
            "blue": "#0000FF",
            "red": "#FF0000",
            "green": "#00FF00",
            "gray": "#808080",
        }
    },
    "components": [
        {"id": "nav", "type": "header", "text": "Navigation", "role": "nav", "bbox": [0, 0, 480, 40], "visual": {"color": "#000000", "bg_color": "#FFFFFF", "height": 40}},
        {"id": "hero", "type": "text", "text": "Welcome Back", "role": "hero", "bbox": [10, 50, 460, 60], "visual": {"color": "#0000FF", "height": 60, "font_weight": "bold"}},
        {"id": "cta1", "type": "button", "text": "Start Now", "role": "cta", "bbox": [10, 130, 220, 50], "visual": {"color": "#FFFFFF", "bg_color": "#0000FF", "height": 50}},
        {"id": "cta2", "type": "button", "text": "Learn More", "role": "cta", "bbox": [240, 130, 220, 50], "visual": {"color": "#FFFFFF", "bg_color": "#00FF00", "height": 50}},
        {"id": "content", "type": "text", "text": "This is content", "role": "content", "bbox": [10, 200, 460, 200], "visual": {"color": "#000000", "height": 200}},
        {"id": "footer", "type": "footer", "text": "Footer", "role": "footer", "bbox": [0, 430, 480, 50], "visual": {"color": "#FFFFFF", "bg_color": "#000000", "height": 50}},
    ]
}

def test_multiple_same_type():
    """Test targeting multiple buttons correctly"""
    print("\n" + "="*80)
    print("TEST: MULTIPLE COMPONENTS OF SAME TYPE")
    print("="*80)
    
    agent = DesignEditAgent()
    
    # First CTA should be targeted by "first" or "start"
    result = agent.edit("make start now button bigger", complex_blueprint)
    
    if result.success:
        cta1 = result.patched_blueprint['components'][2]
        cta2 = result.patched_blueprint['components'][3]
        
        changed = cta1['visual']['height'] > 50
        other_unchanged = cta2['visual']['height'] == 50
        
        print(f"[{'PASS' if changed else 'FAIL'}] CTA1 resized: {cta1['visual']['height']}px")
        print(f"[{'PASS' if other_unchanged else 'FAIL'}] CTA2 unchanged: {cta2['visual']['height']}px")
        return changed and other_unchanged
    
    return False


def test_large_resize():
    """Test resizing within constraints"""
    print("\n" + "="*80)
    print("TEST: LARGE RESIZE OPERATION")
    print("="*80)
    
    agent = DesignEditAgent()
    
    # Try to make content area much bigger
    result = agent.edit("make content much bigger", complex_blueprint)
    
    if result.success:
        content = result.patched_blueprint['components'][4]
        original_height = 200
        new_height = content['visual']['height']
        increased = new_height > original_height
        
        print(f"[{'PASS' if increased else 'FAIL'}] Content resized: {original_height}px -> {new_height}px")
        print(f"      Safe: {result.safe}")
        return increased and result.safe
    
    print("[FAIL] Resize operation failed")
    return False


def test_color_normalization():
    """Test various color name variations"""
    print("\n" + "="*80)
    print("TEST: COLOR NORMALIZATION")
    print("="*80)
    
    agent = DesignEditAgent()
    
    color_tests = [
        ("change hero color to white", "#FFFFFF", "white to hex"),
        ("change footer color to black", "#000000", "black to hex"),
        ("change cta1 color to blue", "#0000FF", "blue to hex"),
    ]
    
    passed = 0
    
    for command, expected_color, desc in color_tests:
        result = agent.edit(command, complex_blueprint)
        
        if result.success:
            # Find the affected component
            found = False
            for comp in result.patched_blueprint['components']:
                if 'color' in comp['visual'] and comp['visual']['color'] == expected_color:
                    found = True
                    break
            
            status = "PASS" if found else "FAIL"
            print(f"[{status}] {desc}: {command}")
            if found:
                passed += 1
        else:
            print(f"[FAIL] {desc}: {command}")
    
    print(f"\nColor Normalization: {passed}/{len(color_tests)} PASS")
    return passed == len(color_tests)


def test_sequential_same_component():
    """Test multiple edits to same component"""
    print("\n" + "="*80)
    print("TEST: SEQUENTIAL EDITS TO SAME COMPONENT")
    print("="*80)
    
    agent = DesignEditAgent()
    working_bp = complex_blueprint
    
    edits = [
        "change hero color to red",
        "make hero bigger",
        "change hero text to Welcome Home",
    ]
    
    print(f"Applying {len(edits)} edits to hero component...\n")
    
    for i, cmd in enumerate(edits, 1):
        result = agent.edit(cmd, working_bp)
        status = "PASS" if result.success else "FAIL"
        print(f"[{status}] Edit {i}: {cmd}")
        
        if result.success:
            working_bp = result.patched_blueprint
    
    # Verify all three changes
    hero = working_bp['components'][1]
    color_ok = hero['visual']['color'] == '#FF0000'
    height_ok = hero['visual']['height'] > 60
    text_ok = hero['text'].lower() == 'welcome home'
    
    print(f"\n[{'PASS' if color_ok else 'FAIL'}] Color: {hero['visual']['color']}")
    print(f"[{'PASS' if height_ok else 'FAIL'}] Height: {hero['visual']['height']}px")
    print(f"[{'PASS' if text_ok else 'FAIL'}] Text: '{hero['text']}'")
    
    return color_ok and height_ok and text_ok


def test_constraint_enforcement():
    """Test that constraints are enforced"""
    print("\n" + "="*80)
    print("TEST: CONSTRAINT ENFORCEMENT")
    print("="*80)
    
    agent = DesignEditAgent()
    
    # Try to make button extremely small (should still apply reasonable size)
    result = agent.edit("make cta1 tiny", complex_blueprint)
    
    if result.success:
        cta1 = result.patched_blueprint['components'][2]
        height = cta1['visual']['height']
        
        # Should still be reasonable size (not below 20px)
        reasonable = height >= 20
        
        print(f"[{'PASS' if reasonable else 'FAIL'}] Constraint enforced: {height}px (minimum 20px)")
        return reasonable
    
    return False


def test_all_components_in_bounds():
    """Test that all components stay in viewport"""
    print("\n" + "="*80)
    print("TEST: ALL COMPONENTS IN VIEWPORT BOUNDS")
    print("="*80)
    
    agent = DesignEditAgent()
    
    edits = [
        "make nav bigger",
        "make hero bigger",
        "make footer bigger",
    ]
    
    working_bp = complex_blueprint
    
    for cmd in edits:
        result = agent.edit(cmd, working_bp)
        if result.success:
            working_bp = result.patched_blueprint
    
    # Check all components are within bounds (assuming 480x800 viewport)
    all_ok = True
    for comp in working_bp['components']:
        bbox = comp['bbox']
        # x1, y1, x2, y2
        x1, y1, x2, y2 = bbox
        
        if not (0 <= x1 and x2 <= 480 and 0 <= y1 and y2 <= 800):
            all_ok = False
            print(f"  OUT OF BOUNDS: {comp['id']} at {bbox}")
    
    print(f"[{'PASS' if all_ok else 'FAIL'}] All components within viewport")
    return all_ok


def test_mixed_operations():
    """Test combining different operation types"""
    print("\n" + "="*80)
    print("TEST: MIXED OPERATIONS (COLOR + SIZE + TEXT)")
    print("="*80)
    
    agent = DesignEditAgent()
    working_bp = complex_blueprint
    
    commands = [
        ("change nav color to gray", "nav", "color", "#808080"),
        ("make nav bigger", "nav", "height", lambda x: x > 40),
        ("change nav text to Menu", "nav", "text", "menu"),
    ]
    
    all_ok = True
    
    for cmd, comp_id, field, expected in commands:
        result = agent.edit(cmd, working_bp)
        
        if result.success:
            comp = next((c for c in result.patched_blueprint['components'] if c['id'] == comp_id), None)
            
            if comp:
                if isinstance(expected, str):
                    if field == "color":
                        match = comp['visual'].get(field) == expected
                    else:
                        match = comp.get(field, "").lower() == expected.lower()
                elif callable(expected):
                    match = expected(comp.get(field, comp['visual'].get(field)))
                else:
                    match = comp.get(field) == expected or comp['visual'].get(field) == expected
                
                status = "PASS" if match else "FAIL"
                print(f"[{status}] {cmd}")
                
                working_bp = result.patched_blueprint
                
                if not match:
                    all_ok = False
            else:
                print(f"[FAIL] Component not found: {comp_id}")
                all_ok = False
        else:
            print(f"[FAIL] Edit failed: {cmd}")
            all_ok = False
    
    return all_ok


if __name__ == "__main__":
    print("\n" + "="*80)
    print("PHASE 10.1 ADVANCED EDGE CASE TESTING")
    print("="*80)
    
    tests = {
        "Multiple Same Type": test_multiple_same_type(),
        "Large Resize": test_large_resize(),
        "Color Normalization": test_color_normalization(),
        "Sequential Same Component": test_sequential_same_component(),
        "Constraint Enforcement": test_constraint_enforcement(),
        "Components In Bounds": test_all_components_in_bounds(),
        "Mixed Operations": test_mixed_operations(),
    }
    
    print("\n" + "="*80)
    print("EDGE CASE TEST RESULTS")
    print("="*80)
    
    passed = sum(1 for v in tests.values() if v)
    total = len(tests)
    
    for test_name, result in tests.items():
        status = "PASS" if result else "FAIL"
        print(f"[{status}] {test_name}")
    
    print(f"\nTOTAL: {passed}/{total} EDGE CASE TESTS PASSED")
    
    if passed == total:
        print("\nPHASE 10.1 AGENT HANDLES EDGE CASES CORRECTLY")
    else:
        print(f"\nWARNING: {total - passed} edge case tests failed")
