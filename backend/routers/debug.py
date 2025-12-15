"""Debug router for development and testing (Phase-2).

Provides sample blueprints and inspection endpoints.
"""
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from backend.utils.sample_blueprint import get_sample_blueprint

router = APIRouter(prefix="/debug", tags=["debug"])


@router.get("/sample_blueprint")
def sample_blueprint():
    """Return a deterministic sample blueprint for testing /generate, /edit, etc."""
    return JSONResponse({"blueprint": get_sample_blueprint()})
