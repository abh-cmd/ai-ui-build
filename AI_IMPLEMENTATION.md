# AI LLM Integration Implementation

## Overview
This document describes the LLM-powered AI logic integrated into the backend while maintaining strict separation from the frontend (Antigravity). The implementation follows the global rules:

1. **Blueprint is the ONLY thing AI touches**
2. **LLMs MUST NOT generate JSX or frontend code**
3. **All AI logic must be behind AI_MODE flag**
4. **If AI fails, fallback to mock logic**

---

## Architecture

### Control Flow
```
Image Upload
    ↓
[vision.py] 
    ├─ AI_MODE=off → return stub blueprint (deterministic)
    └─ AI_MODE=on → LLM vision → validate schema → fallback to stub on error
    ↓
[autocorrect.py] - improves blueprint spacing/tokens
    ↓
[codegen.py] - generates React files from blueprint
    ↓
Frontend (Antigravity handles routing, canvas, multi-page)
```

---

## Step 1: Vision LLM (`backend/ai/vision.py`)

### Current Behavior (AI_MODE=off)
- Returns deterministic stub blueprint based on filename keywords
- No LLM calls
- Guaranteed availability

### New Behavior (AI_MODE=on)
- Calls `llm_client.analyze_image_with_llm(image_path)`
- LLM analyzes image and returns blueprint JSON
- Validates response against schema
- Fallback to stub on error (quota, network, parse failure)

### Key Functions

#### `image_to_raw_json(image_path: str) -> dict`
Entry point for vision processing:
```python
def image_to_raw_json(image_path: str) -> dict:
    if llm_client.is_ai_mode_on():
        blueprint = llm_client.analyze_image_with_llm(image_path)
        if blueprint is not None and _validate_blueprint_schema(blueprint):
            return blueprint
        return image_to_raw_json_stub(image_path)  # Fallback
    else:
        return image_to_raw_json_stub(image_path)
```

#### `_validate_blueprint_schema(blueprint: dict) -> bool`
Ensures LLM response matches required schema:
- Required keys: `screen_id`, `screen_type`, `orientation`, `tokens`, `components`
- Required tokens: `base_spacing`, `primary_color`, `accent_color`, `font_scale`, `border_radius`
- All components must have: `id`, `type`, `bbox`, `text`, `role`, `confidence`, `visual`

### LLM Prompt (in `llm_client.py`)
The Vision LLM receives:
```
System: You are a UI/UX design analyzer. Extract blueprint data and output ONLY valid JSON.
User: Analyze this design image and extract all visible components, colors, spacing, and layout information.
```

LLM Responsibilities:
- Detect layout sections (header, hero, text, cards, buttons)
- Extract visible text
- Estimate bounding boxes
- Assign component types and roles
- Fill tokens (colors, spacing) conservatively

LLM MUST NOT:
- Generate JSX
- Add routing/page logic
- Change schema

---

## Step 2: Edit LLM (`backend/ai/edit_agent.py`)

### Current Behavior (AI_MODE=off)
- Deterministic rule-based edits:
  - `"make product images bigger"` → increase bbox by 20%
  - `"make CTA larger"` → increase height by 20%
  - `"change primary color to #HEX"` → update primary_color token

### New Behavior (AI_MODE=on)
- Sends user command + current blueprint to LLM
- LLM returns full updated blueprint JSON
- Validates output matches schema and preserves component IDs
- Fallback to deterministic rules on error

### Key Functions

#### `interpret_and_patch(command: str, blueprint: dict) -> Tuple[dict, str]`
Main entry point:
```python
def interpret_and_patch(command: str, blueprint: dict) -> Tuple[dict, str]:
    if llm_client.is_ai_mode_on():
        patched, summary = _apply_llm_edit(command, blueprint)
        if patched is not None:
            return patched, summary
    return _apply_deterministic_edit(command, blueprint)
```

#### `_apply_llm_edit(command: str, blueprint: dict) -> Tuple[Optional[dict], str]`
Calls LLM with blueprint context:
```python
system_prompt = """You are a UI design editor. Modify the provided blueprint JSON based on user commands.
Return ONLY valid JSON (no markdown) matching the exact same schema as input.
Preserve all component IDs and structure. Only modify values as requested.
Do not add or remove components unless explicitly requested."""
```

#### `_validate_edited_blueprint(updated: dict, original: dict) -> bool`
Ensures:
- Updated blueprint has `components` array
- Component IDs match original (no rearrangement or deletion)
- Schema is preserved

### Supported Commands (with LLM enhancement)

Rule-based commands still work in both modes:
- `"make product images bigger"`
- `"make CTA larger"` / `"make button larger"`
- `"change primary color to #RRGGBB"`

