"""
PLANNER: Convert intents into ordered execution plan.

Transforms [Intent] → ExecutionPlan with proper ordering and validation.
Ensures: validate → execute → verify (deterministic sequence)
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum


class ExecutionStep(str, Enum):
    """Deterministic execution steps in pipeline."""
    VALIDATE = "validate"
    PATCH = "patch"
    VERIFY = "verify"


@dataclass
class ExecutionPlan:
    """Ordered list of steps to execute intents."""
    steps: List[Dict[str, Any]]
    intents: List[Any]  # Original intents
    sequence: List[str]  # Order of execution
    is_safe: bool = True
    reason: Optional[str] = None


class Planner:
    """Plan execution of intents deterministically."""
    
    def plan(self, intents: List[Any]) -> ExecutionPlan:
        """
        Convert intents into execution plan.
        
        Deterministic: Same intents always produce same plan.
        
        Args:
            intents: List of Intent objects from intent_graph
        
        Returns:
            ExecutionPlan with ordered steps
        """
        if not intents:
            return ExecutionPlan(
                steps=[],
                intents=[],
                sequence=[]
            )
        
        steps: List[Dict[str, Any]] = []
        sequence: List[str] = []
        
        # Step 1: VALIDATE intents
        steps.append({
            "type": ExecutionStep.VALIDATE,
            "description": f"Validate {len(intents)} intents against schema",
            "intents": intents
        })
        sequence.append(ExecutionStep.VALIDATE)
        
        # Step 2: PATCH for each intent (deterministic order)
        # Order: Delete → Create → Style → Position → Size → Color (deterministic)
        ordered_intents = self._order_intents(intents)
        
        for idx, intent in enumerate(ordered_intents):
            steps.append({
                "type": ExecutionStep.PATCH,
                "index": idx,
                "intent": intent,
                "description": f"Apply {intent.type} to {intent.target or 'page'}"
            })
        sequence.append(ExecutionStep.PATCH)
        
        # Step 3: VERIFY final state
        steps.append({
            "type": ExecutionStep.VERIFY,
            "description": "Verify final blueprint validity and safety",
            "checks": ["schema", "accessibility", "layout", "tokens"]
        })
        sequence.append(ExecutionStep.VERIFY)
        
        return ExecutionPlan(
            steps=steps,
            intents=intents,
            sequence=sequence,
            is_safe=True
        )
    
    def _order_intents(self, intents: List[Any]) -> List[Any]:
        """
        Order intents deterministically.
        
        Order: DELETE → CREATE → VISIBILITY → STYLE → POSITION → RESIZE → COLOR
        This prevents conflicts (e.g., deleting before resizing, creating before styling)
        """
        from .intent_graph import IntentType
        
        # Define order priority (lower = execute first)
        order = {
            IntentType.DELETE: 0,
            IntentType.CREATE: 1,
            IntentType.VISIBILITY: 2,
            IntentType.STYLE: 3,
            IntentType.POSITION: 4,
            IntentType.RESIZE: 5,
            IntentType.ALIGN: 6,
            IntentType.TEXT: 7,
            IntentType.COLOR: 8,
        }
        
        # Sort by order, then by original position (stable sort = deterministic)
        return sorted(
            intents,
            key=lambda i: (order.get(i.type, 99), intents.index(i))
        )
    
    def detect_conflicts(self, intents: List[Any]) -> Optional[str]:
        """
        Detect impossible operation sequences.
        
        Returns: Error message if conflict found, None otherwise
        """
        from .intent_graph import IntentType
        
        # Track what operations are on same target
        operations_by_target = {}
        
        for intent in intents:
            target = intent.target or "page"
            if target not in operations_by_target:
                operations_by_target[target] = []
            operations_by_target[target].append(intent.type)
        
        # Check for impossible combinations
        for target, ops in operations_by_target.items():
            # Can't delete and then modify
            if IntentType.DELETE in ops and len(ops) > 1:
                return f"Cannot modify component after deleting it"
            
            # Can't hide and then modify visibility
            if IntentType.VISIBILITY in ops and ops.count(IntentType.VISIBILITY) > 1:
                return f"Conflicting visibility operations on {target}"
        
        return None
    
    def estimate_complexity(self, intents: List[Any]) -> int:
        """Estimate complexity of execution plan (1-10 scale)."""
        complexity = 1
        
        # +1 per intent
        complexity += len(intents)
        
        # +2 if multiple intents on same target
        from collections import Counter
        targets = Counter(i.target for i in intents)
        if any(count > 1 for count in targets.values()):
            complexity += 2
        
        return min(10, complexity)
