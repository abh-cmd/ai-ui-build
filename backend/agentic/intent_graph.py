"""
INTENT GRAPH: Parse and structure multiple intents from user commands.

Deterministically extracts intent types (resize, color, align, text, style, position, etc.)
and validates them against a schema.

Key principle: ONE COMMAND → MULTIPLE INTENTS
Example: "Make button bigger and red" → [resize, color]
"""

from typing import List, Dict, Any, Optional
from enum import Enum
from dataclasses import dataclass
import re


class IntentType(str, Enum):
    """Deterministic intent types extracted from commands."""
    RESIZE = "resize"          # size, bigger, smaller, width, height
    COLOR = "color"            # color, red, blue, primary, accent
    ALIGN = "align"            # center, left, right, top, bottom
    TEXT = "text"              # text content, label, placeholder
    STYLE = "style"            # bold, italic, shadow, rounded, border
    POSITION = "position"      # move, position, placement, offset
    VISIBILITY = "visibility"  # hide, show, visible, display
    DELETE = "delete"          # remove, delete, hide
    CREATE = "create"          # add, new, create


@dataclass
class Intent:
    """Structured representation of a single user intent."""
    type: IntentType
    target: Optional[str] = None        # component ID or type
    value: Optional[str] = None         # new value (color, size, etc)
    params: Dict[str, Any] = None       # additional parameters
    confidence: float = 1.0             # 0.0 to 1.0
    
    def __post_init__(self):
        if self.params is None:
            self.params = {}


