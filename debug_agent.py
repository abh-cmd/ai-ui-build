#!/usr/bin/env python
"""Debug agent processing."""

from backend.agentic import AgenticAgent
import copy
import json

agent = AgenticAgent()
bp = {
    'tokens': {'primary_color': '#2C3E50'},
    'components': [
        {'id': 'btn1', 'type': 'button', 'text': 'Click me', 'role': 'button'}
    ]
}

# Test
result = agent.process('Make button bigger', copy.deepcopy(bp))
print(json.dumps(result, indent=2, default=str))
