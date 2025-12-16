"""
PHASE 10.1 — STEP 1: INTENT PARSING

Parse natural language commands into structured intent.
No mutations. Pure analysis.

Command Grammar:
- Change color: "change [component] color to [color]"
- Resize: "make [component] bigger/smaller/[size]"
- Reorder: "move [component] to [position]"
- Text edit: "change [component] text to [text]"
- Style: "make [component] bold/italic/[style]"
"""

import re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class IntentType(Enum):
    """Possible design editing intents"""
    MODIFY_COLOR = "modify_color"
    RESIZE_COMPONENT = "resize_component"
    REORDER_COMPONENT = "reorder_component"
    EDIT_TEXT = "edit_text"
    MODIFY_STYLE = "modify_style"
    MODIFY_POSITION = "modify_position"
    UNKNOWN = "unknown"


@dataclass
class ComponentTarget:
    """Target component identification"""
    role: Optional[str] = None  # "cta", "header", "content", etc.
    component_type: Optional[str] = None  # "button", "text", "header", etc.
    index: Optional[int] = None  # If multiple same-type components
    text_match: Optional[str] = None  # Partial text match
    
    def __repr__(self):
        parts = []
        if self.role:
            parts.append(f"role={self.role}")
        if self.component_type:
            parts.append(f"type={self.component_type}")
        if self.index is not None:
            parts.append(f"index={self.index}")
        if self.text_match:
            parts.append(f"text~'{self.text_match}'")
        return f"Target({', '.join(parts)})"


@dataclass
class ParsedIntent:
    """Structured intent from natural language"""
    intent_type: IntentType
    confidence: float  # 0.0 - 1.0
    target: Optional[ComponentTarget]
    parameters: Dict = None
    reasoning: List[str] = None
    
    def __post_init__(self):
        if self.parameters is None:
            self.parameters = {}
        if self.reasoning is None:
            self.reasoning = []


