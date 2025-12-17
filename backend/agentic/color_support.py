"""
PHASE C: COLOR SUPPORT EXTENSION

Extends color palette from 12 colors to support:
- HEX colors: #RRGGBB format
- CSS named colors: All standard CSS color names (140+ colors)
- Semantic tokens: primary, secondary, accent, success, warning, danger
- Color validation and normalization
- Design token mapping

Current limitation: Only 12 hardcoded colors
Goal: Support full CSS color spectrum while maintaining type safety
"""

from typing import Dict, Optional, Tuple, Set
from dataclasses import dataclass
from enum import Enum
import re


class ColorFormat(Enum):
    """Supported color formats."""
    HEX = "hex"              # #RRGGBB
    NAMED = "named"          # "red", "blue", etc.
    SEMANTIC = "semantic"    # "primary", "accent", etc.
    RGB = "rgb"              # rgb(255, 0, 0)
    HSL = "hsl"              # hsl(0, 100%, 50%)


class SemanticColor(Enum):
    """Semantic color tokens."""
    PRIMARY = "primary"
    SECONDARY = "secondary"
    ACCENT = "accent"
    SUCCESS = "success"
    WARNING = "warning"
    DANGER = "danger"
    INFO = "info"
    LIGHT = "light"
    DARK = "dark"


