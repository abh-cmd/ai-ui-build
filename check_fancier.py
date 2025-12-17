#!/usr/bin/env python
"""Check what Phase 11 basic parser does with 'Make it look fancier'."""

from backend.agentic.intent_graph import IntentGraph

parser = IntentGraph()

command = 'Make it look fancier'
intents = parser.parse(command, {})

print(f"Command: '{command}'")
print(f"Phase 11 intents: {len(intents)}")

for i in intents:
    print(f"  - {i.type.value}: target={i.target}, value={i.value}, conf={i.confidence:.1%}")

if not intents:
    print("  (No keywords matched - expected result)")
