"""
PHASE B: INTENT PARSER IMPROVEMENT

Replaces keyword-based parsing with rule-based intent grammar to support:
- Compound commands: "Make button bigger and red"
- Multi-intent extraction: [RESIZE, COLOR]
- Per-intent confidence scoring
- Fallback safety for ambiguous commands

Current limitation: Keyword-based parsing struggles with compound commands
Goal: Support complex natural language intent extraction

Architecture:
1. IntentGrammar: Define rules for intent patterns
2. CompoundIntentParser: Parse compound commands
3. IntentValidator: Validate parsed intents
4. SafetyFallback: Graceful degradation for ambiguous commands
"""

from typing import Dict, Any, List, Optional, Tuple, Pattern
from dataclasses import dataclass, field
from enum import Enum
import re


class IntentPattern(Enum):
    """Pattern types for intent recognition."""
    # Size patterns
    SIZE_INCREASE = r"\b(bigger|larger|increase|expand|grow|extend|wider|taller|wider)\b"
    SIZE_DECREASE = r"\b(smaller|reduce|shrink|decrease|narrow|shorten|compress|diminish)\b"
    SIZE_EXPLICIT = r"\b((?:width|height|size)\s*(?:of)?\s*\d+|set\s+(?:width|height|size))\b"
    
    # Color patterns
    COLOR_NAMED = r"\b(red|blue|green|yellow|orange|purple|pink|brown|black|white|gray|grey|navy|teal|cyan|magenta)\b"
    COLOR_HEX = r"\#[0-9A-Fa-f]{6}\b"
    COLOR_SEMANTIC = r"\b(primary|secondary|accent|success|warning|danger|info|light|dark)\b"
    
    # Text patterns
    TEXT_CHANGE = r"\b(change|set|make|update|modify)\s+(?:text|label|content|title)\b"
    TEXT_ADD = r"\b(add|put|insert|write)\s+(?:text|label|content)\b"
    
    # Alignment patterns
    ALIGN_HORIZONTAL = r"\b(left|right|center|center-align)\b"
    ALIGN_VERTICAL = r"\b(top|bottom|middle|center-align)\b"
    ALIGN_COMBINED = r"\b(center|middle)\b"
    
    # Style patterns
    STYLE_BOLD = r"\b(bold|make.*bold|emphasis)\b"
    STYLE_ROUNDED = r"\b(round|rounded|border-radius)\b"
    STYLE_SHADOW = r"\b(shadow|drop-shadow)\b"
    
    # Visibility patterns
    VISIBILITY_HIDE = r"\b(hide|hidden|invisible|remove|delete)\b"
    VISIBILITY_SHOW = r"\b(show|visible|display)\b"
    
    # Target patterns
    TARGET_BUTTON = r"\b(button|btn)\b"
    TARGET_CARD = r"\b(card|card\s+component)\b"
    TARGET_TEXT = r"\b(text|label|heading|title)\b"
    TARGET_IMAGE = r"\b(image|img|photo|picture)\b"
    TARGET_CONTAINER = r"\b(container|box|div|section)\b"


@dataclass
class ParsedIntent:
    """Result of parsing a single intent from text."""
    type: str  # "COLOR", "RESIZE", "TEXT", "ALIGN", "STYLE", "VISIBILITY"
    target: Optional[str]  # Component name or None
    value: Optional[str]  # Parsed value
    confidence: float  # 0.0 to 1.0
    reason: str  # Why this confidence level
    matches: Dict[str, Any] = field(default_factory=dict)  # Raw pattern matches


@dataclass
class CompoundParseResult:
    """Result of parsing a compound command."""
    intents: List[ParsedIntent]
    combined_confidence: float  # Average of individual confidences
    ambiguity_level: str  # "clear", "moderate", "ambiguous"
    fallback_used: bool  # Whether safety fallback was activated
    explanation: str


class IntentGrammarRules:
    """Define grammar rules for intent recognition."""
    
    # Size change patterns
    SIZE_RULES = {
        "bigger|larger|increase|expand|grow": ("resize", "increase", 0.95),
        "smaller|reduce|shrink|decrease": ("resize", "decrease", 0.95),
        "width\\s*(\\d+)|height\\s*(\\d+)": ("resize", "explicit", 0.90),
    }
    
    # Color patterns
    COLOR_RULES = {
        "red|crimson|scarlet": ("color", "red", 0.95),
        "blue|navy|azure": ("color", "blue", 0.95),
        "green|lime|emerald": ("color", "green", 0.95),
        "yellow|gold|amber": ("color", "yellow", 0.95),
        "orange|coral": ("color", "orange", 0.95),
        "purple|violet|indigo": ("color", "purple", 0.95),
        "pink|magenta|rose": ("color", "pink", 0.95),
        "brown|tan|beige": ("color", "brown", 0.95),
        "black|dark": ("color", "black", 0.95),
        "white|light": ("color", "white", 0.95),
        "gray|grey": ("color", "gray", 0.95),
        "#[0-9a-f]{6}": ("color", "hex", 0.95),
        "primary|accent|secondary": ("color", "semantic", 0.85),
    }
    
    # Text patterns
    TEXT_RULES = {
        "change\\s+(?:text|label|content)\\s+to\\s+(.+)": ("text", "set", 0.90),
        "add\\s+(?:text|label)\\s+(.+)": ("text", "add", 0.90),
        "set\\s+(?:text|label)\\s+to\\s+(.+)": ("text", "set", 0.90),
    }
    
    # Target patterns
    TARGET_RULES = {
        "button|btn": "button",
        "card": "card",
        "text|label|heading": "text",
        "image|img": "image",
        "container|box": "container",
        "header|nav": "navbar",
    }


