#!/usr/bin/env python
"""Debug color commands."""

from backend.agentic.intent_parser_enhanced import CompoundIntentParser

parser = CompoundIntentParser()

commands = [
    'Change color to red',
    'Make button red',
    'Make it look fancier',
]

for cmd in commands:
    result = parser.parse_compound(cmd)
    print(f"\nCommand: '{cmd}'")
    print(f"  Intents: {len(result.intents)}")
    print(f"  Confidence: {result.combined_confidence:.1%}")
    print(f"  Ambiguity: {result.ambiguity_level}")
    
    for i in result.intents:
        print(f"    - {i.type}: value={i.value}, target={i.target}, conf={i.confidence:.1%}")
