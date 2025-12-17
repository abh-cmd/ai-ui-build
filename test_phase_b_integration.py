#!/usr/bin/env python
"""Quick test of Phase B integration."""

from backend.agentic import AgenticAgent
import copy

agent = AgenticAgent()
bp = {
    'tokens': {'primary_color': '#2C3E50'},
    'components': [
        {'id': 'btn1', 'type': 'button', 'text': 'Click me', 'role': 'button'}
    ]
}

# Test: Make it look fancier
result = agent.process('Make it look fancier', copy.deepcopy(bp))
print(f'Make it fancier: success={result.get("success")}, confidence={result.get("confidence"):.1%}')

# Test: Make button bigger
result = agent.process('Make button bigger', copy.deepcopy(bp))
print(f'Make button bigger: success={result.get("success")}, confidence={result.get("confidence"):.1%}')

# Test: Change button color to red
result = agent.process('Change button color to red', copy.deepcopy(bp))
print(f'Change to red: success={result.get("success")}, confidence={result.get("confidence"):.1%}')
