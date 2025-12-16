"""
PHASE 10.2 Multi-Step Execution Models
Data structures for multi-intent planning and execution.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from enum import Enum


class StepStatus(Enum):
    """Status of a single execution step"""
    PENDING = "pending"
    EXECUTING = "executing"
    SUCCESS = "success"
    FAILED = "failed"
    SKIPPED = "skipped"


class PlanStatus(Enum):
    """Status of entire multi-step plan"""
    VALID = "valid"
    CONFLICTED = "conflicted"
    REJECTED = "rejected"


@dataclass
class PlanStep:
    """
    Represents a single atomic edit step within a multi-step plan.
    
    Each step is independent and executable by Phase 10.1 agent.
    """
    step_id: int
    command: str  # The natural language command for this step
    intent_type: str  # e.g., "modify_color", "resize_component"
    target: Dict[str, Any]  # {role, type, id} component selector
    parameters: Dict[str, Any]  # {color, size, text, etc.}
    reasoning: str  # Why this step was extracted
    status: StepStatus = StepStatus.PENDING
    error: Optional[str] = None
    
    def __repr__(self) -> str:
        return f"Step {self.step_id}: {self.intent_type} on {self.target.get('id', '?')}"


@dataclass
class RollbackSnapshot:
    """
    Snapshot of blueprint state for rollback purposes.
    Captured before each step execution.
    """
    step_id: int
    blueprint: Dict[str, Any]
    timestamp: float  # Unix timestamp
    
    def __repr__(self) -> str:
        return f"Snapshot before step {self.step_id}"


@dataclass
class StepExecutionResult:
    """
    Result of executing a single step through Phase 10.1 agent.
    """
    step_id: int
    step: PlanStep
    success: bool
    safe: bool
    patched_blueprint: Optional[Dict[str, Any]] = None
    summary: str = ""
    errors: List[str] = field(default_factory=list)
    verification_passed: bool = False
    
    def __repr__(self) -> str:
        status = "SUCCESS" if self.success else "FAILED"
        return f"Step {self.step_id}: {status} (safe={self.safe})"


@dataclass
class MultiStepPlan:
    """
    Plan decomposed from a single complex command into ordered atomic steps.
    """
    original_command: str
    steps: List[PlanStep] = field(default_factory=list)
    status: PlanStatus = PlanStatus.VALID
    conflicts: List[str] = field(default_factory=list)  # Detected conflicts
    reasoning: List[str] = field(default_factory=list)  # How plan was generated
    confidence: float = 0.0  # Overall confidence in the plan
    
    def add_conflict(self, conflict_description: str) -> None:
        """Mark a detected conflict"""
        self.conflicts.append(conflict_description)
        self.status = PlanStatus.CONFLICTED
    
    def is_valid(self) -> bool:
        """Check if plan is valid (no conflicts)"""
        return self.status == PlanStatus.VALID and len(self.conflicts) == 0
    
    def __repr__(self) -> str:
        return f"MultiStepPlan({len(self.steps)} steps, {self.status.value})"


@dataclass
class MultiStepExecutionResult:
    """
    Final result of executing a complete multi-step plan.
    This is the user-facing output.
    """
    status: str  # "success", "failed", "partial", "conflicted"
    final_blueprint: Dict[str, Any]
    steps_executed: int
    steps_failed: int
    steps_total: int
    rollback_triggered: bool = False
    rollback_reason: Optional[str] = None
    changes_applied: List[str] = field(default_factory=list)  # List of successful changes
    confidence: float = 0.0
    reasoning_trace: List[str] = field(default_factory=list)
    step_results: List[StepExecutionResult] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to JSON-serializable dict"""
        return {
            "status": self.status,
            "final_blueprint": self.final_blueprint,
            "steps_executed": self.steps_executed,
            "steps_failed": self.steps_failed,
            "steps_total": self.steps_total,
            "rollback_triggered": self.rollback_triggered,
            "rollback_reason": self.rollback_reason,
            "changes_applied": self.changes_applied,
            "confidence": self.confidence,
            "reasoning_trace": self.reasoning_trace,
        }
    
    def __repr__(self) -> str:
        return f"MultiStepResult({self.status}, {self.steps_executed}/{self.steps_total} steps)"