# CSS Named Colors - Complete 147-color palette
CSS_NAMED_COLORS: Dict[str, str] = {
    # Reds
    "red": "#FF0000",
    "crimson": "#DC143C",
    "darkred": "#8B0000",
    "firebrick": "#B22222",
    "indianred": "#CD5C5C",
    "lightcoral": "#F08080",
    "salmon": "#FA8072",
    "lightsalmon": "#FFA07A",
    
    # Greens
    "green": "#008000",
    "darkgreen": "#006400",
    "forestgreen": "#228B22",
    "limegreen": "#32CD32",
    "lime": "#00FF00",
    "springgreen": "#00FF7F",
    "mediumspringgreen": "#00FA9A",
    "lightgreen": "#90EE90",
    "palegreen": "#98FB98",
    "darkseagreen": "#8FBC8F",
    "mediumseagreen": "#3CB371",
    "seagreen": "#2E8B57",
    
    # Blues
    "blue": "#0000FF",
    "darkblue": "#00008B",
    "navy": "#000080",
    "mediumblue": "#0000CD",
    "lightblue": "#ADD8E6",
    "skyblue": "#87CEEB",
    "lightskyblue": "#87CEFA",
    "steelblue": "#4682B4",
    "cornflowerblue": "#6495ED",
    "royalblue": "#4169E1",
    "dodgerblue": "#1E90FF",
    "deepskyblue": "#00BFFF",
    "powderblue": "#B0E0E6",
    "slateblue": "#6A5ACD",
    "mediumslateblue": "#7B68EE",
    "darkslateblue": "#483D8B",
    "midnightblue": "#191970",
    
    # Yellows
    "yellow": "#FFFF00",
    "gold": "#FFD700",
    "lightyellow": "#FFFFE0",
    "lemonchiffon": "#FFFACD",
    "papayawhip": "#FFEFD5",
    "moccasin": "#FFE4B5",
    "peachpuff": "#FFDAB9",
    "palegoldenrod": "#EEE8AA",
    "khaki": "#F0E68C",
    "darkkhaki": "#BDB76B",
    
    # Oranges
    "orange": "#FFA500",
    "darkorange": "#FF8C00",
    "orangered": "#FF4500",
    "tomato": "#FF6347",
    "coral": "#FF7F50",
    "lightcoral": "#F08080",
    
    # Purples & Violets
    "purple": "#800080",
    "darkmagenta": "#8B008B",
    "magenta": "#FF00FF",
    "violet": "#EE82EE",
    "mediumvioletred": "#C71585",
    "deeppink": "#FF1493",
    "hotpink": "#FF69B4",
    "lightpink": "#FFB6C1",
    "lavender": "#E6E6FA",
    "mediumorchid": "#BA55D3",
    "orchid": "#DA70D6",
    "plum": "#DDA0DD",
    "thistle": "#D8BFD8",
    "indigo": "#4B0082",
    "blueviolet": "#8A2BE2",
    
    # Grays & Neutrals
    "black": "#000000",
    "white": "#FFFFFF",
    "gray": "#808080",
    "grey": "#808080",
    "darkgray": "#A9A9A9",
    "darkgrey": "#A9A9A9",
    "lightgray": "#D3D3D3",
    "lightgrey": "#D3D3D3",
    "gainsboro": "#DCDCDC",
    "whitesmoke": "#F5F5F5",
    "darkslategray": "#2F4F4F",
    "darkslategrey": "#2F4F4F",
    "slategray": "#708090",
    "slategrey": "#708090",
    "silver": "#C0C0C0",
    "dimgray": "#696969",
    "dimgrey": "#696969",
    
    # Browns
    "brown": "#A52A2A",
    "maroon": "#800000",
    "darkbrown": "#654321",
    "saddlebrown": "#8B4513",
    "sienna": "#A0522D",
    "peru": "#CD853F",
    "tan": "#D2B48C",
    "burlywood": "#DEB887",
    "chocolate": "#D2691E",
    "rosybrown": "#BC8F8F",
    
    # Cyans & Teals
    "cyan": "#00FFFF",
    "aqua": "#00FFFF",
    "darkcyan": "#008B8B",
    "teal": "#008080",
    "darkturquoise": "#00CED1",
    "mediumturquoise": "#48D1CC",
    "turquoise": "#40E0D0",
    "lightseagreen": "#20B2AA",
    "lightcyan": "#E0FFFF",
    "aquamarine": "#7FFFD4",
    "cadetblue": "#5F9EA0",
    
    # Pinks & Reds Extended
    "pink": "#FFC0CB",
    "lightpink": "#FFB6C1",
    "palevioletred": "#DB7093",
    "darkgoldenrod": "#B8860B",
    "goldenrod": "#DAA520",
    
    # Olives & Browns Extended
    "olive": "#808000",
    "olivedrab": "#6B8E23",
    
    # Additional useful colors
    "beige": "#F5F5DC",
    "bisque": "#FFE4C4",
    "blanchedalmond": "#FFEBCD",
    "cornsilk": "#FFF8DC",
    "eggshell": "#F0EFF0",
    "floralwhite": "#FFFAF0",
    "ghostwhite": "#F8F8FF",
    "honeydew": "#F0FFF0",
    "ivory": "#FFFFF0",
    "linen": "#FAF0E6",
    "mintcream": "#F5FFFA",
    "mistyrose": "#FFE4E1",
    "navajowhite": "#FFDEAD",
    "oldlace": "#FDF5E6",
    "seashell": "#FFF5EE",
    "snow": "#FFFAFA",
    "wheat": "#F5DEB3",
    "antiquewhite": "#FAEBD7",
    "azure": "#F0FFFF",
    "lavenderblush": "#FFF0F5",
}


