from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

# Import router modules explicitly to avoid circular imports
from backend.routers import upload, autocorrect, generate, edit, debug

app = FastAPI(title="AI UI Builder", version="0.1.0")

# Add no-cache middleware to prevent response caching
class NoCacheMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response

app.add_middleware(NoCacheMiddleware)

# Enable CORS for all origins (for development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(upload.router)
app.include_router(autocorrect.router)
app.include_router(generate.router)
app.include_router(edit.router)
# Debug router for development/testing (Phase-2)
app.include_router(debug.router)

@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "ok", "service": "ai-ui-builder"}
