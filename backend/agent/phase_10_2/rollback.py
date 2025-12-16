"""
PHASE 10.2 Rollback Manager
Handles blueprint snapshots and state recovery.
"""

import copy
import time
from typing import List, Optional, Dict, Any
from backend.agent.phase_10_2.models import RollbackSnapshot


class RollbackManager:
    """
    Manages blueprint snapshots and rollback capabilities.
    Maintains history for safe recovery on failure.
    """
    
    def __init__(self, max_snapshots: int = 100):
        """
        Initialize rollback manager.
        
        Args:
            max_snapshots: Maximum snapshots to keep in memory
        """
        self.snapshots: List[RollbackSnapshot] = []
        self.max_snapshots = max_snapshots
    
    def create_snapshot(self, step_id: int, blueprint: Dict[str, Any]) -> RollbackSnapshot:
        """
        Create a snapshot of the blueprint before a step.
        
        Args:
            step_id: ID of the step about to execute
            blueprint: Current blueprint state
            
        Returns:
            RollbackSnapshot
        """
        # Deep copy to ensure no references to original
        blueprint_copy = copy.deepcopy(blueprint)
        
        snapshot = RollbackSnapshot(
            step_id=step_id,
            blueprint=blueprint_copy,
            timestamp=time.time(),
        )
        
        self.snapshots.append(snapshot)
        
        # Trim if too many snapshots
        if len(self.snapshots) > self.max_snapshots:
            self.snapshots = self.snapshots[-self.max_snapshots:]
        
        return snapshot
    
    def get_latest_snapshot(self) -> Optional[RollbackSnapshot]:
        """Get the most recent snapshot"""
        return self.snapshots[-1] if self.snapshots else None
    
    def get_snapshot_before_step(self, step_id: int) -> Optional[RollbackSnapshot]:
        """Get snapshot from before a specific step"""
        for snapshot in reversed(self.snapshots):
            if snapshot.step_id < step_id:
                return snapshot
        return None
    
    def rollback_to_step(self, step_id: int) -> Optional[Dict[str, Any]]:
        """
        Rollback to the state before a specific step.
        
        Args:
            step_id: Step to rollback before
            
        Returns:
            Blueprint state before that step, or None if no snapshot found
        """
        snapshot = self.get_snapshot_before_step(step_id)
        if snapshot:
            # Return a deep copy so caller can't mutate our snapshot
            return copy.deepcopy(snapshot.blueprint)
        return None
    
    def rollback_to_latest_valid(self) -> Optional[Dict[str, Any]]:
        """
        Rollback to the most recent snapshot.
        
        Returns:
            Latest snapshot blueprint, or None if no snapshots
        """
        snapshot = self.get_latest_snapshot()
        if snapshot:
            return copy.deepcopy(snapshot.blueprint)
        return None
    
    def clear_snapshots(self) -> None:
        """Clear all snapshots"""
        self.snapshots = []
    
    def get_snapshot_history(self) -> List[Dict[str, Any]]:
        """Get a summary of all snapshots for debugging"""
        return [
            {
                "step_id": s.step_id,
                "timestamp": s.timestamp,
                "components_count": len(s.blueprint.get('components', [])),
            }
            for s in self.snapshots
        ]
