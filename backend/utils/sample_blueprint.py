"""Utilities: sample blueprint and JSON-safety helpers (Phase-1 defensive fixes).

This file provides a deterministic sample blueprint generator and a
recursive `make_json_safe` helper that converts tuples/sets to lists and
ensures values are basic Python types suitable for JSON serialization.
"""
from typing import Any


def get_sample_blueprint() -> dict:
    """Return a deterministic sample blueprint for testing /generate, /edit, etc.
    
    Tokens and components comply with autocorrect rules:
    - base_spacing is multiple of 8
    - CTA height >= 44
    - product aspect_ratio == 1.0
    
    Phase-2: Updated schema with enhanced design tokens.
    """
    return {
        "screen_id": "home",
        "screen_type": "storefront",
        "orientation": "portrait",
        "tokens": {
            "base_spacing": 16,
            "primary_color": "#E63946",
            "accent_color": "#F1FAEE",
            "font_scale": {"h1": "28px", "h2": "20px", "body": "14px"},
            "border_radius": "8px",
        },
        "components": [
            {
                "id": "header_1",
                "type": "header",
                "bbox": [0, 0, 375, 100],
                "text": "Welcome",
                "role": "title",
                "confidence": 0.98,
                "visual": {"bg_color": "#E63946", "text_color": "#F1FAEE"},
            },
            {
                "id": "product_card_1",
                "type": "product_card",
                "bbox": [12, 120, 363, 320],
                "text": "Premium Product A",
                "role": "content",
                "confidence": 0.94,
                "visual": {"image_url": "/product_a.jpg", "aspect_ratio": 1.0, "price": "$49.99"},
            },
            {
                "id": "product_card_2",
                "type": "product_card",
                "bbox": [12, 340, 363, 540],
                "text": "Premium Product B",
                "role": "content",
                "confidence": 0.93,
                "visual": {"image_url": "/product_b.jpg", "aspect_ratio": 1.0, "price": "$59.99"},
            },
            {
                "id": "cta_button",
                "type": "button",
                "bbox": [12, 560, 363, 620],
                "text": "Shop Now",
                "role": "cta",
                "confidence": 0.96,
                "visual": {"bg_color": "#E63946", "text_color": "#F1FAEE", "height": 60},
            },
        ],
        "meta": {"source": "sample-blueprint", "generated_by": "sample-blueprint"},
    }


def make_json_safe(obj: Any) -> Any:
    """Recursively convert tuples/sets to lists and ensure JSON-serializable types.

    - tuples -> lists
    - sets -> lists
    - converts non-serializable keys to strings
    """
    if obj is None:
        return None
    if isinstance(obj, (str, int, float, bool)):
        # Basic types are safe (avoid NaN/Inf usage elsewhere)
        return obj
    if isinstance(obj, (list, tuple)):
        return [make_json_safe(x) for x in list(obj)]
    if isinstance(obj, set):
        return [make_json_safe(x) for x in sorted(list(obj))]
    if isinstance(obj, dict):
        new = {}
        for k, v in obj.items():
            new[str(k)] = make_json_safe(v)
        return new
    # Fallback: coerce to string
    return str(obj)
