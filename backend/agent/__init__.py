"""
PHASE 10.1 — AGENTIC AI CORE

5-step deterministic design editing pipeline:
1. Intent Parser - Parse NL commands
2. Planner - Generate safe plans
3. Patcher - Apply patches
4. Verifier - Verify safety
5. Agent Runner - Orchestrate all steps

Public API:
    from backend.agent import run_agent, DesignEditAgent, AgentResult
"""

from .result import AgentResult
from .intent_parser import IntentParser, ParsedIntent, IntentType, ComponentTarget
from .planner import Planner, ChangePlan, ComponentPatch, FieldPatch
from .patcher import Patcher
from .verifier import Verifier
from .agent_runner import DesignEditAgent, run_agent

__all__ = [
    "AgentResult",
    "IntentParser",
    "ParsedIntent",
    "IntentType",
    "ComponentTarget",
    "Planner",
    "ChangePlan",
    "ComponentPatch",
    "FieldPatch",
    "Patcher",
    "Verifier",
    "DesignEditAgent",
    "run_agent",
]
