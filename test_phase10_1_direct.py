from backend.agent import DesignEditAgent

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

agent = DesignEditAgent()

# Test different commands with Phase 10.1
test_commands = [
    "make header bigger",
    "make header smaller",
    "Make header smaller",
    "change header color to red",
]

for cmd in test_commands:
    print(f"\nTesting with Phase 10.1: '{cmd}'")
    try:
        result = agent.edit(cmd, test_blueprint)
        print(f"Status: {result.status}")
        if result.errors:
            print(f"Errors: {result.errors}")
    except Exception as e:
        print(f"Exception: {e}")