class CompoundIntentParser:
    """Parse compound natural language commands into structured intents."""
    
    def __init__(self):
        """Initialize the compound intent parser."""
        self.rules = IntentGrammarRules()
        self._compile_patterns()
    
    def _compile_patterns(self) -> None:
        """Compile regex patterns for efficiency."""
        self.compiled_patterns: Dict[str, Pattern] = {}
        
        # Compile all rule patterns
        for pattern_dict in [self.rules.SIZE_RULES, self.rules.COLOR_RULES, self.rules.TEXT_RULES]:
            for pattern, _ in pattern_dict.items():
                key = f"{pattern}"
                self.compiled_patterns[key] = re.compile(pattern, re.IGNORECASE)
    
    def parse_compound(self, command: str) -> CompoundParseResult:
        """
        Parse a compound command into multiple intents.
        
        Args:
            command: User command (e.g., "Make button bigger and red")
        
        Returns:
            CompoundParseResult with parsed intents and metadata
        """
        # Split on conjunctions
        segments = self._split_by_conjunctions(command)
        
        parsed_intents: List[ParsedIntent] = []
        segment_confidences: List[float] = []
        
        # Parse each segment
        for segment in segments:
            intent = self._parse_single_segment(segment.strip(), command)
            if intent:
                parsed_intents.append(intent)
                segment_confidences.append(intent.confidence)
        
        # Calculate combined metrics
        if segment_confidences:
            combined_confidence = sum(segment_confidences) / len(segment_confidences)
        else:
            combined_confidence = 0.0
        
        ambiguity = self._assess_ambiguity(command, parsed_intents, combined_confidence)
        fallback = combined_confidence < 0.7  # Use fallback if low confidence
        
        explanation = self._build_explanation(parsed_intents, combined_confidence, ambiguity)
        
        return CompoundParseResult(
            intents=parsed_intents,
            combined_confidence=combined_confidence,
            ambiguity_level=ambiguity,
            fallback_used=fallback,
            explanation=explanation
        )
    
    def _split_by_conjunctions(self, command: str) -> List[str]:
        """
        Split command by conjunctions (and, or, then) and commas.
        
        Examples:
            "Make button bigger and red" -> ["Make button bigger", "red"]
            "Change color to red, blue, and green" -> ["Change color to red", "blue", "green"]
        """
        # Replace commas with 'and' for consistent handling
        command_normalized = command.replace(',', ' and ')
        
        # Split by 'and', 'or', 'then'
        pattern = r'\s+(?:and|or|then)\s+'
        segments = re.split(pattern, command_normalized, flags=re.IGNORECASE)
        return [s.strip() for s in segments if s.strip()]
    
    def _parse_single_segment(self, segment: str, full_command: str) -> Optional[ParsedIntent]:
        """
        Parse a single segment into an intent.
        
        Args:
            segment: Single segment (e.g., "button bigger")
            full_command: Full original command (for context)
        
        Returns:
            ParsedIntent or None if no match
        """
        intent_type = None
        value = None
        confidence = 0.0
        matches = {}
        
        # Try to match size patterns
        for pattern, (itype, val, conf) in self.rules.SIZE_RULES.items():
            if re.search(pattern, segment, re.IGNORECASE):
                intent_type = itype
                value = val
                confidence = conf
                matches['pattern'] = pattern
                break
        
        # Try to match color patterns
        if not intent_type:
            for pattern, (itype, val, conf) in self.rules.COLOR_RULES.items():
                match = re.search(pattern, segment, re.IGNORECASE)
                if match:
                    intent_type = itype
                    value = val
                    confidence = conf
                    matches['pattern'] = pattern
                    matches['match'] = match.group(0)
                    break
        
        # Try to match target
        target = None
        for pattern, tgt in self.rules.TARGET_RULES.items():
            if re.search(pattern, full_command, re.IGNORECASE):
                target = tgt
                matches['target_pattern'] = pattern
                break
        
        if intent_type:
            reason = f"Matched {intent_type} with pattern '{matches.get('pattern', 'unknown')}'"
            
            return ParsedIntent(
                type=intent_type.upper(),
                target=target,
                value=value,
                confidence=confidence,
                reason=reason,
                matches=matches
            )
        
        return None
    
    def _assess_ambiguity(
        self,
        command: str,
        intents: List[ParsedIntent],
        confidence: float
    ) -> str:
        """
        Assess ambiguity level of the parsed command.
        
        Returns: "clear", "moderate", or "ambiguous"
        """
        if not intents:
            return "ambiguous"
        
        if confidence >= 0.85 and len(intents) <= 2:
            return "clear"
        elif confidence >= 0.70:
            return "moderate"
        else:
            return "ambiguous"
    
    def _build_explanation(
        self,
        intents: List[ParsedIntent],
        combined_confidence: float,
        ambiguity: str
    ) -> str:
        """Build human-readable explanation of parsing."""
        lines = []
        lines.append(f"Parsed {len(intents)} intent(s)")
        lines.append(f"Combined confidence: {combined_confidence:.1%}")
        lines.append(f"Ambiguity level: {ambiguity}")
        
        for i, intent in enumerate(intents, 1):
            lines.append(f"  [{i}] {intent.type}")
            if intent.target:
                lines.append(f"      Target: {intent.target}")
            if intent.value:
                lines.append(f"      Value: {intent.value}")
            lines.append(f"      Confidence: {intent.confidence:.1%} ({intent.reason})")
        
        return "\n".join(lines)


