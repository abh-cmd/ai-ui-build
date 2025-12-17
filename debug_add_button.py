#!/usr/bin/env python
"""Debug add button command."""

from backend.agentic import AgenticAgent
import copy
import json

agent = AgenticAgent()
bp = {
    'tokens': {'primary_color': '#2C3E50', 'accent_color': '#E74C3C', 'spacing': 16, 'font_scale': 1.0, 'base_spacing': 8},
    'components': [
        {'id': 'title_1', 'type': 'text', 'text': 'Menu', 'bbox': [20, 20, 200, 60], 'visual': {'font_size': 32, 'color': '#2C3E50'}},
        {'id': 'cta_1', 'type': 'button', 'text': 'Order Now', 'bbox': [50, 220, 250, 280], 'visual': {'color': '#E74C3C', 'height': 50}, 'role': 'cta'}
    ]
}

command = 'Add a button that says Delivery'

result = agent.process(command, copy.deepcopy(bp))
print(f"Result:")
print(f"  Success: {result.get('success')}")
print(f"  Confidence: {result.get('confidence'):.1%}")

if result.get('success'):
    modified = result.get('modified_blueprint', {})
    components = modified.get('components', [])
    print(f"  Components: {len(components)}")
    for c in components:
        print(f"    - {c.get('id')}: text={c.get('text')}")
else:
    print(f"  Reasoning: {result.get('reasoning')}")
