#!/usr/bin/env python
"""Full trace of 'Change color to red' command."""

from backend.agentic import AgenticAgent
import copy

agent = AgenticAgent()
bp = {
    'tokens': {'primary_color': '#2C3E50', 'base_spacing': 8},
    'components': [
        {
            'id': 'btn1',
            'type': 'button',
            'text': 'Click me',
            'bbox': [50, 100, 200, 160],
            'visual': {'color': '#333', 'height': 50},
            'role': 'cta'
        }
    ]
}

command = 'Change color to red'

result = agent.process(command, copy.deepcopy(bp))
print(f"Result:")
print(f"  Success: {result.get('success')}")
print(f"  Confidence: {result.get('confidence'):.1%}")
print(f"  Reasoning: {result.get('reasoning')}")

if not result.get('success'):
    print(f"  Details: {result.get('details')}")
