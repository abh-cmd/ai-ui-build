from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional

from backend.ai.autocorrect import improve_blueprint
from backend.utils.sample_blueprint import make_json_safe

router = APIRouter(prefix="/autocorrect", tags=["autocorrect"])


class AutocorrectRequest(BaseModel):
    """Request body for autocorrect endpoint."""
    blueprint: dict


@router.post("/")
async def autocorrect_blueprint(request: Optional[AutocorrectRequest] = None):
    """
    Improve existing blueprint by applying spacing/alignment rules.
    
    Rules applied:
    - Snap spacing to base 8
    - Ensure CTA minimum height 44
    - Normalize product card aspect ratios
    """
    try:
        if not request or not getattr(request, "blueprint", None):
            return JSONResponse({"detail": "No blueprint provided"}, status_code=400)

        improved_blueprint, changes = improve_blueprint(request.blueprint)

        safe_blueprint = make_json_safe(improved_blueprint)

        return JSONResponse({
            "blueprint": safe_blueprint,
            "changes_applied": changes,
        })

    except ValueError as ve:
        # Validation errors from autocorrect
        return JSONResponse({"detail": str(ve)}, status_code=400)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
