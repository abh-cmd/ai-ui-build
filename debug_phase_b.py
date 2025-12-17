#!/usr/bin/env python
"""Debug Phase B parser."""

from backend.agentic.intent_parser_enhanced import CompoundIntentParser

parser = CompoundIntentParser()

commands = [
    'Make it look fancier',
    'Make button bigger',
    'Change button color to red',
]

for cmd in commands:
    result = parser.parse_compound(cmd)
    print(f"\nCommand: '{cmd}'")
    print(f"  Intents found: {len(result.intents)}")
    print(f"  Confidence: {result.combined_confidence:.1%}")
    print(f"  Ambiguity: {result.ambiguity_level}")
    for i, intent in enumerate(result.intents):
        print(f"    Intent {i+1}: type={intent.type}, value={intent.value}, target={intent.target}, conf={intent.confidence:.1%}")
