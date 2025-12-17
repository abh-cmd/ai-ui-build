#!/usr/bin/env python
"""Debug text change command."""

from backend.agentic import AgenticAgent
import copy
import json

agent = AgenticAgent()
bp = {
    'tokens': {'primary_color': '#2C3E50', 'base_spacing': 8},
    'components': [
        {
            'id': 'cta_1',
            'type': 'button',
            'text': 'Order Now',
            'bbox': [50, 220, 250, 260],
            'visual': {'color': '#E74C3C', 'height': 40},
            'role': 'cta'
        }
    ]
}

command = 'Change button text to Reserve'

# Parse via Phase B
result = agent.compound_parser.parse_compound(command)
print(f"Phase B parse result:")
print(f"  Intents: {len(result.intents)}")
print(f"  Confidence: {result.combined_confidence:.1%}")

for i in result.intents:
    print(f"    - {i.type}: value={i.value}, target={i.target}")

# Try agent
result = agent.process(command, copy.deepcopy(bp))
print(f"\nAgent result:")
print(f"  Success: {result.get('success')}")
print(f"  Confidence: {result.get('confidence'):.1%}")
print(f"  Reasoning: {result.get('reasoning')}")
