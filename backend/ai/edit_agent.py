import copy
import json
import re
from typing import Tuple, Optional
from backend.ai import llm_client
from backend.utils.blueprint_validator import validate_blueprint, BlueprintValidationError


def interpret_and_patch(command: str, blueprint: dict) -> Tuple[dict, str]:
    """
    Apply natural language edits to blueprint.
    
    Strict behavior:
    - Validates blueprint first (HTTP 400 if invalid)
    - Only applies deterministic, schema-preserving edits
    - If AI_MODE=on, uses LLM to interpret command intent
    - Falls back to deterministic rules
    - Re-validates after patching
    
    Args:
        command: Natural language instruction
        blueprint: Current blueprint dict
    
    Returns:
        tuple: (patched_blueprint, patch_summary: str)
        
    Raises:
        BlueprintValidationError: If blueprint is invalid
    """
    # Validate input blueprint first
    validate_blueprint(blueprint)
    
    # Try LLM interpretation if available
    if llm_client.is_ai_mode_on():
        patched, summary = _apply_llm_edit(command, blueprint)
        if patched is not None:
            try:
                validate_blueprint(patched)
                return patched, summary
            except BlueprintValidationError:
                # LLM violated schema, fallback to deterministic
                pass
    
    # Apply deterministic edits
    patched, summary = _apply_deterministic_edit(command, blueprint)
    
    # Re-validate to ensure schema integrity
    validate_blueprint(patched)
    
    return patched, summary


def _apply_llm_edit(command: str, blueprint: dict) -> Tuple[Optional[dict], str]:
    """
    Apply LLM-powered blueprint edits.
    
    LLM is ONLY used for:
    - Understanding command intent
    - Determining numeric changes
    - Mapping command to blueprint fields
    
    LLM is NEVER used for:
    - Generating JSX
    - Adding/removing components
    - Changing schema structure
    
    Args:
        command: User edit command
        blueprint: Current blueprint (already validated)
    
    Returns:
        tuple: (patched_blueprint or None, summary)
    """
    system_prompt = """You are a design blueprint editor. Your ONLY job is to modify JSON values.

RULES:
1. Return ONLY valid JSON (no markdown, no commentary)
2. Preserve ALL component IDs exactly
3. Preserve ALL top-level keys
4. Modify ONLY numeric and color values
5. Never add/remove components
6. Never change schema structure

Command types allowed:
- Change colors (hex format only)
- Change numeric values (sizes, spacing, heights)
- Scale bbox dimensions proportionally

If the command cannot be expressed as numeric/color changes, return null."""

    user_prompt = f"""Blueprint:
{json.dumps(blueprint, indent=2)}

Command: {command}

Return ONLY the complete modified blueprint as JSON (or null if unsupported)."""

    try:
        response = llm_client.call_gemini_chat(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            model="gemini-2.0-flash-exp"
        )
        
        if response is None or response.strip() == "null":
            return None, "LLM could not interpret command"
        
        # Parse response
        updated = json.loads(response)
        if not isinstance(updated, dict):
            return None, "LLM response was not a blueprint"
        
        # Validate schema preservation
        if not _validate_schema_preserved(updated, blueprint):
            return None, "LLM violated schema constraints"
        
        return updated, "Updated via LLM interpretation"
        
    except json.JSONDecodeError:
        return None, "LLM response was not valid JSON"
    except Exception as e:
        return None, f"LLM error: {str(e)}"


def _validate_schema_preserved(updated: dict, original: dict) -> bool:
    """
    Validate that LLM-edited blueprint preserves critical schema.
    
    Args:
        updated: Edited blueprint
        original: Original blueprint
    
    Returns:
        bool: True if schema preserved
    """
    # Must have components
    if "components" not in updated or not isinstance(updated["components"], list):
        return False
    
    # Component IDs must be identical
    if "components" not in original:
        return False
    
    original_ids = {c.get("id") for c in original["components"]}
    updated_ids = {c.get("id") for c in updated["components"]}
    
    if original_ids != updated_ids:
        return False
    
    # Must have tokens
    if "tokens" not in updated or not isinstance(updated["tokens"], dict):
        return False
    
    return True



