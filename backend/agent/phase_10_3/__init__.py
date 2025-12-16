"""
PHASE 10.3: Advanced Optimization & Scaling
Production-grade performance optimization and scaling.
"""

from backend.agent.phase_10_3.profiler import PipelineProfiler, ExecutionProfile
from backend.agent.phase_10_3.optimizer import OptimizedMultiStepAgent
from backend.agent.phase_10_3.batch_processor import BatchProcessor, BatchResult
from backend.agent.phase_10_3.error_recovery import ErrorRecoveryManager

__all__ = [
    # Profiling
    "PipelineProfiler",
    "ExecutionProfile",
    # Optimization
    "OptimizedMultiStepAgent",
    # Batch Processing
    "BatchProcessor",
    "BatchResult",
    # Error Recovery
    "ErrorRecoveryManager",
]