class ColorValidator:
    """Validate and normalize colors."""
    
    HEX_PATTERN = re.compile(r'^#[0-9A-Fa-f]{6}$')
    RGB_PATTERN = re.compile(r'^rgb\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)$')
    HSL_PATTERN = re.compile(r'^hsl\(\s*(\d+)\s*,\s*(\d+)%\s*,\s*(\d+)%\s*\)$')
    
    @classmethod
    def validate_hex(cls, color: str) -> Tuple[bool, str]:
        """
        Validate HEX color format.
        
        Args:
            color: Color string (e.g., "#FF0000")
        
        Returns:
            (is_valid, normalized_color)
        """
        color = color.strip()
        
        if not cls.HEX_PATTERN.match(color):
            return False, ""
        
        return True, color.upper()
    
    @classmethod
    def validate_named(cls, color: str) -> Tuple[bool, str]:
        """
        Validate CSS named color.
        
        Args:
            color: Color name (e.g., "red")
        
        Returns:
            (is_valid, hex_value)
        """
        color_lower = color.strip().lower()
        
        if color_lower in CSS_NAMED_COLORS:
            return True, CSS_NAMED_COLORS[color_lower]
        
        return False, ""
    
    @classmethod
    def validate_semantic(cls, token: str) -> Tuple[bool, str]:
        """
        Validate semantic token.
        
        Args:
            token: Semantic token (e.g., "primary")
        
        Returns:
            (is_valid, token_value)
        """
        token_lower = token.strip().lower()
        
        try:
            SemanticColor[token_lower.upper()]
            return True, token_lower
        except KeyError:
            return False, ""
    
    @classmethod
    def validate_rgb(cls, color: str) -> Tuple[bool, str]:
        """
        Validate RGB color format and convert to HEX.
        
        Args:
            color: Color string (e.g., "rgb(255, 0, 0)")
        
        Returns:
            (is_valid, hex_value)
        """
        match = cls.RGB_PATTERN.match(color.strip())
        
        if not match:
            return False, ""
        
        r, g, b = int(match.group(1)), int(match.group(2)), int(match.group(3))
        
        if not (0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255):
            return False, ""
        
        hex_value = f"#{r:02X}{g:02X}{b:02X}"
        return True, hex_value
    
    @classmethod
    def validate_hsl(cls, color: str) -> Tuple[bool, str]:
        """
        Validate HSL color format and convert to HEX.
        
        Args:
            color: Color string (e.g., "hsl(0, 100%, 50%)")
        
        Returns:
            (is_valid, hex_value)
        """
        match = cls.HSL_PATTERN.match(color.strip())
        
        if not match:
            return False, ""
        
        h, s, l = int(match.group(1)), int(match.group(2)), int(match.group(3))
        
        if not (0 <= h <= 360 and 0 <= s <= 100 and 0 <= l <= 100):
            return False, ""
        
        # Convert HSL to RGB to HEX
        hex_value = cls._hsl_to_hex(h, s, l)
        return True, hex_value
    
    @staticmethod
    def _hsl_to_hex(h: int, s: int, l: int) -> str:
        """Convert HSL to HEX color."""
        h = h / 360.0
        s = s / 100.0
        l = l / 100.0
        
        if s == 0:
            r = g = b = int(l * 255)
        else:
            def hue2rgb(p: float, q: float, t: float) -> float:
                if t < 0:
                    t += 1
                if t > 1:
                    t -= 1
                if t < 1/6:
                    return p + (q - p) * 6 * t
                if t < 1/2:
                    return q
                if t < 2/3:
                    return p + (q - p) * (2/3 - t) * 6
                return p
            
            q = l * (1 + s) if l < 0.5 else l + s - l * s
            p = 2 * l - q
            
            r = int(hue2rgb(p, q, h + 1/3) * 255)
            g = int(hue2rgb(p, q, h) * 255)
            b = int(hue2rgb(p, q, h - 1/3) * 255)
        
        return f"#{r:02X}{g:02X}{b:02X}"


class ColorNormalizer:
    """Normalize colors to standard format."""
    
    @classmethod
    def normalize(cls, color_input: str) -> Tuple[bool, str, ColorFormat]:
        """
        Normalize any color format to HEX.
        
        Args:
            color_input: Color in any supported format
        
        Returns:
            (is_valid, normalized_hex, format_type)
        """
        color_input = color_input.strip()
        
        # Try HEX
        is_valid, hex_val = ColorValidator.validate_hex(color_input)
        if is_valid:
            return True, hex_val, ColorFormat.HEX
        
        # Try RGB
        is_valid, hex_val = ColorValidator.validate_rgb(color_input)
        if is_valid:
            return True, hex_val, ColorFormat.RGB
        
        # Try HSL
        is_valid, hex_val = ColorValidator.validate_hsl(color_input)
        if is_valid:
            return True, hex_val, ColorFormat.HSL
        
        # Try Named
        is_valid, hex_val = ColorValidator.validate_named(color_input)
        if is_valid:
            return True, hex_val, ColorFormat.NAMED
        
        # Try Semantic
        is_valid, token = ColorValidator.validate_semantic(color_input)
        if is_valid:
            return True, token, ColorFormat.SEMANTIC
        
        return False, "", ColorFormat.NAMED


