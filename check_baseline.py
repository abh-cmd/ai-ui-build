#!/usr/bin/env python
"""Quick Phase 10.2 baseline check."""

import sys
sys.path.insert(0, '.')

from backend.agent.phase_10_3.profiler import PipelineProfiler
from backend.agent.phase_10_2 import execute_multi_step_edit

bp = {
    'components': [
        {'id': 'c1', 'name': 'Card', 'styles': {}},
        {'id': 'c2', 'name': 'Button', 'styles': {}}
    ]
}

cmd = 'Make the first card red'
profiler = PipelineProfiler()

result = profiler.profile_execution(lambda: execute_multi_step_edit(cmd, bp), cmd)
print(f'Command: {cmd}')
print(f'Status: {result.overall_status}')
print(f'Total Time: {result.overall_time_ms:.2f}ms')
for stage, time_ms in result.stage_times_ms.items():
    pct = (time_ms / result.overall_time_ms * 100) if result.overall_time_ms > 0 else 0
    print(f'  {stage}: {time_ms:.2f}ms ({pct:.1f}%)')
