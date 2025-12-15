# AI UI Builder

A deterministic MVP for converting design sketches to storefront code.

## Setup

```bash
# Install dependencies
pip install fastapi uvicorn pillow

# Run backend server
uvicorn backend.app:app --reload
```

## API Endpoints

### Phase-1 Core Endpoints
- `POST /upload/` - Upload image, get raw blueprint + autocorrected version
- `POST /autocorrect/` - Apply deterministic spacing/validation rules
- `POST /generate/` - Generate React component files from blueprint
- `POST /edit/` - Apply natural language edits to blueprint (e.g., "make product images bigger")
- `GET /health` - Health check

### Phase-2 Debug Endpoints
- `GET /debug/sample_blueprint` - Return deterministic sample blueprint

## Phase-2: Sample Blueprint & Validation

### Get Sample Blueprint
```bash
curl http://127.0.0.1:8000/debug/sample_blueprint > sample_bp.json
```

### Validate Blueprint Locally
```bash
python tools/check_blueprint.py sample_bp.json
```

The validator checks:
- `base_spacing` is multiple of 8
- All CTA heights >= 44px
- All product aspect_ratios == 1.0

Output:
```
base_spacing: 16
cta_heights: [60]
product_aspect_ratios: [1.0, 1.0]
OK
```

## Project Structure
```
backend/
  app.py              - FastAPI entry point
  routers/
    upload.py         - Image → blueprint
    autocorrect.py    - Blueprint normalization
    generate.py       - Blueprint → React code
    edit.py           - Natural language edits
    debug.py          - Sample blueprint endpoint [Phase-2]
  ai/
    vision.py         - Image processing stub
    autocorrect.py    - Spacing/token normalization
    codegen.py        - React code generation
    edit_agent.py     - Command interpretation
  models/
    schemas.py        - Pydantic models
  utils/
    sample_blueprint.py - Sample data + JSON safety

tools/
  check_blueprint.py  - Blueprint validation CLI [Phase-2]

frontend/
  Vite React app (not deployed)
```

## Design Tokens (Sample)

From `get_sample_blueprint()`:
- Primary: `#E63946` (crimson)
- Accent: `#F1FAEE` (off-white)
- Base spacing: 16px (multiple of 8)
- Font scale: h1=28px, h2=20px, body=14px
- Border radius: 8px

## Testing

**Phase-1 Smoke Tests (All Passing)**
```bash
# Health
curl http://127.0.0.1:8000/health

# Upload + Autocorrect (via router)
curl -F "file=@test-image.png" http://127.0.0.1:8000/upload/

# Generate (POST blueprint)
curl -X POST -H "Content-Type: application/json" \
  -d '{"blueprint":{...}}' \
  http://127.0.0.1:8000/generate/

# Edit (POST command + blueprint)
curl -X POST -H "Content-Type: application/json" \
  -d '{"command":"make product images bigger","blueprint":{...}}' \
  http://127.0.0.1:8000/edit/
```

**Phase-2 Validation**
```bash
# Get sample, validate locally
curl http://127.0.0.1:8000/debug/sample_blueprint > sample_bp.json
python tools/check_blueprint.py sample_bp.json
```

## Next Steps
- [ ] Frontend end-to-end testing
- [ ] Additional edit commands
- [ ] Production deployment (Docker, environment config)
- [ ] Real AI vision model integration (replace vision.py stub)
