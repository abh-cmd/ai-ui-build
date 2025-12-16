from backend.agent.phase_10_2.decomposer import MultiIntentDecomposer

# Test blueprint
test_blueprint = {
    "id": "main_layout",
    "type": "container",
    "components": [
        {"id": "header", "type": "text", "text": "Welcome", "color": "#000000", "size": 24},
        {"id": "product_section", "type": "container", "components": [
            {"id": "product_1", "type": "product_card", "text": "Product A", "color": "#FFFFFF"}
        ]},
        {"id": "cta_button", "type": "button", "text": "Click Me", "color": "#FF0000"}
    ]
}

decomposer = MultiIntentDecomposer()
plan = decomposer.decompose("Make header smaller", test_blueprint)

print(f"Status: {plan.status}")
print(f"Steps: {len(plan.steps)}")
for step in plan.steps:
    print(f"\nStep {step.step_id}:")
    print(f"  Intent: {step.intent_type}")
    print(f"  Target: {step.target}")
    print(f"  Parameters: {step.parameters}")
    print(f"  Command: {step.command}")
