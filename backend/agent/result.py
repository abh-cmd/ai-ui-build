"""
PHASE 10.1 — AGENT RESULT MODEL

Structured response from the design edit agent with full reasoning trace.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class AgentResult:
    """
    Structured result from design editing agent.
    
    Attributes:
        success: Whether edit was successful and applied
        patched_blueprint: Modified blueprint (None if failed)
        summary: Human-readable summary of changes
        changes_applied: List of field paths that changed
        confidence: Confidence in intent parsing (0.0-1.0)
        safe: Whether all safety checks passed
        reasoning: Step-by-step reasoning trace (all 5 steps)
        errors: Any errors encountered
    """
    success: bool
    patched_blueprint: Optional[Dict] = None
    summary: str = ""
    changes_applied: List[str] = field(default_factory=list)
    confidence: float = 0.0
    safe: bool = False
    reasoning: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
