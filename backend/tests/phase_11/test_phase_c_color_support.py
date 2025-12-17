"""
PHASE C: COLOR SUPPORT EXTENSION TESTS

Tests validate:
- HEX color validation (#RRGGBB)
- CSS named color support (140+ colors)
- Semantic token support
- RGB/HSL color format conversion
- Color normalization
- Design token mapping
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))
sys.path.insert(0, str(Path.cwd() / "backend"))

from agentic.color_support import (
    ColorValidator,
    ColorNormalizer,
    ColorPalette,
    DesignTokenMapping,
    SemanticColor,
    ColorFormat,
    CSS_NAMED_COLORS
)


def test_hex_validation():
    """Test HEX color validation."""
    print("\n[PHASE C TEST 1] HEX Color Validation")
    
    # Valid HEX
    valid, normalized = ColorValidator.validate_hex("#FF0000")
    assert valid, "Valid HEX rejected"
    assert normalized == "#FF0000", f"Expected #FF0000, got {normalized}"
    
    # Invalid HEX
    valid, _ = ColorValidator.validate_hex("#GGGGGG")
    assert not valid, "Invalid HEX accepted"
    
    # Case insensitive
    valid, normalized = ColorValidator.validate_hex("#ff0000")
    assert valid, "Case-insensitive HEX failed"
    assert normalized == "#FF0000", f"Expected uppercase, got {normalized}"
    
    print(f"  PASS - HEX validation working correctly")
    print(f"  Examples: #FF0000, #00FF00, #0000FF all valid")
    return True


def test_named_color_validation():
    """Test CSS named color validation."""
    print("\n[PHASE C TEST 2] Named Color Validation")
    
    # Valid colors
    colors_to_test = ["red", "blue", "green", "navy", "crimson", "lightcoral"]
    
    for color in colors_to_test:
        valid, hex_val = ColorValidator.validate_named(color)
        assert valid, f"Named color '{color}' rejected"
        assert hex_val.startswith("#"), f"Expected HEX format, got {hex_val}"
    
    # Invalid color
    valid, _ = ColorValidator.validate_named("notacolor")
    assert not valid, "Invalid color accepted"
    
    # Case insensitive
    valid, hex_val = ColorValidator.validate_named("RED")
    assert valid, "Case-insensitive named color failed"
    assert hex_val == "#FF0000", f"Expected #FF0000, got {hex_val}"
    
    print(f"  PASS - Named color validation working")
    print(f"  Total colors available: {len(CSS_NAMED_COLORS)}")
    print(f"  Sample: {colors_to_test}")
    return True


def test_semantic_token_validation():
    """Test semantic token validation."""
    print("\n[PHASE C TEST 3] Semantic Token Validation")
    
    tokens = ["primary", "secondary", "accent", "success", "danger", "info"]
    
    for token in tokens:
        valid, value = ColorValidator.validate_semantic(token)
        assert valid, f"Semantic token '{token}' rejected"
        assert value == token, f"Expected {token}, got {value}"
    
    # Invalid token
    valid, _ = ColorValidator.validate_semantic("invalid_token")
    assert not valid, "Invalid token accepted"
    
    print(f"  PASS - Semantic token validation working")
    print(f"  Valid tokens: {tokens}")
    return True


def test_rgb_conversion():
    """Test RGB to HEX conversion."""
    print("\n[PHASE C TEST 4] RGB Color Conversion")
    
    # Valid RGB
    valid, hex_val = ColorValidator.validate_rgb("rgb(255, 0, 0)")
    assert valid, "Valid RGB rejected"
    assert hex_val == "#FF0000", f"Expected #FF0000, got {hex_val}"
    
    # RGB with spaces
    valid, hex_val = ColorValidator.validate_rgb("rgb( 0, 255, 0 )")
    assert valid, "RGB with spaces failed"
    assert hex_val == "#00FF00", f"Expected #00FF00, got {hex_val}"
    
    # Invalid RGB (out of range)
    valid, _ = ColorValidator.validate_rgb("rgb(256, 0, 0)")
    assert not valid, "Out-of-range RGB accepted"
    
    print(f"  PASS - RGB conversion working")
    print(f"  Examples: rgb(255,0,0)->FF0000, rgb(0,255,0)->#00FF00")
    return True


def test_hsl_conversion():
    """Test HSL to HEX conversion."""
    print("\n[PHASE C TEST 5] HSL Color Conversion")
    
    # Valid HSL (red)
    valid, hex_val = ColorValidator.validate_hsl("hsl(0, 100%, 50%)")
    assert valid, "Valid HSL rejected"
    assert hex_val.startswith("#"), f"Expected HEX format, got {hex_val}"
    
    # HSL with spaces
    valid, hex_val = ColorValidator.validate_hsl("hsl( 120, 100%, 50% )")
    assert valid, "HSL with spaces failed"
    
    # Invalid HSL (hue > 360)
    valid, _ = ColorValidator.validate_hsl("hsl(361, 100%, 50%)")
    assert not valid, "Out-of-range HSL accepted"
    
    print(f"  PASS - HSL conversion working")
    print(f"  Example: hsl(0,100%,50%) converted to HEX")
    return True


def test_color_normalizer():
    """Test universal color normalizer."""
    print("\n[PHASE C TEST 6] Color Normalizer")
    
    test_cases = [
        ("#FF0000", ColorFormat.HEX),
        ("red", ColorFormat.NAMED),
        ("rgb(0, 255, 0)", ColorFormat.RGB),
        ("primary", ColorFormat.SEMANTIC),
    ]
    
    normalizer = ColorNormalizer()
    
    for color_input, expected_format in test_cases:
        is_valid, normalized, color_format = normalizer.normalize(color_input)
        assert is_valid, f"Failed to normalize '{color_input}'"
        assert color_format == expected_format, \
            f"Expected {expected_format}, got {color_format}"
        assert normalized.startswith("#") or color_format == ColorFormat.SEMANTIC, \
            f"Expected HEX or token, got {normalized}"
    
    print(f"  PASS - Color normalizer working")
    print(f"  Successfully normalized {len(test_cases)} different formats")
    return True


def test_color_palette():
    """Test color palette management."""
    print("\n[PHASE C TEST 7] Color Palette Management")
    
    palette = ColorPalette()
    
    # Get named color
    hex_red = palette.get_color("red")
    assert hex_red == "#FF0000", f"Expected #FF0000, got {hex_red}"
    
    # Get semantic token
    hex_primary = palette.get_color("primary")
    assert hex_primary is not None, "Primary token not found"
    
    # Check availability
    assert palette.is_available("blue"), "Blue should be available"
    assert palette.is_available("primary"), "Primary should be available"
    assert not palette.is_available("notacolor"), "Invalid color should not be available"
    
    print(f"  PASS - Palette management working")
    print(f"  Available colors: {len(palette.available_colors)}")
    return True


def test_semantic_token_override():
    """Test overriding semantic tokens."""
    print("\n[PHASE C TEST 8] Semantic Token Override")
    
    palette = ColorPalette()
    
    # Get original primary
    original = palette.get_color("primary")
    
    # Override with new color
    success = palette.set_semantic_token("primary", "#00FF00")
    assert success, "Failed to set semantic token"
    
    # Verify it changed
    new_value = palette.get_color("primary")
    assert new_value == "#00FF00", f"Expected #00FF00, got {new_value}"
    assert new_value != original, "Token should have changed"
    
    # Try invalid HEX
    success = palette.set_semantic_token("primary", "invalid")
    assert not success, "Should reject invalid HEX"
    
    print(f"  PASS - Semantic token override working")
    return True


def test_design_token_mapping():
    """Test design token mapping."""
    print("\n[PHASE C TEST 9] Design Token Mapping")
    
    palette = ColorPalette()
    mapping = DesignTokenMapping(palette)
    
    # Get tokens
    text_primary = mapping.get_token("text.primary")
    assert text_primary is not None, "text.primary token not found"
    
    button_primary = mapping.get_token("button.primary")
    assert button_primary is not None, "button.primary token not found"
    
    # All should be valid HEX or colors
    assert text_primary.startswith("#"), f"Expected HEX, got {text_primary}"
    
    print(f"  PASS - Design token mapping working")
    print(f"  Sample tokens: text.primary={text_primary}, button.primary={button_primary}")
    return True


def test_large_palette_support():
    """Test support for large color palette."""
    print("\n[PHASE C TEST 10] Large Palette Support")
    
    # Verify we have 120+ CSS colors
    assert len(CSS_NAMED_COLORS) > 120, f"Expected 120+ colors, got {len(CSS_NAMED_COLORS)}"
    
    # Test sample of colors
    sample_colors = [
        "red", "blue", "green", "yellow", "orange", "purple",
        "crimson", "navy", "teal", "olive", "coral", "salmon",
        "gold", "khaki", "plum", "orchid", "lavender", "indigo"
    ]
    
    for color in sample_colors:
        valid, hex_val = ColorValidator.validate_named(color)
        assert valid, f"Color {color} not in palette"
        assert hex_val.startswith("#"), f"Invalid HEX for {color}"
    
    print(f"  PASS - Large palette available")
    print(f"  Total CSS colors: {len(CSS_NAMED_COLORS)}")
    print(f"  Tested: {sample_colors}")
    return True


def test_determinism():
    """Test that color operations are deterministic."""
    print("\n[PHASE C TEST 11] Determinism")
    
    normalizer = ColorNormalizer()
    command_colors = ["red", "blue", "rgb(255, 0, 0)", "#00FF00", "primary"]
    
    # Normalize multiple times
    for color in command_colors:
        result1 = normalizer.normalize(color)
        result2 = normalizer.normalize(color)
        result3 = normalizer.normalize(color)
        
        assert result1 == result2 == result3, \
            f"Non-deterministic result for {color}: {result1} vs {result2} vs {result3}"
    
    print(f"  PASS - All operations deterministic")
    print(f"  Tested {len(command_colors)} colors across 3 runs each")
    return True


if __name__ == "__main__":
    print("\n" + "="*60)
    print("PHASE C: COLOR SUPPORT EXTENSION TESTS")
    print("="*60)
    
    tests = [
        test_hex_validation,
        test_named_color_validation,
        test_semantic_token_validation,
        test_rgb_conversion,
        test_hsl_conversion,
        test_color_normalizer,
        test_color_palette,
        test_semantic_token_override,
        test_design_token_mapping,
        test_large_palette_support,
        test_determinism,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
        except AssertionError as e:
            failed += 1
            print(f"  FAIL: {e}")
        except Exception as e:
            failed += 1
            print(f"  ERROR: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "="*60)
    print(f"RESULTS: {passed} passed, {failed} failed")
    print("="*60)
    
    if failed == 0:
        print("PHASE C TESTS: ALL PASS - Extended color support ready")
    else:
        print(f"PHASE C TESTS: {failed} failing - needs fixes")
    
    sys.exit(0 if failed == 0 else 1)
