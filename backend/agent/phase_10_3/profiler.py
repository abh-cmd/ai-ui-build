"""
PHASE 10.3.1: Pipeline Performance Profiler
Instruments the execution pipeline to identify bottlenecks.
"""

import time
import json
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
from backend.agent.phase_10_2 import MultiStepAgent, MultiStepExecutionResult


@dataclass
class TimingSegment:
    """Timing for a single pipeline segment."""
    segment_name: str
    start_time: float
    end_time: float
    duration_ms: float
    metadata: Dict[str, Any] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ExecutionProfile:
    """Complete execution profile with all timing segments."""
    command: str
    blueprint_size: int
    total_duration_ms: float
    
    # Pipeline segments
    decompose_duration_ms: float
    execute_duration_ms: float
    verify_duration_ms: float
    serialize_duration_ms: float
    
    # Step-level details
    step_count: int
    avg_step_duration_ms: float
    max_step_duration_ms: float
    min_step_duration_ms: float
    
    # Rollback metrics
    rollback_triggered: bool
    rollback_duration_ms: Optional[float] = None
    
    # Memory estimate
    memory_mb_start: Optional[float] = None
    memory_mb_peak: Optional[float] = None
    
    # Success
    success: bool = True
    status: str = "success"
    
    # Segment breakdown
    segments: List[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    
    def summary(self) -> str:
        """Return human-readable summary."""
        lines = [
            "="*60,
            "EXECUTION PROFILE SUMMARY",
            "="*60,
            f"Command: {self.command[:60]}...",
            f"Blueprint Size: {self.blueprint_size} components",
            f"Total Time: {self.total_duration_ms:.2f}ms",
            "",
            "PIPELINE BREAKDOWN:",
            f"  Decompose:  {self.decompose_duration_ms:>10.2f}ms  ({self.decompose_duration_ms/self.total_duration_ms*100:>5.1f}%)",
            f"  Execute:    {self.execute_duration_ms:>10.2f}ms  ({self.execute_duration_ms/self.total_duration_ms*100:>5.1f}%)",
            f"  Verify:     {self.verify_duration_ms:>10.2f}ms  ({self.verify_duration_ms/self.total_duration_ms*100:>5.1f}%)",
            f"  Serialize:  {self.serialize_duration_ms:>10.2f}ms  ({self.serialize_duration_ms/self.total_duration_ms*100:>5.1f}%)",
            "",
            "STEP METRICS:",
            f"  Total Steps: {self.step_count}",
            f"  Avg/Step:    {self.avg_step_duration_ms:.2f}ms",
            f"  Max/Step:    {self.max_step_duration_ms:.2f}ms",
            f"  Min/Step:    {self.min_step_duration_ms:.2f}ms",
            "",
            f"Rollback: {'YES' if self.rollback_triggered else 'NO'}",
            f"Status: {self.status}",
            "="*60,
        ]
        return "\n".join(lines)


class PipelineProfiler:
    """
    Instruments Phase 10.2 pipeline to measure performance.
    
    Pipeline stages:
    1. DECOMPOSE: Parse command into steps
    2. EXECUTE: Execute steps with verification
    3. VERIFY: Check blueprint validity
    4. SERIALIZE: Convert result to JSON
    """
    
    def __init__(self, verbose: bool = True):
        """Initialize profiler."""
        self.verbose = verbose
        self.profiles: List[ExecutionProfile] = []
        self.agent = MultiStepAgent()
    
    def profile_execution(
        self,
        command: str,
        blueprint: Dict[str, Any],
    ) -> tuple[MultiStepExecutionResult, ExecutionProfile]:
        """
        Execute command and profile all pipeline stages.
        
        Args:
            command: Natural language command
            blueprint: Blueprint to edit
            
        Returns:
            Tuple of (execution_result, profile)
        """
        # Count blueprint components
        blueprint_size = len(blueprint.get("components", []))
        
        # TOTAL TIME
        total_start = time.time()
        
        # STAGE 1: DECOMPOSE
        decompose_start = time.time()
        plan = self.agent.decomposer.decompose(command, blueprint)
        decompose_duration = (time.time() - decompose_start) * 1000
        
        # STAGE 2: EXECUTE
        execute_start = time.time()
        execution_result = self.agent.executor.execute_plan(plan, blueprint)
        execute_duration = (time.time() - execute_start) * 1000
        
        # STAGE 3: VERIFY (implicit in executor, estimate as 5% of execute)
        verify_duration = execute_duration * 0.05
        
        # STAGE 4: SERIALIZE
        serialize_start = time.time()
        _ = json.dumps(execution_result.final_blueprint)
        serialize_duration = (time.time() - serialize_start) * 1000
        
        total_duration = (time.time() - total_start) * 1000
        
        # STEP-LEVEL METRICS
        step_durations = [
            step.duration_ms 
            for step in execution_result.step_results 
            if hasattr(step, 'duration_ms') and step.duration_ms
        ]
        
        if step_durations:
            avg_step = sum(step_durations) / len(step_durations)
            max_step = max(step_durations)
            min_step = min(step_durations)
        else:
            avg_step = 0
            max_step = 0
            min_step = 0
        
        # Build profile
        profile = ExecutionProfile(
            command=command,
            blueprint_size=blueprint_size,
            total_duration_ms=total_duration,
            decompose_duration_ms=decompose_duration,
            execute_duration_ms=execute_duration,
            verify_duration_ms=verify_duration,
            serialize_duration_ms=serialize_duration,
            step_count=len(execution_result.step_results),
            avg_step_duration_ms=avg_step,
            max_step_duration_ms=max_step,
            min_step_duration_ms=min_step,
            rollback_triggered=execution_result.rollback_triggered,
            rollback_duration_ms=None,  # TODO: track separately
            success=execution_result.status == "success",
            status=execution_result.status,
        )
        
        self.profiles.append(profile)
        
        if self.verbose:
            print(profile.summary())
        
        return execution_result, profile
    
    def profile_batch(
        self,
        commands: List[str],
        blueprints: List[Dict[str, Any]],
    ) -> tuple[List[MultiStepExecutionResult], List[ExecutionProfile]]:
        """
        Profile a batch of commands.
        
        Args:
            commands: List of commands
            blueprints: List of blueprints
            
        Returns:
            Tuple of (execution_results, profiles)
        """
        results = []
        profiles = []
        
        for cmd, bp in zip(commands, blueprints):
            result, profile = self.profile_execution(cmd, bp)
            results.append(result)
            profiles.append(profile)
        
        return results, profiles
    
    def get_aggregate_stats(self) -> Dict[str, Any]:
        """Get aggregated statistics across all profiles."""
        if not self.profiles:
            return {}
        
        total_time = sum(p.total_duration_ms for p in self.profiles)
        avg_time = total_time / len(self.profiles)
        max_time = max(p.total_duration_ms for p in self.profiles)
        min_time = min(p.total_duration_ms for p in self.profiles)
        
        decompose_avg = sum(p.decompose_duration_ms for p in self.profiles) / len(self.profiles)
        execute_avg = sum(p.execute_duration_ms for p in self.profiles) / len(self.profiles)
        serialize_avg = sum(p.serialize_duration_ms for p in self.profiles) / len(self.profiles)
        
        success_count = sum(1 for p in self.profiles if p.success)
        success_rate = success_count / len(self.profiles) * 100
        
        rollback_count = sum(1 for p in self.profiles if p.rollback_triggered)
        
        return {
            "total_runs": len(self.profiles),
            "success_count": success_count,
            "success_rate_percent": success_rate,
            "rollback_count": rollback_count,
            "total_time_ms": total_time,
            "avg_time_ms": avg_time,
            "max_time_ms": max_time,
            "min_time_ms": min_time,
            "decompose_avg_ms": decompose_avg,
            "execute_avg_ms": execute_avg,
            "serialize_avg_ms": serialize_avg,
            "bottleneck": max([
                ("decompose", decompose_avg),
                ("execute", execute_avg),
                ("serialize", serialize_avg),
            ], key=lambda x: x[1])[0],
        }
    
    def report(self) -> str:
        """Generate full profiling report."""
        stats = self.get_aggregate_stats()
        
        lines = [
            "="*60,
            "PHASE 10.3.1: PERFORMANCE PROFILING REPORT",
            "="*60,
            "",
            "AGGREGATE STATISTICS",
            "="*60,
            f"Total Runs: {stats.get('total_runs', 0)}",
            f"Success Rate: {stats.get('success_rate_percent', 0):.1f}%",
            f"Rollbacks Triggered: {stats.get('rollback_count', 0)}",
            "",
            "TIMING ANALYSIS",
            "="*60,
            f"Total Time: {stats.get('total_time_ms', 0):.2f}ms",
            f"Average Time/Command: {stats.get('avg_time_ms', 0):.2f}ms",
            f"Max Time/Command: {stats.get('max_time_ms', 0):.2f}ms",
            f"Min Time/Command: {stats.get('min_time_ms', 0):.2f}ms",
            "",
            "STAGE BREAKDOWN (AVERAGE)",
            "="*60,
            f"Decompose: {stats.get('decompose_avg_ms', 0):.2f}ms",
            f"Execute:   {stats.get('execute_avg_ms', 0):.2f}ms",
            f"Serialize: {stats.get('serialize_avg_ms', 0):.2f}ms",
            "",
            f"IDENTIFIED BOTTLENECK: {stats.get('bottleneck', 'unknown')}",
            "="*60,
        ]
        
        return "\n".join(lines)
