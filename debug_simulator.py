#!/usr/bin/env python
"""Debug simulator."""

from backend.agentic.simulator import Simulator
from backend.agentic.patch_generator import JSONPatch
import copy

simulator = Simulator()
bp = {
    'tokens': {'primary_color': '#2C3E50'},
    'components': [
        {
            'id': 'btn1',
            'type': 'button',
            'text': 'Click me',
            'role': 'button',
            'bbox': [50, 100, 200, 150],
            'visual': {'font_size': 16, 'height': 40}
        }
    ]
}

patches = [
    JSONPatch(op='replace', path='/components/0/visual/height', value=48)
]

print(f"Original blueprint: {bp}")
print(f"\nPatches: {patches}")

result = simulator.simulate(bp, patches)

print(f"\nSimulation result:")
print(f"  Safe: {result.safe}")
print(f"  Reason: {result.reason}")
print(f"  Risk score: {result.risk_score:.1%}")
print(f"  Warnings: {result.warnings}")

if result.modified_blueprint:
    print(f"\nModified blueprint height: {result.modified_blueprint['components'][0]['visual'].get('height')}")
