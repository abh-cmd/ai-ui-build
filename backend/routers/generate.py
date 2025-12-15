from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional

from backend.ai.codegen import generate_react_project
from backend.utils.sample_blueprint import make_json_safe

router = APIRouter(prefix="/generate", tags=["generate"])


class GenerateRequest(BaseModel):
    """Request body for code generation."""
    blueprint: dict


@router.post("/")
async def generate_code(request: Optional[GenerateRequest] = None):
    """
    Generate React + Tailwind code from improved blueprint JSON.
    
    Returns dict of file paths → content.
    Files include: tokens.js, App.jsx, components/Header.jsx, components/ProductCard.jsx
    """
    try:
        if not request or not getattr(request, "blueprint", None):
            return JSONResponse({"detail": "No blueprint provided"}, status_code=400)

        result = generate_react_project(request.blueprint)

        # Ensure files and entry are JSON-serializable
        files = {str(k): str(v) for k, v in result.get("files", {}).items()}
        entry = str(result.get("entry", "src/App.jsx"))

        return JSONResponse({"files": files, "entry": entry})

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
