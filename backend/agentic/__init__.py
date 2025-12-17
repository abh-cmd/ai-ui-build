"""
PHASE 11: AGENTIC AI CORE
Deterministic, production-grade agentic intelligence engine for design edits.

Pipeline: INTENT → PLAN → PATCH → SIMULATE → VERIFY → APPLY → EXPLAIN

This module upgrades /edit/enhance into a true agentic system while preserving:
- Phase 10.2 determinism and rollback guarantees
- API contracts and response schemas
- Blueprint immutability
- Validator enforcement
"""

from .intent_graph import IntentGraph, Intent
from .planner import Planner, ExecutionPlan
from .patch_generator import PatchGenerator, JSONPatch
from .simulator import Simulator, SimulationResult
from .verifier import Verifier, VerificationResult
from .explainer import Explainer
from .agent import AgenticAgent

__all__ = [
    "IntentGraph",
    "Intent",
    "Planner",
    "ExecutionPlan",
    "PatchGenerator",
    "JSONPatch",
    "Simulator",
    "SimulationResult",
    "Verifier",
    "VerificationResult",
    "Explainer",
    "AgenticAgent",
]