class IntentValidator:
    """Validate parsed intents for safety and consistency."""
    
    # Valid intent types
    VALID_TYPES = {
        "RESIZE", "COLOR", "TEXT", "ALIGN", "STYLE", "VISIBILITY",
        "POSITION", "DELETE", "CREATE"
    }
    
    # Valid targets
    VALID_TARGETS = {
        "button", "card", "text", "image", "container", "navbar",
        None  # No specific target
    }
    
    # Valid color values
    VALID_COLORS = {
        "red", "blue", "green", "yellow", "orange", "purple", "pink",
        "brown", "black", "white", "gray", "navy", "teal", "cyan",
        "magenta", "hex", "semantic"
    }
    
    @classmethod
    def validate(cls, intent: ParsedIntent) -> Tuple[bool, str]:
        """
        Validate a parsed intent.
        
        Returns: (is_valid, reason)
        """
        # Check type
        if intent.type not in cls.VALID_TYPES:
            return False, f"Invalid intent type: {intent.type}"
        
        # Check target
        if intent.target and intent.target not in cls.VALID_TARGETS:
            return False, f"Invalid target: {intent.target}"
        
        # Check value for color intent
        if intent.type == "COLOR" and intent.value not in cls.VALID_COLORS:
            return False, f"Invalid color: {intent.value}"
        
        # Check confidence
        if not (0.0 <= intent.confidence <= 1.0):
            return False, f"Invalid confidence: {intent.confidence}"
        
        return True, "Valid"


class SafetyFallback:
    """Graceful degradation when parsing is ambiguous."""
    
    @staticmethod
    def apply_fallback(
        compound_result: CompoundParseResult,
        original_command: str
    ) -> CompoundParseResult:
        """
        Apply safety fallback for ambiguous commands.
        
        When ambiguity is high, fall back to simpler heuristics.
        """
        if compound_result.ambiguity_level == "clear" and compound_result.combined_confidence >= 0.85:
            # No fallback needed
            return compound_result
        
        # For moderate/ambiguous, try keyword-based fallback
        # This maintains backward compatibility
        fallback_intents = SafetyFallback._keyword_fallback(original_command)
        
        if fallback_intents:
            return CompoundParseResult(
                intents=fallback_intents,
                combined_confidence=min(0.75, compound_result.combined_confidence),
                ambiguity_level="moderate",
                fallback_used=True,
                explanation=f"Safety fallback applied. {compound_result.explanation}"
            )
        
        return compound_result
    
    @staticmethod
    def _keyword_fallback(command: str) -> List[ParsedIntent]:
        """Simple keyword-based fallback."""
        # This is a simplified version - actual implementation would be more robust
        intents = []
        
        # Color keywords
        color_keywords = {
            "red": "red", "blue": "blue", "green": "green",
            "yellow": "yellow", "orange": "orange", "purple": "purple"
        }
        
        for keyword, color in color_keywords.items():
            if keyword in command.lower():
                intents.append(ParsedIntent(
                    type="COLOR",
                    target=None,
                    value=color,
                    confidence=0.70,
                    reason=f"Keyword fallback: found '{keyword}'",
                    matches={}
                ))
        
        return intents
