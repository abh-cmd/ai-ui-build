import os
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse

from backend.ai.vision import image_to_raw_json
from backend.ai.autocorrect import improve_blueprint
from backend.utils.sample_blueprint import make_json_safe

router = APIRouter(prefix="/upload", tags=["upload"])


@router.post("/")
async def upload_file(file: UploadFile = File(...)):
    """
    Upload sketch/product image and convert to blueprint JSON.
    
    Process:
    1. Save uploaded file to persistent uploads directory (so LLM can analyze it)
    2. Call vision module to extract raw blueprint (with AI_MODE analyzing actual image)
    3. Call autocorrect to improve spacing/tokens
    4. Return improved blueprint JSON
    """
    uploaded_file_path = None
    try:
        # Create uploads directory if it doesn't exist
        uploads_dir = "uploads"
        os.makedirs(uploads_dir, exist_ok=True)
        
        # Save uploaded file with original filename to uploads directory
        # This keeps the file available for LLM vision analysis
        uploaded_file_path = os.path.join(uploads_dir, file.filename)
        contents = await file.read()
        
        with open(uploaded_file_path, "wb") as f:
            f.write(contents)
        
        print(f"DEBUG: Received filename: {file.filename}")
        print(f"DEBUG: Filename lowercase: {file.filename.lower()}")
        print(f"DEBUG: Saved to: {uploaded_file_path}")
        
        # Extract raw blueprint from image using full path so LLM can analyze it
        # vision.py will:
        # - If AI_MODE is on: send actual image to OpenAI for analysis
        # - If AI_MODE is off or LLM fails: use filename branching logic
        raw_blueprint = image_to_raw_json(uploaded_file_path)
        
        print(f"DEBUG: Generated blueprint type: {raw_blueprint.get('screen_type')}")
        print(f"DEBUG: Blueprint components: {[c['type'] for c in raw_blueprint.get('components', [])]}")

        # Improve blueprint (apply spacing rules, token normalization)
        improved_blueprint, changes = improve_blueprint(raw_blueprint)

        # Defensive: ensure JSON-serializable structures (tuples->lists, sets->lists)
        safe_blueprint = make_json_safe(improved_blueprint)

        # Return the exact required shape for Phase-1 tests
        return JSONResponse({
            "filename": file.filename,
            "blueprint": safe_blueprint,
            "changes_applied": changes,
        })
    
    except Exception as e:
        # Phase-1 defensive fix: return HTTP 500 for unexpected errors
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        # Note: NOT deleting the file anymore so LLM can use it for analysis
        # Files accumulate in /uploads directory - clean periodically as needed
        pass
