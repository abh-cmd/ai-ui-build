"""Vision stub: deterministic blueprint for testing and fallback.

This module provides the deterministic stub that is used when AI_MODE is off
or when LLM processing fails. Implements blueprint branching based on filename.
"""

import os


def image_to_raw_json_stub(image_path: str) -> dict:
    """
    Return a deterministic sample blueprint based on filename.
    
    Branching logic:
    - "store" or "product" in filename -> storefront blueprint
    - "about" or "company" in filename -> content blueprint
    - else -> landing page blueprint
    
    This stub is used when:
    - AI_MODE is off (default)
    - LLM vision processing fails
    - API key is missing or invalid
    
    Args:
        image_path: Path to image file (used for filename branching)
    
    Returns:
        dict: Deterministic blueprint matching schema
    """
    
    # Extract filename for branching logic
    filename = os.path.basename(image_path).lower()
    
    # Branching logic based on filename
    if "store" in filename or "product" in filename:
        return _create_storefront_blueprint()
    elif "about" in filename or "company" in filename:
        return _create_content_blueprint()
    else:
        return _create_landing_blueprint()


def _create_storefront_blueprint() -> dict:
    """Create a storefront blueprint with header, products, and CTA."""
    return {
        "screen_id": "storefront",
        "screen_type": "storefront",
        "orientation": "portrait",
        "tokens": {
            "base_spacing": 16,
            "primary_color": "#3B82F6",
            "accent_color": "#F59E0B",
            "font_scale": {
                "heading": 1.5,
                "body": 1.0
            },
            "border_radius": "8px"
        },
        "components": [
            {
                "id": "header_1",
                "type": "header",
                "bbox": [0, 0, 375, 80],
                "text": "My Store",
                "role": "hero",
                "confidence": 0.95,
                "visual": {
                    "bg_color": "#3B82F6",
                    "text_color": "#FFFFFF"
                }
            },
            {
                "id": "product_card_1",
                "type": "product_card",
                "bbox": [12, 100, 363, 280],
                "text": "Product 1",
                "role": "content",
                "confidence": 0.92,
                "visual": {
                    "image_url": "/placeholder.jpg",
                    "aspect_ratio": 1.0,
                    "price": "$29.99"
                }
            },
            {
                "id": "product_card_2",
                "type": "product_card",
                "bbox": [12, 300, 363, 480],
                "text": "Product 2",
                "role": "content",
                "confidence": 0.90,
                "visual": {
                    "image_url": "/placeholder.jpg",
                    "aspect_ratio": 1.0,
                    "price": "$39.99"
                }
            },
            {
                "id": "cta_button",
                "type": "button",
                "bbox": [12, 500, 363, 560],
                "text": "Shop Now",
                "role": "cta",
                "confidence": 0.94,
                "visual": {
                    "bg_color": "#F59E0B",
                    "text_color": "#000000",
                    "height": 44
                }
            }
        ],
        "meta": {
            "source": "sketch_upload",
            "vision_confidence": 0.92
        }
    }


def _create_content_blueprint() -> dict:
    """Create a content blueprint with header, text section, bullet list, and CTA."""
    return {
        "screen_id": "about",
        "screen_type": "content",
        "orientation": "portrait",
        "tokens": {
            "base_spacing": 16,
            "primary_color": "#10B981",
            "accent_color": "#8B5CF6",
            "font_scale": {
                "heading": 1.5,
                "body": 1.0
            },
            "border_radius": "8px"
        },
        "components": [
            {
                "id": "header_2",
                "type": "header",
                "bbox": [0, 0, 375, 80],
                "text": "About Us",
                "role": "hero",
                "confidence": 0.95,
                "visual": {
                    "bg_color": "#10B981",
                    "text_color": "#FFFFFF"
                }
            },
            {
                "id": "text_section_1",
                "type": "text",
                "bbox": [12, 100, 363, 200],
                "text": "Learn more about our company and mission",
                "role": "content",
                "confidence": 0.91,
                "visual": {
                    "text_color": "#1F2937",
                    "font_size": 16
                }
            },
            {
                "id": "bullet_list_1",
                "type": "list",
                "bbox": [12, 220, 363, 380],
                "text": "Feature 1\nFeature 2\nFeature 3",
                "role": "content",
                "confidence": 0.89,
                "visual": {
                    "text_color": "#374151",
                    "font_size": 14
                }
            },
            {
                "id": "cta_button_2",
                "type": "button",
                "bbox": [12, 410, 363, 470],
                "text": "Learn More",
                "role": "cta",
                "confidence": 0.93,
                "visual": {
                    "bg_color": "#8B5CF6",
                    "text_color": "#FFFFFF",
                    "height": 44
                }
            }
        ],
        "meta": {
            "source": "sketch_upload",
            "vision_confidence": 0.91
        }
    }


def _create_landing_blueprint() -> dict:
    """Create a landing page blueprint with hero, feature cards, and CTA."""
    return {
        "screen_id": "landing",
        "screen_type": "landing",
        "orientation": "portrait",
        "tokens": {
            "base_spacing": 16,
            "primary_color": "#EF4444",
            "accent_color": "#F97316",
            "font_scale": {
                "heading": 1.5,
                "body": 1.0
            },
            "border_radius": "8px"
        },
        "components": [
            {
                "id": "hero_section_1",
                "type": "hero",
                "bbox": [0, 0, 375, 180],
                "text": "THIS IS A FALLBACK STUB - GEMINI FAILED",
                "role": "hero",
                "confidence": 0.96,
                "visual": {
                    "bg_color": "#EF4444",
                    "text_color": "#FFFFFF"
                }
            },
            {
                "id": "feature_card_1",
                "type": "card",
                "bbox": [12, 200, 363, 300],
                "text": "Feature One",
                "role": "content",
                "confidence": 0.90,
                "visual": {
                    "bg_color": "#FEE2E2",
                    "text_color": "#7F1D1D"
                }
            },
            {
                "id": "feature_card_2",
                "type": "card",
                "bbox": [12, 320, 363, 420],
                "text": "Feature Two",
                "role": "content",
                "confidence": 0.90,
                "visual": {
                    "bg_color": "#FFEDD5",
                    "text_color": "#7C2D12"
                }
            },
            {
                "id": "feature_card_3",
                "type": "card",
                "bbox": [12, 440, 363, 540],
                "text": "Feature Three",
                "role": "content",
                "confidence": 0.90,
                "visual": {
                    "bg_color": "#FFF7ED",
                    "text_color": "#7C2D12"
                }
            },
            {
                "id": "cta_button_3",
                "type": "button",
                "bbox": [12, 570, 363, 630],
                "text": "Get Started",
                "role": "cta",
                "confidence": 0.94,
                "visual": {
                    "bg_color": "#F97316",
                    "text_color": "#FFFFFF",
                    "height": 44
                }
            }
        ],
        "meta": {
            "source": "sketch_upload",
            "vision_confidence": 0.92
        }
    }
