"""
PHASE 10.2: Multi-Step Agentic Planning with Rollback
Public API for multi-step editing.
"""

from backend.agent.phase_10_2.models import (
    PlanStep, StepStatus, PlanStatus,
    RollbackSnapshot, StepExecutionResult,
    MultiStepPlan, MultiStepExecutionResult,
)
from backend.agent.phase_10_2.decomposer import MultiIntentDecomposer, ConflictDetector
from backend.agent.phase_10_2.rollback import RollbackManager
from backend.agent.phase_10_2.executor import MultiStepExecutor
from backend.agent.phase_10_2.orchestrator import MultiStepAgent, execute_multi_step_edit

__all__ = [
    # Models
    "PlanStep",
    "StepStatus",
    "PlanStatus",
    "RollbackSnapshot",
    "StepExecutionResult",
    "MultiStepPlan",
    "MultiStepExecutionResult",
    # Components
    "ConflictDetector",
    "MultiIntentDecomposer",
    "RollbackManager",
    "MultiStepExecutor",
    "MultiStepAgent",
    # Functions
    "execute_multi_step_edit",
]
