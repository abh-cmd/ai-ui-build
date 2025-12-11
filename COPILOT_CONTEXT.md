# GitHub Copilot Project Context

You are assisting with the development of an AI-powered UI Builder for small businesses.

The goal of the project:
Convert a rough sketch + product photos + basic business info into:
1. A clean JSON blueprint of the UI.
2. An improved, professionally aligned layout.
3. Fully working React + Tailwind frontend code.

Copilot’s role:
- Write code ONLY inside the file currently being edited.
- Follow the structure and architecture described below.
- Do NOT invent new architecture or folders.
- Generate clear, modular, readable code.

Project Architecture (fixed — always follow this):

backend/
- app.py                    → FastAPI application setup
- routers/
    upload.py              → POST /upload endpoint
    autocorrect.py         → POST /autocorrect endpoint
    generate.py            → POST /generate endpoint
    edit.py                → POST /edit endpoint
- ai/
    vision.py              → sketch → raw JSON blueprint
    autocorrect.py         → improve spacing, alignment, hierarchy
    codegen.py             → JSON blueprint → React/Tailwind code
    edit_agent.py          → natural-language command → JSON patch
- models/
    schemas.py             → Pydantic models for JSON structures

frontend/
- src/
    pages/
        UploadPage.jsx      → upload UI, display JSON
    components/
        PreviewPanel.jsx    → iframe/code preview
        ProductCard.jsx     → product display component
    tokens.js               → spacing, colors, typography tokens

Rules for Copilot:
- Use FastAPI for backend code.
- Use Pydantic models for JSON validation.
- Use React functional components and Tailwind CSS in frontend.
- Keep code mobile-first, clean, and modular.
- All generated backend endpoints must return JSON.
- All frontend requests must use fetch().

When generating code:
- Follow this project structure strictly.
- Use existing imports before adding new ones.
- Only complete the file being edited; do not generate new files.

End of context.
