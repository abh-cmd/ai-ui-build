from backend.agent import DesignEditAgent

# Test blueprint
test_blueprint = {
    "id": "main_layout",
    "type": "container",
    "components": [
        {"id": "header", "type": "text", "text": "Welcome", "color": "#000000", "size": 24},
    ]
}

agent = DesignEditAgent()
cmd = "make header bigger"
print(f"Testing with Phase 10.1: '{cmd}'")
result = agent.edit(cmd, test_blueprint)
print(f"Result type: {type(result)}")
print(f"Result attributes: {dir(result)}")
print(f"Result: {result}")
