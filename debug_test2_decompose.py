from backend.agent.phase_10_2.decomposer import MultiIntentDecomposer

decomposer = MultiIntentDecomposer()

# Blueprint with proper structure
test_blueprint = {
    "screen_id": "test",
    "tokens": {
        "colors": {
            "white": "#FFFFFF",
            "black": "#000000",
            "blue": "#0000FF",
            "red": "#FF0000",
            "green": "#00FF00",
        }
    },
    "components": [
        {
            "id": "header",
            "type": "header",
            "text": "Welcome",
            "role": "hero",
            "bbox": [10, 10, 480, 40],
            "visual": {"color": "#0000FF", "height": 40, "font_weight": "normal"}
        },
    ]
}

cmd = "Change header to green and invalid nonsense"
plan = decomposer.decompose(cmd, test_blueprint)

print(f"Status: {plan.status}")
print(f"Steps: {len(plan.steps)}")
for i, step in enumerate(plan.steps, 1):
    print(f"\nStep {i}:")
    print(f"  Command: {step.command}")
    print(f"  Intent: {step.intent_type}")
    print(f"  Target: {step.target}")
    print(f"  Parameters: {step.parameters}")

print(f"\nConflicts: {plan.conflicts}")
print(f"Reasoning: {plan.reasoning}")
