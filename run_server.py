#!/usr/bin/env python
import os
import sys

# Default: Use stub (demo mode)
# To use real Gemini: 
#   1. Set GOOGLE_API_KEY environment variable
#   2. Uncomment the line below
# os.environ["AI_MODE"] = "on"

ai_mode = os.getenv("AI_MODE", "off").lower()

# If AI_MODE is on but no API key, warn user
if ai_mode == "on":
    if not os.getenv("GOOGLE_API_KEY"):
        print("WARNING: AI_MODE=on but GOOGLE_API_KEY not set. Falling back to stub mode.", file=sys.stderr)
        ai_mode = "off"

os.environ["AI_MODE"] = ai_mode

from backend.app import app
import uvicorn

if __name__ == "__main__":
    if ai_mode == "on":
        print("Starting server with AI_MODE=on (using Gemini API)...", file=sys.stderr)
    else:
        print("Starting server with AI_MODE=off (using deterministic stub)...", file=sys.stderr)
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
