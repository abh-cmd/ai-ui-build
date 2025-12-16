# AI IMPLEMENTATION MAP - Exactly Where AI Is Used

## QUICK ANSWER: The 4 Core AI Files

```
backend/ai/
├── llm_client.py      ← Google Gemini API calls (THE ACTUAL AI)
├── vision.py          ← Image analysis orchestration
├── edit_agent.py      ← Natural language edits
└── codegen.py         ← React code generation from blueprint
```

---

## 1. THE ACTUAL AI: backend/ai/llm_client.py

**Where Google Gemini API is called:**

```python
# Line 31-47: Check if AI is enabled
def is_ai_mode_on() -> bool:
    ai_mode = os.getenv("AI_MODE", "off").lower()
    return ai_mode == "on"

# Line 49-72: Call Gemini Chat API
def call_gemini_chat(messages, model="gemini-1.5-flash"):
    import google.generativeai as genai
    api_key = os.getenv("GOOGLE_API_KEY")
    genai.configure(api_key=api_key)
    model_obj = genai.GenerativeModel(model)
    # ... sends messages to Gemini ...

# Line 75-186: Vision analysis with Gemini
def analyze_image_with_llm(image_path):
    # 1. Read image file
    # 2. Encode as base64
    # 3. Call gemini-1.5-flash with image
    # 4. LLM analyzes design → returns blueprint JSON
    genai.configure(api_key=api_key)
    # ... Sends to Gemini with prompt ...
    # Returns: {"screen_id": "...", "tokens": {...}, "components": [...]}
```

**Environment Required:**
- `AI_MODE=on` (turns AI on)
- `GOOGLE_API_KEY=AIza...` (Gemini API key)

---

## 2. IMAGE ANALYSIS ORCHESTRATOR: backend/ai/vision.py

**Where the AI flow is controlled:**

```python
def image_to_raw_json(image_path: str) -> dict:
    """
    Entry point for all image uploads
    """
    if llm_client.is_ai_mode_on():
        # AI MODE ON: Use Gemini to analyze image
        blueprint = llm_client.analyze_image_with_llm(image_path)
        if blueprint is not None and _validate_blueprint_schema(blueprint):
            return blueprint  # ← LLM result used
    
    # FALLBACK: Return deterministic stub if AI fails
    return image_to_raw_json_stub(image_path)
```

**The Control Flow:**
```
Upload Image
    ↓
vision.py:image_to_raw_json()
    ├─ AI_MODE=on? YES
    │   ├─ Call llm_client.analyze_image_with_llm()
    │   └─ Validate schema
    ├─ AI_MODE=off? or LLM failed?
    │   └─ Use deterministic stub (no AI)
    ↓
Return Blueprint to /upload endpoint
```

---

## 3. NATURAL LANGUAGE EDIT AGENT: backend/ai/edit_agent.py

**Where edit commands are processed:**

```python
def interpret_and_patch(command: str, blueprint: dict):
    """
    Example: "Make CTA larger"
    """
    if llm_client.is_ai_mode_on():
        # AI MODE ON: Send to Gemini for intelligent editing
        patched, summary = _apply_llm_edit(command, blueprint)
        if patched is not None:
            return patched, summary  # ← LLM result used
    
    # FALLBACK: Use deterministic rules
    return _apply_deterministic_edit(command, blueprint)

def _apply_llm_edit(command, blueprint):
    response = llm_client.call_openai_chat(
        messages=[
            {"role": "system", "content": "You are a UI designer..."},
            {"role": "user", "content": f"Edit blueprint: {command}"}
        ]
    )
    # LLM returns modified blueprint JSON
    return json.loads(response), "Updated via LLM"
```

---

## 4. REACT CODE GENERATION: backend/ai/codegen.py

**Where blueprint colors become React:**

```python
def _generate_hero_section(component: dict, tokens: dict):
    # Extract color from BLUEPRINT (not hardcoded)
    bg_color = component.get("visual", {}).get("bg_color", "#3B82F6")
    
    # Generate React with ACTUAL color from blueprint
    return f'''export default function HeroSection() {{
  return (
    <section style={{{{backgroundColor: "{bg_color}"}}}} >
      ...
    </section>
  );
}}'''

def _generate_feature_cards_grid(components, tokens):
    # For each feature card in blueprint
    for comp in components:
        bg_color = comp.get("visual", {}).get("bg_color")  # From LLM result
        text_color = comp.get("visual", {}).get("text_color")
        
        # Generate React using ACTUAL colors from blueprint
        jsx = f'style={{{{backgroundColor: "{bg_color}", color: "{text_color}"}}}}'
```

