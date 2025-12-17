#!/usr/bin/env python
"""Debug patch generation."""

from backend.agentic.intent_graph import IntentGraph, Intent, IntentType
from backend.agentic.patch_generator import PatchGenerator
import json

pg = PatchGenerator()

bp = {
    'tokens': {'primary_color': '#2C3E50'},
    'components': [
        {'id': 'btn1', 'type': 'button', 'text': 'Click me', 'role': 'button', 'bbox': [50, 100, 200, 150]}
    ]
}

# Create intent manually
intent = Intent(
    type=IntentType.RESIZE,
    target='button',
    value='large',
    confidence=0.95,
    params={}
)

print(f"Intent: {intent}")
print(f"Generating patches...")

patches = pg.generate(intent, bp)
print(f"Patches generated: {len(patches)}")

for i, patch in enumerate(patches):
    print(f"  Patch {i+1}: {patch}")