With LLM (AI_MODE=on), natural language is more flexible:
- `"Add testimonials section"`
- `"Change header to dark blue"`
- `"Make text sections shorter"`
- Any blueprint modification while preserving schema

---

## Step 3: AI Mode Switch

### Environment Variable: `AI_MODE`
- `AI_MODE=off` (default): Stub + deterministic rules only
- `AI_MODE=on`: LLM vision + LLM edits with fallback

### Implementation
```python
def is_ai_mode_on() -> bool:
    ai_mode = os.getenv("AI_MODE", "off").lower()
    return ai_mode == "on"
```

### When AI_MODE=on Fails
Automatic fallback to mock/stub:
1. **Missing API Key** → Use stub blueprint
2. **API Quota Error (429)** → Use stub blueprint
3. **Network Error** → Use stub blueprint
4. **Invalid JSON Response** → Use stub blueprint
5. **Schema Validation Fails** → Use stub blueprint

**Result**: System remains operational without LLM

---

## Critical Constraints

### ✅ What AI CAN Do
- Analyze images and extract design information
- Suggest blueprint modifications via natural language
- Return JSON matching the fixed schema
- Call OpenAI APIs only

### ❌ What AI MUST NOT Do
- Generate React/JSX code
- Create routing logic
- Rename component IDs (breaks linkage)
- Add fields outside the schema
- Modify frontend behavior
- Change blueprint schema structure

---

## Testing

### Test Suite: `test_ai_integration.py`

Run all tests:
```bash
cd c:\Users\ASUS\Desktop\design-to-code\ai-ui-builder
.venv\Scripts\python.exe test_ai_integration.py
```

Tests verify:
1. ✓ Vision stub mode (AI_MODE=off) returns expected blueprints
2. ✓ Edit deterministic mode (AI_MODE=off) applies rules correctly
3. ✓ Blueprint schema validation accepts/rejects correctly
4. ✓ Edit validation preserves component IDs

**Result**: All tests pass

---

## Integration with Antigravity

### Frontend Independence
- Antigravity receives `{ files: { "src/App.jsx": "...", ... }, entry: "src/App.jsx" }`
- No knowledge of AI_MODE or vision process
- Can store multiple pages independently
- Routing/navigation handled entirely in frontend

### Backend Isolation
- Vision → Blueprint (LLM or stub)
- Edit → Blueprint patch (LLM or rules)
- Codegen → React files from blueprint (unchanged)
- No coupling between vision and frontend

### Multi-Page Support
- Each upload generates independent page
- Blueprint schema is identical across all pages
- Frontend can store: `pages["store"] = { files }`, `pages["about"] = { files }`, etc.
- No backend changes needed for Phase-5 (multi-page)

---

## Production Safety

### No Console Output
- Removed all `print()` statements for production
- Errors logged internally via exceptions

### Synchronous Functions
- All functions are synchronous (no async)
- Compatible with FastAPI sync endpoints

### Error Handling
- Explicit try/except on LLM calls
- Graceful fallback to stubs
- Validation before returning blueprints

### API Key Security
- API key read from environment only
- Never logged or exposed
- Missing key → silent fallback to stub

---

## Checklist

✅ **Different images produce different blueprints in AI_MODE=on**
- LLM analyzes each image independently
- Different designs → different component layouts → different blueprints

✅ **Same commands produce consistent edits**
- LLM receives same blueprint + command → deterministic output
- Deterministic rules are stateless and repeatable

✅ **AI_MODE=off behaves exactly as before**
- Stub vision returns expected blueprints
- Deterministic rules unchanged

✅ **Antigravity integration remains untouched**
- No frontend code modified
- Backend only touches blueprint
- Codegen unchanged
- Frontend routing independent

---

## Deployment

### Enable AI Mode (Production with LLM)
```powershell
$env:AI_MODE = "on"
$env:OPENAI_API_KEY = "sk-proj-..."
.venv\Scripts\python.exe -m uvicorn backend.app:app --port 8002
```

### Disable AI Mode (Demo/Fallback)
```powershell
$env:AI_MODE = "off"
.venv\Scripts\python.exe -m uvicorn backend.app:app --port 8002
```

---

## Future Enhancements

Possible additions without breaking changes:
1. **Custom component types** - Add to schema, update generators
2. **Theme support** - Expand tokens for dark/light modes
3. **Layout variations** - LLM suggests grid layouts, sections
4. **Accessibility hints** - LLM suggests ARIA labels, semantic HTML
5. **Multi-language support** - LLM translates component text

All maintained within:
- Fixed blueprint schema
- No JSX generation
- AI_MODE flag protection
- Fallback safety
