from backend.agent.phase_10_2 import execute_multi_step_edit

# Test blueprint (with proper roles for Phase 10.1)
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
        {
            "id": "product_section",
            "type": "container",
            "text": "Products",
            "role": "content",
            "bbox": [10, 60, 480, 200],
            "visual": {"color": "#000000", "height": 200}
        },
        {
            "id": "cta_button",
            "type": "button",
            "text": "Get Started",
            "role": "cta",
            "bbox": [10, 270, 200, 50],
            "visual": {"color": "#FFFFFF", "bg_color": "#0000FF", "height": 50}
        },
    ]
}

# Test single command
cmd = "Make header smaller"
print(f"Testing: '{cmd}'")
result = execute_multi_step_edit(cmd, test_blueprint)
print(f"Status: {result.status}")
print(f"Steps executed: {result.steps_executed}/{result.steps_total}")
print(f"Rollback triggered: {result.rollback_triggered}")
if result.rollback_triggered:
    print(f"Rollback reason: {result.rollback_reason}")
print(f"Reasoning: {result.reasoning_trace}")