---

## COMPLETE DATA FLOW (AI_MODE=ON)

```
┌─────────────────────────────────────┐
│   User Uploads Design Image         │
└──────────────┬──────────────────────┘
               │
               ↓
┌──────────────────────────────────────────┐
│  FastAPI /upload endpoint                │
│  routers/upload.py:upload_image()        │
└──────────────┬───────────────────────────┘
               │
               ↓
┌──────────────────────────────────────────┐
│  vision.py:image_to_raw_json()           │
│  "Should we use AI?"                     │
└──────────────┬───────────────────────────┘
               │
         ┌─────┴──────┐
         │             │
   YES (AI_MODE=on)    NO
         │             │
         ↓             ↓
    ┌────────────┐   ┌──────────────┐
    │  Gemini    │   │ Deterministic│
    │    LLM     │   │     Stub     │
    │(REAL AI)  │   │  (No AI used)│
    └────┬───────┘   └──────┬───────┘
         │                  │
         └─────────┬────────┘
                   ↓
        ┌──────────────────────────┐
        │  Blueprint JSON Result   │
        │ {screen_id, tokens,      │
        │  components with colors}│
        └──────────┬───────────────┘
                   │
                   ↓
        ┌──────────────────────────┐
        │ /generate endpoint        │
        │ routers/generate.py       │
        └──────────┬───────────────┘
                   │
                   ↓
        ┌──────────────────────────┐
        │  codegen.py             │
        │  generate_react_project()│
        │  Uses colors from        │
        │  blueprint.components[]  │
        └──────────┬───────────────┘
                   │
                   ↓
        ┌──────────────────────────┐
        │  React Files Generated   │
        │  - tokens.js             │
        │  - App.jsx               │
        │  - HeroSection.jsx (RED) │
        │  - FeatureCards.jsx      │
        │  - CTAButton.jsx(ORANGE) │
        └──────────┬───────────────┘
                   │
                   ↓
        ┌──────────────────────────┐
        │  Frontend Renders        │
        │  (with actual colors)    │
        └──────────────────────────┘
```

---

## QUICK TEST: Where to Look for AI

### If AI_MODE=on and working:
1. **backend/ai/llm_client.py** - Gemini API is being called
2. **backend/ai/vision.py** - image_to_raw_json() returned LLM result, not stub
3. **Console logs** - Should show Gemini API calls
4. **Generated React** - Colors match your design (not hardcoded)

### If AI_MODE=off:
1. **vision.py** - Falls back to image_to_raw_json_stub()
2. **edit_agent.py** - Falls back to _apply_deterministic_edit()
3. **Generated React** - Uses default blue colors

---

## ENVIRONMENT SETUP

```bash
# Enable AI
export AI_MODE=on
export GOOGLE_API_KEY=AIzaSyChRPAhjFkxaUXzerm884yyeMk5jdoy64s

# Start backend
python -m uvicorn backend.app:app --port 8002

# Now image uploads will use Gemini for analysis!
```

---

## THE THREE MODES

```
MODE 1: AI_MODE=off (DEFAULT)
├─ No AI used
├─ vision.py uses stub only
├─ edit_agent.py uses rules only
└─ Safe, deterministic, no API key needed

MODE 2: AI_MODE=on, No API Key
├─ AI enabled but key missing
├─ Falls back to stub gracefully
├─ No errors, just uses deterministic
└─ System stays stable

MODE 3: AI_MODE=on, API Key Set ✓ (CURRENT)
├─ Gemini API calls active
├─ Image analysis via LLM
├─ Intelligent edits via LLM
├─ Smart design colors extracted
└─ Full AI pipeline operational
```

---

## FILES TOUCHED BY AI

| File | What AI Does |
|------|--------------|
| **llm_client.py** | Makes actual API calls to Gemini |
| **vision.py** | Decides: use AI or fallback? |
| **edit_agent.py** | Sends edits to LLM |
| **codegen.py** | Uses LLM-extracted colors |
| **routers/upload.py** | Calls vision.py |
| **routers/edit.py** | Calls edit_agent.py |

**Files NOT touched by AI:**
- Frontend React code (just renders what codegen produces)
- Database (no AI storage)
- Settings/config files
