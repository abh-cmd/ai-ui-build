#!/usr/bin/env python
"""Full trace of agent processing."""

from backend.agentic import AgenticAgent
import copy

agent = AgenticAgent()
bp = {
    'tokens': {'primary_color': '#2C3E50'},
    'components': [
        {'id': 'btn1', 'type': 'button', 'text': 'Click me', 'role': 'button', 'bbox': [50, 100, 200, 150], 'visual': {'font_size': 16, 'height': 40}}
    ]
}

command = 'Make button bigger'

# Step 1: Parse intents
intents = agent.intent_graph.parse(command, bp)
print(f"1. Intents parsed: {len(intents)}")

# Step 2: Plan
plan = agent.planner.plan(intents)
print(f"2. Plan: {plan}")

# Step 3: Check conflicts
conflict = agent.planner.detect_conflicts(intents)
print(f"3. Conflict detection: {conflict}")

# Step 4: Generate patches
patches = []
for intent in intents:
    intent_patches = agent.patch_generator.generate(intent, bp)
    print(f"4. Patches for {intent.type.value}: {len(intent_patches)}")
    for p in intent_patches:
        print(f"   - {p}")
    patches.extend(intent_patches)

print(f"   Total patches: {len(patches)}")

# Step 5: Simulate
if patches:
    sim_result = agent.simulator.simulate(bp, patches)
    print(f"5. Simulation: safe={sim_result.safe}, reason={sim_result.reason}")
    
    if sim_result.modified_blueprint:
        modified = sim_result.modified_blueprint
        print(f"   Modified components: {len(modified.get('components', []))}")
        for c in modified.get('components', []):
            print(f"     - {c.get('id')}: {c.get('type')}")
