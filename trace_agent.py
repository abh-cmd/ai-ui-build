#!/usr/bin/env python
"""Detailed trace of agent processing."""

from backend.agentic import AgenticAgent
from backend.agentic.intent_graph import IntentGraph
from backend.agentic.intent_parser_enhanced import CompoundIntentParser
import copy

agent = AgenticAgent()
bp_orig = {
    'tokens': {'primary_color': '#2C3E50'},
    'components': [
        {'id': 'btn1', 'type': 'button', 'text': 'Click me', 'role': 'button', 'bbox': [50, 100, 200, 150], 'visual': {'font_size': 16}}
    ]
}

command = 'Make button bigger'
bp = copy.deepcopy(bp_orig)

# Step 1: Try Phase 11 parser
print("Step 1: Phase 11 IntentGraph parser")
intents_11 = agent.intent_graph.parse(command, bp)
print(f"  Result: {len(intents_11)} intents")
if intents_11:
    for i in intents_11:
        print(f"    - {i.type.value}: target={i.target}, value={i.value}")

# Step 2: If no intents, try Phase B
if not intents_11:
    print("\nStep 2: Phase B CompoundIntentParser (fallback)")
    phase_b_result = agent.compound_parser.parse_compound(command)
    print(f"  Intents: {len(phase_b_result.intents)}")
    print(f"  Confidence: {phase_b_result.combined_confidence:.1%}")
    print(f"  Ambiguity: {phase_b_result.ambiguity_level}")
    
    for i in phase_b_result.intents:
        print(f"    - {i.type}: target={i.target}, value={i.value}, conf={i.confidence:.1%}")
    
    # Step 3: Convert to Phase 11 format
    print("\nStep 3: Convert Phase B intents to Phase 11 format")
    converted = agent._convert_phase_b_intents(phase_b_result.intents)
    for i in converted:
        print(f"    - {i.type.value}: target={i.target}, value={i.value}, conf={i.confidence:.1%}")
    
    # Step 4: Try planning
    print("\nStep 4: Planning")
    plan = agent.planner.plan(converted)
    print(f"  Plan: {plan}")
    
    # Step 5: Try patch generation
    print("\nStep 5: Patch Generation")
    patches = []
    for intent in converted:
        intent_patches = agent.patch_generator.generate(intent, bp)
        print(f"  Intent {intent.type.value} -> {len(intent_patches)} patches")
        patches.extend(intent_patches)
    
    print(f"  Total patches: {len(patches)}")
    for p in patches:
        print(f"    - {p}")
