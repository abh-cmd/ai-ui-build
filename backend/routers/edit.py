from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import json

from backend.ai.edit_agent import interpret_and_patch
from backend.utils.blueprint_validator import validate_blueprint, BlueprintValidationError
from backend.utils.command_validator import CommandValidator, CommandValidationError
from backend.utils.sample_blueprint import make_json_safe

router = APIRouter(prefix="/enhance", tags=["enhance"])


class EnhanceRequest(BaseModel):
    """Request body for enhance endpoint."""
    command: str
    blueprint: dict


@router.post("/")
async def enhance_blueprint(request: EnhanceRequest):
    """
    Apply natural language edits to blueprint.
    
    Enforces PHASE 6.1 command contract:
    - Valid commands only (frozen UX contract)
    - Blueprint schema strictly preserved
    - Deterministic edits only
    
    Input:
    {
        "command": "make button bigger",
        "blueprint": {...}
    }
    
    Returns:
    {
        "patched_blueprint": {...},
        "summary": "Increased button height by 20%"
    }
    
    Error responses:
    - 400: Invalid command or blueprint
    - 422: Unsupported command (valid syntax, not implemented)
    - 500: Server error
    """
    
    try:
        # 1. VALIDATE COMMAND (from PHASE 6.1 contract)
        try:
            CommandValidator.validate(request.command)
        except CommandValidationError as e:
            return JSONResponse(
                {
                    "error": str(e),
                    "code": "INVALID_COMMAND"
                },
                status_code=400
            )
        
        # 2. VALIDATE BLUEPRINT STRUCTURE
        try:
            validate_blueprint(request.blueprint)
        except BlueprintValidationError as e:
            return JSONResponse(
                {
                    "error": f"Invalid blueprint: {str(e)}",
                    "code": "INVALID_BLUEPRINT"
                },
                status_code=400
            )
        
        # 3. APPLY PATCH (deterministic + LLM fallback)
        try:
            patched_blueprint, summary = interpret_and_patch(
                request.command,
                request.blueprint
            )
        except BlueprintValidationError as e:
            return JSONResponse(
                {
                    "error": f"Patch validation failed: {str(e)}",
                    "code": "INVALID_OUTPUT"
                },
                status_code=500
            )
        except ValueError as e:
            return JSONResponse(
                {
                    "error": str(e),
                    "code": "PATCH_ERROR"
                },
                status_code=422
            )
        
        # 4. ENSURE OUTPUT IS CLEAN JSON
        safe_blueprint = make_json_safe(patched_blueprint)
        
        return JSONResponse({
            "patched_blueprint": safe_blueprint,
            "summary": summary
        }, status_code=200)
    
    except Exception as e:
        print(f"[ERROR] /enhance endpoint: {str(e)}")
        return JSONResponse(
            {
                "error": "Internal server error",
                "code": "INTERNAL_ERROR"
            },
            status_code=500
        )


# Keep /edit as alias for backwards compatibility
@router.post("/edit")
async def edit_blueprint(request: EnhanceRequest):
    """Alias for /enhance endpoint (backwards compatible)."""
    return await enhance_blueprint(request)
