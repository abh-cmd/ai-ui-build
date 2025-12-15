"""Vision processing for blueprint extraction from images.

This module handles converting uploaded images to blueprint JSON.
It supports optional LLM-based vision via AI_MODE flag,
with automatic fallback to deterministic stub if LLM is unavailable.

Default behavior (AI_MODE=off): Uses deterministic stub for stability.
LLM behavior (AI_MODE=on): Attempts OpenAI vision, falls back to stub on error.

Environment Variables:
    AI_MODE: "on" or "off" (default "off")
    OPENAI_API_KEY: Required only if AI_MODE="on"
"""

import os
from backend.ai import llm_client
from backend.ai.vision_stub import (
    image_to_raw_json_stub,
    _create_storefront_blueprint,
    _create_content_blueprint,
    _create_landing_blueprint
)


def image_to_raw_json(image_path: str) -> dict:
    """
    Extract blueprint from image using LLM (if enabled) or fallback to stub.
    
    If AI_MODE=on:
    - Calls OpenAI vision to analyze image and extract blueprint JSON
    - Falls back to stub on API error, quota error, or parse failure
    
    If AI_MODE=off:
    - Returns deterministic stub blueprint
    
    Args:
        image_path: Path to uploaded image file
    
    Returns:
        dict: Blueprint with components and tokens
    """
    if llm_client.is_ai_mode_on():
        blueprint = llm_client.analyze_image_with_llm(image_path)
        if blueprint is not None:
            if _validate_blueprint_schema(blueprint):
                return blueprint
        return image_to_raw_json_stub(image_path)
    else:
        return image_to_raw_json_stub(image_path)


def _validate_blueprint_schema(blueprint: dict) -> bool:
    """
    Validate blueprint has required schema fields.
    
    Args:
        blueprint: Blueprint dict to validate
    
    Returns:
        bool: True if schema is valid, False otherwise
    """
    required_keys = ["screen_id", "screen_type", "orientation", "tokens", "components"]
    for key in required_keys:
        if key not in blueprint:
            return False
    
    if not isinstance(blueprint.get("components"), list):
        return False
    
    if not isinstance(blueprint.get("tokens"), dict):
        return False
    
    required_tokens = ["base_spacing", "primary_color", "accent_color", "font_scale", "border_radius"]
    for token_key in required_tokens:
        if token_key not in blueprint["tokens"]:
            return False
    
    for comp in blueprint["components"]:
        if not all(k in comp for k in ["id", "type", "bbox", "text", "role", "confidence", "visual"]):
            return False
    
    return True

