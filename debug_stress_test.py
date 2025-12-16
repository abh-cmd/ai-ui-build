from backend.agent.phase_10_2 import execute_multi_step_edit

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

# Valid and invalid commands for stress test
valid_commands = [
    "Make header smaller and change its color to blue",
    "Change product section text to sale",
    "Make cta_button bigger",
    "Change header color to red",
    "Make header smaller",
    "Change cta_button color to green",
]

invalid_commands = [
    "Change header to purple and delete it",
    "Make nonexistent component bigger",
    "Delete header and resize it",
]

print("Testing valid commands:")
for i, cmd in enumerate(valid_commands):
    result = execute_multi_step_edit(cmd, test_blueprint)
    status = "✓" if result.status == "success" else "✗"
    print(f"{status} {i+1}. '{cmd}' -> {result.status}")

print("\nTesting invalid commands:")
for i, cmd in enumerate(invalid_commands):
    result = execute_multi_step_edit(cmd, test_blueprint)
    status = "✓" if result.status != "success" else "✗"
    print(f"{status} {i+1}. '{cmd}' -> {result.status}")