class IntentParser:
    """
    PHASE 10.1 STEP 1: Parse natural language into structured intent.
    
    Rules:
    - NEVER guess component IDs
    - Identify using role + type
    - Mark ambiguous (confidence < 0.6)
    - Return explicit reasoning
    """
    
    # Command patterns (regex + intent mapping)
    PATTERNS = {
        # Color changes - HIGHEST specificity first
        IntentType.MODIFY_COLOR: [
            (r"change\s+(?P<target>.+?)\s+(?:color|background|bg)\s+to\s+(?P<color>.+?)(?:\.|$)", 0.95),
            (r"make\s+(?P<target>.+?)\s+(?P<color>red|blue|green|yellow|orange|purple|pink|white|black|gray|grey|brown|navy|teal|indigo|violet)\b", 0.85),
        ],
        
        # Resize
        IntentType.RESIZE_COMPONENT: [
            (r"(?:make|resize|increase|decrease)\s+(?P<target>.+?)\s+(?P<size>bigger|larger|smaller|huge|tiny|medium)(?:\s|\.|\b)", 0.90),
            (r"(?P<target>.+?)\s+(?P<size>\d+)px", 0.85),
            (r"increase\s+(?:the\s+)?size\s+(?:of\s+)?(?P<target>.+?)(?:\s|\.|\b)", 0.80),
        ],
        
        # Text editing - HIGHEST specificity first
        IntentType.EDIT_TEXT: [
            (r"change\s+(?:the\s+)?(?:text|label)\s+(?:of\s+|on\s+)?(?P<target>.+?)\s+to\s+(?P<text>.+?)(?:\.|$)", 0.95),
            (r"(?P<target>.+?)\s+(?:text|label)\s+(?:to|should\s+be|=)\s+(?P<text>.+?)(?:\.|$)", 0.90),
            (r"replace\s+(?:the\s+)?text\s+(?:with\s+)?(?P<text>.+?)(?:\.|$)", 0.85),
        ],
        
        # Style (bold, italic, etc)
        IntentType.MODIFY_STYLE: [
            (r"make\s+(?P<target>.+?)\s+(?P<style>bold|italic|underline|uppercase|lowercase)(?:\s|\.|\b)", 0.95),
            (r"(?P<target>.+?)\s+(?:should\s+)?be\s+(?P<style>bold|italic|heavy|light)(?:\s|\.|\b)", 0.85),
        ],
        
        # Reorder
        IntentType.REORDER_COMPONENT: [
            (r"move\s+(?P<target>.+?)\s+(?:to\s+)?(?P<position>top|bottom|left|right|center|first|last)(?:\s|\.|\b)", 0.90),
            (r"(?P<target>.+?)\s+(?:goes\s+)?(?P<position>above|below|before|after|next\s+to)\s+(?P<ref>.+?)(?:\s|\.|\b)", 0.85),
        ],
        
        # Position changes
        IntentType.MODIFY_POSITION: [
            (r"(?P<target>.+?)\s+(?:position|location)\s+(?P<position>.+?)(?:\.|$)", 0.80),
        ],
    }
    
    # Component type keywords
    COMPONENT_KEYWORDS = {
        "button": ["button", "cta", "action", "click"],
        "text": ["text", "label", "content", "paragraph", "heading", "title"],
        "header": ["header", "title", "heading", "h1"],
        "product": ["product", "item", "card", "listing"],
        "image": ["image", "icon", "photo", "picture"],
    }
    
    # Role keywords
    ROLE_KEYWORDS = {
        "cta": ["button", "order", "submit", "click", "action"],
        "hero": ["title", "header", "heading", "main"],
        "content": ["text", "description", "label", "info"],
        "decoration": ["icon", "image", "separator", "divider"],
    }
    
    # Color keyword mapping
    COLOR_KEYWORDS = {
        "#0000FF": ["blue", "primary", "accent"],
        "#FFFFFF": ["white", "light", "background"],
        "#000000": ["black", "dark"],
        "#FF0000": ["red", "danger", "warning"],
        "#00FF00": ["green", "success"],
        "#808080": ["gray", "grey", "neutral"],
    }
    
    def parse(self, command: str, blueprint: Dict) -> ParsedIntent:
        """
        Parse a natural language command into structured intent.
        
        Args:
            command: Natural language command
            blueprint: Current blueprint JSON
            
        Returns:
            ParsedIntent with confidence and reasoning
        """
        command_lower = command.lower().strip()
        reasoning = []
        
        # Step 1: Try to match command patterns
        intent_type = IntentType.UNKNOWN
        matched_pattern = None
        best_confidence = 0.0
        pattern_groups = {}
        
        for itype, patterns in self.PATTERNS.items():
            for pattern_regex, confidence in patterns:
                match = re.search(pattern_regex, command_lower, re.IGNORECASE)
                if match and confidence > best_confidence:
                    intent_type = itype
                    best_confidence = confidence
                    matched_pattern = pattern_regex
                    pattern_groups = match.groupdict()
                    reasoning.append(f"Matched pattern: {pattern_regex[:50]}...")
                    reasoning.append(f"Base confidence: {confidence}")
        
        # Step 2: Identify target component
        target = self._identify_target(command_lower, blueprint, pattern_groups, reasoning)
        
        # Step 3: Extract parameters
        parameters = self._extract_parameters(intent_type, pattern_groups, reasoning)
        
        # Step 4: Adjust confidence based on target clarity
        final_confidence = best_confidence
        if target and target.role:
            reasoning.append(f"Target clearly identified: {target.role}/{target.component_type}")
            final_confidence = min(1.0, final_confidence + 0.1)
        elif target and target.text_match:
            reasoning.append(f"Target identified by text pattern: '{target.text_match}'")
            final_confidence = max(0, final_confidence - 0.1)
        else:
            reasoning.append("Target ambiguous - needs clarification")
            final_confidence = max(0, final_confidence - 0.2)
        
        # Step 5: Final confidence check
        if final_confidence < 0.6:
            reasoning.append("CONFIDENCE TOO LOW - marking as uncertain")
            intent_type = IntentType.UNKNOWN
        
        return ParsedIntent(
            intent_type=intent_type,
            confidence=round(final_confidence, 2),
            target=target,
            parameters=parameters,
            reasoning=reasoning
        )
    
    def _identify_target(
        self,
        command: str,
        blueprint: Dict,
        pattern_groups: Dict,
        reasoning: List[str]
    ) -> Optional[ComponentTarget]:
        """
        Identify which component is being targeted.
        
        Uses:
        1. Explicit role/type from pattern
        2. Text matching from blueprint
        3. Component keywords
        """
        target = ComponentTarget()
        
        # Try to get target from regex groups
        if "target" in pattern_groups and pattern_groups["target"]:
            target_word = pattern_groups["target"].lower()
            reasoning.append(f"Target word from pattern: '{target_word}'")
            
            # Look up component type
            for comp_type, keywords in self.COMPONENT_KEYWORDS.items():
                if any(kw in target_word for kw in keywords):
                    target.component_type = comp_type
                    reasoning.append(f"Matched component type: {comp_type}")
                    break
            
            # Look up role
            for role, keywords in self.ROLE_KEYWORDS.items():
                if any(kw in target_word for kw in keywords):
                    target.role = role
                    reasoning.append(f"Matched role: {role}")
                    break
            
            # Try text matching in blueprint
            if "components" in blueprint:
                for idx, comp in enumerate(blueprint["components"]):
                    comp_text = comp.get("text", "").lower()
                    if target_word in comp_text or comp_text in target_word:
                        target.text_match = comp.get("text", "")
                        target.index = idx
                        reasoning.append(f"Matched component by text at index {idx}")
                        break
        
        return target if (target.role or target.component_type or target.text_match) else None
    
    def _extract_parameters(
        self,
        intent_type: IntentType,
        pattern_groups: Dict,
        reasoning: List[str]
    ) -> Dict:
        """Extract parameters specific to the intent type."""
        params = {}
        
        if intent_type == IntentType.MODIFY_COLOR:
            if "color" in pattern_groups:
                color = pattern_groups["color"].lower()
                normalized = self._normalize_color(color)
                if normalized:
                    params["color"] = normalized
                    reasoning.append(f"Color parameter: {params['color']}")
                else:
                    reasoning.append(f"Invalid color: {color}")
                    return {}  # Reject this intent
        
        elif intent_type == IntentType.RESIZE_COMPONENT:
            if "size" in pattern_groups:
                size = pattern_groups["size"].lower()
                params["size_direction"] = self._normalize_size(size)
                reasoning.append(f"Size parameter: {params['size_direction']}")
        
        elif intent_type == IntentType.EDIT_TEXT:
            if "text" in pattern_groups:
                params["new_text"] = pattern_groups["text"].strip()
                reasoning.append(f"Text parameter: '{params['new_text']}'")
        
        elif intent_type == IntentType.MODIFY_STYLE:
            if "style" in pattern_groups:
                params["style"] = pattern_groups["style"].lower()
                reasoning.append(f"Style parameter: {params['style']}")
        
        elif intent_type == IntentType.REORDER_COMPONENT:
            if "position" in pattern_groups:
                params["position"] = pattern_groups["position"].lower()
                reasoning.append(f"Position parameter: {params['position']}")
        
        return params
    
    def _normalize_color(self, color_str: str) -> Optional[str]:
        """Map color keywords to hex codes. Returns None if not a valid color."""
        color_str = color_str.lower().strip()
        
        # Check against keywords first
        for hex_color, keywords in self.COLOR_KEYWORDS.items():
            for kw in keywords:
                if color_str == kw:
                    return hex_color
        
        # Check direct color names
        color_map = {
            "blue": "#0000FF",
            "white": "#FFFFFF",
            "black": "#000000",
            "red": "#FF0000",
            "green": "#00FF00",
            "gray": "#808080",
            "grey": "#808080",
            "yellow": "#FFFF00",
            "orange": "#FFA500",
            "purple": "#800080",
            "pink": "#FFC0CB",
        }
        
        if color_str in color_map:
            return color_map[color_str]
        
        # Check if it's hex format
        if color_str.startswith("#") and len(color_str) == 7:
            try:
                int(color_str[1:], 16)
                return color_str
            except ValueError:
                return None
        
        # Not a valid color
        return None
    
    def _normalize_size(self, size_str: str) -> str:
        """Normalize size keywords."""
        size_map = {
            "bigger": "increase_20",
            "larger": "increase_20",
            "increase": "increase_20",
            "smaller": "decrease_20",
            "tiny": "decrease_30",
            "huge": "increase_50",
            "medium": "set_100",
        }
        return size_map.get(size_str.lower(), size_str)