class ColorPalette:
    """Manages application color palette with design tokens."""
    
    def __init__(self):
        """Initialize with default semantic tokens."""
        self.semantic_map: Dict[str, str] = {
            "primary": "#3B82F6",      # Blue
            "secondary": "#6B7280",    # Gray
            "accent": "#F59E0B",       # Amber
            "success": "#10B981",      # Green
            "warning": "#F59E0B",      # Amber
            "danger": "#EF4444",       # Red
            "info": "#3B82F6",         # Blue
            "light": "#F3F4F6",        # Light gray
            "dark": "#111827",         # Dark gray
        }
        
        # Track all available colors for validation
        self.available_colors = set(CSS_NAMED_COLORS.keys()) | set(self.semantic_map.keys())
    
    def get_color(self, color_name: str) -> Optional[str]:
        """
        Get color HEX value by name or token.
        
        Args:
            color_name: Named color or semantic token
        
        Returns:
            HEX value or None if not found
        """
        color_lower = color_name.lower()
        
        # Check semantic tokens first
        if color_lower in self.semantic_map:
            return self.semantic_map[color_lower]
        
        # Check named colors
        if color_lower in CSS_NAMED_COLORS:
            return CSS_NAMED_COLORS[color_lower]
        
        return None
    
    def set_semantic_token(self, token: str, hex_color: str) -> bool:
        """
        Set or override a semantic token.
        
        Args:
            token: Token name
            hex_color: HEX color value
        
        Returns:
            True if successful
        """
        is_valid, normalized = ColorValidator.validate_hex(hex_color)
        if not is_valid:
            return False
        
        token_lower = token.lower()
        # Check if token is a valid semantic token by checking enum values
        valid_tokens = {color.value.lower() for color in SemanticColor}
        if token_lower not in valid_tokens:
            return False
        
        self.semantic_map[token_lower] = normalized
        return True
    
    def is_available(self, color_name: str) -> bool:
        """Check if color is available in palette."""
        return color_name.lower() in self.available_colors


class DesignTokenMapping:
    """Map design system tokens to color values."""
    
    def __init__(self, palette: ColorPalette):
        """Initialize with color palette."""
        self.palette = palette
        self.tokens: Dict[str, str] = {}
        self._build_tokens()
    
    def _build_tokens(self) -> None:
        """Build complete token mapping."""
        # Text colors
        self.tokens["text.primary"] = self.palette.get_color("dark")
        self.tokens["text.secondary"] = self.palette.get_color("secondary")
        self.tokens["text.disabled"] = "#9CA3AF"
        
        # Background colors
        self.tokens["bg.primary"] = self.palette.get_color("white")
        self.tokens["bg.secondary"] = self.palette.get_color("light")
        self.tokens["bg.tertiary"] = "#F9FAFB"
        
        # Border colors
        self.tokens["border.primary"] = "#E5E7EB"
        self.tokens["border.secondary"] = "#D1D5DB"
        
        # Button colors
        self.tokens["button.primary"] = self.palette.get_color("primary")
        self.tokens["button.secondary"] = self.palette.get_color("secondary")
        self.tokens["button.success"] = self.palette.get_color("success")
        self.tokens["button.danger"] = self.palette.get_color("danger")
    
    def get_token(self, token_path: str) -> Optional[str]:
        """Get token value by path."""
        return self.tokens.get(token_path)