class IntentGraph:
    """Parse and extract intents from user commands deterministically."""
    
    # Keyword mappings (deterministic)
    KEYWORDS = {
        # Resize
        "resize": ("resize", IntentType.RESIZE),
        "bigger": ("resize", IntentType.RESIZE),
        "smaller": ("resize", IntentType.RESIZE),
        "large": ("resize", IntentType.RESIZE),
        "small": ("resize", IntentType.RESIZE),
        "wider": ("resize", IntentType.RESIZE),
        "taller": ("resize", IntentType.RESIZE),
        "height": ("resize", IntentType.RESIZE),
        "width": ("resize", IntentType.RESIZE),
        
        # Color
        "color": ("color", IntentType.COLOR),
        "red": ("color", IntentType.COLOR),
        "blue": ("color", IntentType.COLOR),
        "green": ("color", IntentType.COLOR),
        "yellow": ("color", IntentType.COLOR),
        "purple": ("color", IntentType.COLOR),
        "orange": ("color", IntentType.COLOR),
        "black": ("color", IntentType.COLOR),
        "white": ("color", IntentType.COLOR),
        "primary": ("color", IntentType.COLOR),
        "accent": ("color", IntentType.COLOR),
        "dark": ("color", IntentType.COLOR),
        "light": ("color", IntentType.COLOR),
        
        # Align
        "align": ("align", IntentType.ALIGN),
        "center": ("align", IntentType.ALIGN),
        "left": ("align", IntentType.ALIGN),
        "right": ("align", IntentType.ALIGN),
        "top": ("align", IntentType.ALIGN),
        "bottom": ("align", IntentType.ALIGN),
        "centered": ("align", IntentType.ALIGN),
        
        # Text
        "text": ("text", IntentType.TEXT),
        "label": ("text", IntentType.TEXT),
        "placeholder": ("text", IntentType.TEXT),
        "content": ("text", IntentType.TEXT),
        
        # Style
        "bold": ("style", IntentType.STYLE),
        "italic": ("style", IntentType.STYLE),
        "shadow": ("style", IntentType.STYLE),
        "rounded": ("style", IntentType.STYLE),
        "border": ("style", IntentType.STYLE),
        "spacing": ("style", IntentType.STYLE),
        "padding": ("style", IntentType.STYLE),
        
        # Position
        "move": ("position", IntentType.POSITION),
        "position": ("position", IntentType.POSITION),
        "placement": ("position", IntentType.POSITION),
        "offset": ("position", IntentType.POSITION),
        
        # Visibility
        "hide": ("visibility", IntentType.VISIBILITY),
        "show": ("visibility", IntentType.VISIBILITY),
        "visible": ("visibility", IntentType.VISIBILITY),
        "display": ("visibility", IntentType.VISIBILITY),
        
        # Delete
        "delete": ("delete", IntentType.DELETE),
        "remove": ("delete", IntentType.DELETE),
        
        # Create
        "add": ("create", IntentType.CREATE),
        "new": ("create", IntentType.CREATE),
        "create": ("create", IntentType.CREATE),
    }
    
    # Component type keywords
    COMPONENT_TYPES = {
        "button": "button",
        "btn": "button",
        "cta": "button",
        "link": "link",
        "text": "text",
        "heading": "heading",
        "title": "heading",
        "product": "product",
        "image": "image",
        "navbar": "navbar",
        "nav": "navbar",
        "container": "container",
        "box": "container",
        "card": "card",
    }
    
    def parse(self, command: str, blueprint: Dict[str, Any]) -> List[Intent]:
        """
        Parse command into list of intents.
        
        Deterministic: Same command always produces same intents.
        
        Args:
            command: User command string (e.g., "Make button bigger and red")
            blueprint: Current blueprint (for context)
        
        Returns:
            List of Intent objects (ordered, deterministic)
        """
        if not command or not isinstance(command, str):
            return []
        
        # Normalize command
        command_lower = command.lower().strip()
        
        intents: List[Intent] = []
        found_keywords = set()
        
        # Extract intent types (deterministic order: keywords appear in order)
        for keyword, (category, intent_type) in self.KEYWORDS.items():
            if keyword in command_lower and keyword not in found_keywords:
                found_keywords.add(keyword)
                
                # Extract target if present
                target = self._extract_target(command_lower, blueprint)
                
                # Extract value if present (for colors, sizes, etc)
                value = self._extract_value(command_lower, intent_type)
                
                # Create intent with confidence based on specificity
                confidence = self._calculate_confidence(command, keyword, target, value)
                
                intent = Intent(
                    type=intent_type,
                    target=target,
                    value=value,
                    confidence=confidence
                )
                intents.append(intent)
        
        return intents
    
    def _extract_target(self, command: str, blueprint: Dict[str, Any]) -> Optional[str]:
        """Extract target component from command."""
        for comp_keyword, comp_type in self.COMPONENT_TYPES.items():
            if comp_keyword in command:
                return comp_type
        
        # If no component keyword found, return None
        return None
    
    def _extract_value(self, command: str, intent_type: IntentType) -> Optional[str]:
        """Extract value based on intent type (color, size, etc)."""
        if intent_type == IntentType.COLOR:
            # Extract color keywords
            colors = ["red", "blue", "green", "yellow", "purple", "orange", "black", "white", "dark", "light", "primary", "accent"]
            for color in colors:
                if color in command:
                    return color
        
        elif intent_type == IntentType.RESIZE:
            # Extract size indicators
            sizes = {
                "much bigger": "larger",
                "bigger": "large",
                "smaller": "small",
                "much smaller": "tiny",
                "double": "2x",
            }
            for size_key, size_val in sizes.items():
                if size_key in command:
                    return size_val
        
        elif intent_type == IntentType.ALIGN:
            aligns = ["center", "left", "right", "top", "bottom", "centered"]
            for align in aligns:
                if align in command:
                    return align
        
        return None
    
    def _calculate_confidence(self, original_command: str, keyword: str, target: Optional[str], value: Optional[str]) -> float:
        """
        Calculate confidence score for intent (0.0 to 1.0).
        
        Deterministic scoring:
        - Base: 0.9 (keyword found)
        - +0.05 if target found
        - +0.05 if value found
        """
        confidence = 0.9
        
        if target:
            confidence += 0.05
        
        if value:
            confidence += 0.05
        
        return min(1.0, confidence)
    
    def validate_intents(self, intents: List[Intent]) -> bool:
        """Validate that intents are well-formed."""
        for intent in intents:
            if not isinstance(intent.type, IntentType):
                return False
            if not 0.0 <= intent.confidence <= 1.0:
                return False
        
        return True
    
    def to_dict(self) -> Dict[str, Any]:
        """Export intent graph state."""
        return {
            "keywords_count": len(self.KEYWORDS),
            "component_types_count": len(self.COMPONENT_TYPES),
            "intent_types": [t.value for t in IntentType],
        }
