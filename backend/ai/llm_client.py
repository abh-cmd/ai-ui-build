"""LLM client wrapper for optional AI vision processing.

This module handles Google Gemini API calls for image analysis when AI_MODE is enabled.
It provides safe fallback mechanisms to ensure the service remains stable
if the LLM is unavailable or misconfigured.

Environment Variables:
    AI_MODE: "on" or "off" (default "off")
    GOOGLE_API_KEY: Google Gemini API key (required if AI_MODE="on")
"""

import os
import json
import base64
import re
from typing import List, Dict, Any, Optional


def is_ai_mode_on() -> bool:
    """
    Check if AI mode is enabled via environment variable.
    
    Returns:
        bool: True if AI_MODE env var is set to "on", False otherwise
    """
    ai_mode = os.getenv("AI_MODE", "off").lower()
    return ai_mode == "on"


def call_gemini_chat(
    messages: List[Dict[str, str]],
    model: str = "gemini-1.5-flash"
) -> Optional[str]:
    """
    Call Google Gemini Chat API.
    
    Args:
        messages: List of message dicts with "role" and "content" keys
        model: Model name (default "gemini-1.5-flash")
    
    Returns:
        str: Response text, or None if API call fails
    """
    try:
        import google.generativeai as genai
    except ImportError:
        raise ImportError(
            "google-generativeai package required for AI_MODE. Install with: pip install google-generativeai"
        )
    
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("GOOGLE_API_KEY not set. Cannot use Gemini API.")
        return None
    
    genai.configure(api_key=api_key)
    
    try:
        # Use correct model format for current API
        model_name = "gemini-1.5-flash" if not model.startswith("models/") else model
        model_obj = genai.GenerativeModel(model_name)
        # Convert messages to Gemini format
        chat = model_obj.start_chat()
        
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            chat.send_message(content)
        
        return chat.last.text
    except Exception as e:
        print(f"Gemini API error: {e}")
        return None


def analyze_image_with_llm(image_path: str) -> Optional[Dict[str, Any]]:
    """
    Analyze an image using Google Gemini vision to extract blueprint data.
    
    Uses gemini-2.0-flash-exp with vision capabilities to:
    1. Read image file
    2. Send to LLM with blueprint schema instructions
    3. Parse JSON response
    4. Return blueprint dict or None on failure
    
    Args:
        image_path: Path to image file
    
    Returns:
        dict: Blueprint dict, or None if analysis fails
    """
    if not os.path.exists(image_path):
        print(f"Image file not found: {image_path}")
        return None
    
    try:
        import google.generativeai as genai
    except ImportError:
        print("google-generativeai package not installed. Cannot use LLM vision.")
        return None
    
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("GOOGLE_API_KEY not set. Cannot use Gemini vision.")
        return None
    
    genai.configure(api_key=api_key)
    
    # Determine image type
    image_ext = os.path.splitext(image_path)[1].lower()
    if image_ext in [".jpg", ".jpeg"]:
        mime_type = "image/jpeg"
    elif image_ext == ".png":
        mime_type = "image/png"
    else:
        mime_type = "image/jpeg"  # default
    
    system_prompt = """You are a UI/UX design analyzer. Analyze the provided image and extract blueprint data.
Output ONLY valid JSON (no markdown, no code blocks) matching this schema:
{
  "screen_id": "home",
  "screen_type": "storefront",
  "orientation": "portrait",
  "tokens": {
    "base_spacing": 16,
    "primary_color": "#RRGGBB",
    "accent_color": "#RRGGBB",
    "font_scale": {"heading": 1.5, "body": 1.0},
    "border_radius": "8px"
  },
  "components": [
    {
      "id": "unique_id",
      "type": "header|product_card|button|...",
      "bbox": [x, y, width, height],
      "text": "component text",
      "role": "hero|content|cta|...",
      "confidence": 0.9,
      "visual": {...}
    }
  ],
  "meta": {"source": "llm_analysis"}
}"""

    user_prompt = """Analyze this design image and extract all visible components, colors, spacing, and layout information.
Generate a complete blueprint JSON response."""

    try:
        # Use gemini-2.0-flash-exp which is stable and available
        model = genai.GenerativeModel("gemini-2.0-flash-exp")
        
        with open(image_path, "rb") as f:
            image_bytes = f.read()
        
        response = model.generate_content(
            [
                system_prompt,
                {
                    "mime_type": mime_type,
                    "data": base64.standard_b64encode(image_bytes).decode("utf-8")
                },
                user_prompt
            ]
        )
        
        response_text = response.text
        
        # Try to parse JSON
        try:
            blueprint = json.loads(response_text)
            return blueprint
        except json.JSONDecodeError:
            # Try regex extraction
            json_match = re.search(r"\{.*\}", response_text, re.DOTALL)
            if json_match:
                try:
                    blueprint = json.loads(json_match.group(0))
                    return blueprint
                except json.JSONDecodeError:
                    print("Failed to extract valid JSON from Gemini response")
                    return None
            else:
                print("No JSON found in Gemini response")
                return None
                
    except Exception as e:
        print(f"Gemini vision analysis failed: {e}")
        return None
