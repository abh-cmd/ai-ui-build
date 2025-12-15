"""
PHASE 6.1: Command Validator
Enforces UX Contract rules. NO backend edit logic - only validation.
"""

import re


class CommandValidationError(Exception):
    """Raised when command violates UX contract"""
    pass


class CommandValidator:
    """Validates commands against frozen UX contract"""
    
    # Valid command starters (imperative verbs)
    VALID_STARTERS = {
        "make", "change", "increase", "decrease", "add", "remove",
        "move", "adjust", "set", "update", "modify", "enlarge", "shrink",
        "expand", "reduce", "boost", "lower", "raise", "bump"
    }
    
    # Vague/rejected command patterns
    REJECTED_PATTERNS = [
        r"redesign",
        r"make it (modern|better|clean|fancy|nice|cool|pretty|amazing|awesome)",
        r"improve\s+(ux|ui|experience)",
        r"enhance\s+(design|appearance|look)",
        r"update\s+(everything|the|design)",
        r"(add|make|create)\s+(a\s+)?(new\s+)?(dark\s+)?mode",
        r"(add|create|remove|delete)\s+(a\s+)?(new\s+)?(button|header|image|card|component|section|footer)",
        r"animate",
        r"add\s+hover",
        r"add\s+effect",
        r"reorganize",
        r"restructure",
    ]
    
    # Unsupported keywords (valid command but not yet implemented)
    UNSUPPORTED_KEYWORDS = {
        "animate", "animation", "hover", "effect", "transition",
        "shadow", "blur", "gradient", "glow"
    }
    
    @staticmethod
    def validate(command: str) -> None:
        """
        Validate command against UX contract.
        
        Args:
            command: User's natural language command
            
        Raises:
            CommandValidationError: If command violates contract
        """
        
        if not command or not isinstance(command, str):
            raise CommandValidationError("Command must be non-empty string")
        
        command = command.strip().lower()
        
        # Length check
        words = command.split()
        if len(words) < 2:
            raise CommandValidationError("Command too short (min 2 words)")
        if len(words) > 50:
            raise CommandValidationError("Command too long (max 50 words)")
        
        # Check for empty or gibberish
        if all(len(w) <= 2 for w in words):
            raise CommandValidationError("Command appears to be gibberish")
        
        # Check rejected patterns
        for pattern in CommandValidator.REJECTED_PATTERNS:
            if re.search(pattern, command):
                raise CommandValidationError(
                    f"Invalid command: too vague or unsupported"
                )
        
        # Check for unsupported keywords
        for keyword in CommandValidator.UNSUPPORTED_KEYWORDS:
            if keyword in command:
                raise CommandValidationError(
                    f"Unsupported feature: {keyword}"
                )
        
        # Check command starts with imperative verb
        first_word = words[0].rstrip(",")
        if first_word not in CommandValidator.VALID_STARTERS:
            raise CommandValidationError(
                f"Command must start with action verb (e.g., 'Make', 'Change')"
            )
        
        # Require at least one valid target word
        valid_targets = {
            "button", "header", "title", "text", "image", "color", "size",
            "spacing", "padding", "margin", "font", "cta", "product",
            "width", "height", "larger", "bigger", "smaller", "bolder",
            "brighter", "darker", "primary", "accent", "heading", "content"
        }
        
        if not any(target in words for target in valid_targets):
            raise CommandValidationError(
                "Command must reference valid target (e.g., button, color, size)"
            )


# Quick validation without exceptions
def is_valid_command(command: str) -> tuple[bool, str]:
    """
    Check if command is valid.
    
    Returns:
        (is_valid, error_message)
    """
    try:
        CommandValidator.validate(command)
        return True, ""
    except CommandValidationError as e:
        return False, str(e)