def _apply_deterministic_edit(command: str, blueprint: dict) -> Tuple[dict, str]:
    """
    Apply rule-based deterministic edits.
    
    Supported deterministic commands:
    1. Font size: "increase font size" → 20% increase
    2. Height: "make button taller" → 20% increase
    3. Spacing: "add more spacing" → 20% increase
    4. Colors: "change primary color to #HEX" → update token
    5. Bbox scaling: "make X bigger" → scale bbox by 20%
    
    If command is unsupported → return no changes.
    
    Args:
        command: User command
        blueprint: Current blueprint (already validated)
    
    Returns:
        tuple: (patched_blueprint, summary)
    """
    patched = copy.deepcopy(blueprint)
    summary = ""
    
    cmd_lower = command.lower()
    
    # Pattern 1: Color changes (STRICT hex validation)
    color_match = re.search(r"change.*?(?:primary|accent)\s+color\s+to\s+(#[0-9A-Fa-f]{6})", cmd_lower)
    if color_match:
        new_color = color_match.group(1)
        # Extract which color (primary or accent)
        if "accent" in cmd_lower:
            if "tokens" in patched:
                patched["tokens"]["accent_color"] = new_color
            summary = f"Changed accent color to {new_color}"
        else:
            if "tokens" in patched:
                patched["tokens"]["primary_color"] = new_color
            summary = f"Changed primary color to {new_color}"
        return patched, summary
    
    # Pattern 2: Button/CTA height increase
    if "make" in cmd_lower and ("cta" in cmd_lower or "button" in cmd_lower) and ("bigger" in cmd_lower or "larger" in cmd_lower or "taller" in cmd_lower):
        if "components" in patched:
            for comp in patched["components"]:
                if comp.get("role") == "cta" or comp.get("type") in ["button", "cta"]:
                    # Modify bbox height (index 3)
                    bbox = comp.get("bbox", [0, 0, 100, 44])
                    old_height = bbox[3]
                    bbox[3] = int(old_height * 1.2)
                    comp["bbox"] = bbox
                    summary = f"Increased button height from {int(old_height)}px to {int(bbox[3])}px"
        if not summary:
            summary = "No CTA button found to enlarge"
        return patched, summary
    
    # Pattern 3: Product cards scaling
    if "make" in cmd_lower and "product" in cmd_lower and ("bigger" in cmd_lower or "larger" in cmd_lower):
        scaled = False
        if "components" in patched:
            for comp in patched["components"]:
                if comp.get("type") == "product_card":
                    bbox = comp.get("bbox", [0, 0, 300, 300])
                    new_bbox = [
                        bbox[0],
                        bbox[1],
                        int(bbox[2] * 1.2),
                        int(bbox[3] * 1.2),
                    ]
                    comp["bbox"] = new_bbox
                    scaled = True
        if scaled:
            summary = "Increased product card size by 20%"
        else:
            summary = "No product cards found to enlarge"
        return patched, summary
    
    # Pattern 4: Spacing increase
    if ("spacing" in cmd_lower or "gap" in cmd_lower or "margin" in cmd_lower) and ("more" in cmd_lower or "increase" in cmd_lower or "bigger" in cmd_lower):
        if "tokens" in patched and "base_spacing" in patched["tokens"]:
            old_spacing = patched["tokens"]["base_spacing"]
            patched["tokens"]["base_spacing"] = int(old_spacing * 1.2)
            summary = f"Increased base spacing from {old_spacing}px to {int(patched['tokens']['base_spacing'])}px"
        else:
            summary = "No base spacing found to modify"
        return patched, summary
    
    # Pattern 5: Font size increase
    if "font" in cmd_lower and "size" in cmd_lower and ("increase" in cmd_lower or "bigger" in cmd_lower or "larger" in cmd_lower):
        modified = False
        if "components" in patched:
            for comp in patched["components"]:
                if "visual" in comp and comp["visual"] is not None:
                    if "font_size" in comp["visual"]:
                        old_size = comp["visual"]["font_size"]
                        comp["visual"]["font_size"] = int(old_size * 1.2)
                        modified = True
        if modified:
            summary = "Increased font sizes by 20% across components"
        else:
            summary = "No components with font_size found"
        return patched, summary
    
    # Unsupported command
    summary = f"Command not supported: '{command}'. Supported: color changes, button sizing, product scaling, spacing, font sizes"
    return patched, summary
