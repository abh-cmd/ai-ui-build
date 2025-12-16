# HOW TO RUN A TEST AND SEE THE AI IN ACTION

## Option 1: Simple Curl Test (Verify AI is working)

```bash
# Make sure servers are running:
# Terminal 1: Backend
$env:GOOGLE_API_KEY = "AIzaSyChRPAhjFkxaUXzerm884yyeMk5jdoy64s"
$env:AI_MODE = "on"
cd c:\Users\ASUS\Desktop\design-to-code\ai-ui-builder
.venv\Scripts\python.exe -m uvicorn backend.app:app --port 8002

# Terminal 2: Frontend
cd c:\Users\ASUS\Desktop\design-to-code\ai-ui-builder\frontend
npm run dev

# Terminal 3: Test the API
curl -X POST http://localhost:8002/upload -F "file=@c:\path\to\your\image.jpg"
```

Expected response (AI-powered):
```json
{
  "blueprint": {
    "screen_type": "landing",
    "tokens": {
      "primary_color": "#EF4444",
      "accent_color": "#F97316"
    },
    "components": [...]
  }
}
```

---

## Option 2: UI Test (See colors generated correctly)

1. Go to `http://localhost:5173`
2. Upload a design image
3. **VERIFY AI WORKED IF:**
   - Blueprint colors match your design (not default blue)
   - Generated React shows actual colors in style={{}}
   - Example: style={{backgroundColor: "#EF4444"}} (red from your design)

---

## Option 3: Direct Code Test - The 4 Key Functions

### Test 1: Check if AI Mode is On
```python
from backend.ai import llm_client

# This checks: AI_MODE environment variable
is_ai = llm_client.is_ai_mode_on()
print(f"AI_MODE=on? {is_ai}")  # Should print True
```

**File:** [backend/ai/llm_client.py](backend/ai/llm_client.py) - Lines 18-25

---

### Test 2: Call Gemini API Directly
```python
from backend.ai import llm_client

# This calls the actual Google Gemini API
response = llm_client.analyze_image_with_llm("path/to/image.jpg")

print(response)  # Should print blueprint JSON from Gemini
# {
#   "screen_type": "landing",
#   "tokens": {"primary_color": "#EF4444", ...},
#   "components": [...]
# }
```

**File:** [backend/ai/llm_client.py](backend/ai/llm_client.py) - Lines 75-186

---

### Test 3: Vision Agent (with AI fallback)
```python
from backend.ai import vision

# This decides: use AI or fallback?
blueprint = vision.image_to_raw_json("path/to/image.jpg")

# If AI_MODE=on: calls Gemini (Test 2 above)
# If AI_MODE=off: returns stub
# If Gemini fails: automatically falls back to stub

print(blueprint)  # Blueprint from AI or stub
```

**File:** [backend/ai/vision.py](backend/ai/vision.py) - Lines 24-48

---

### Test 4: Code Generation (uses AI blueprint colors)
```python
from backend.ai import codegen
from backend.ai import vision

# Get blueprint (AI-powered if enabled)
blueprint = vision.image_to_raw_json("image.jpg")

# Generate React code using blueprint colors
result = codegen.generate_react_project(blueprint)

# Check files contain actual colors from blueprint
hero_jsx = result["files"]["src/components/HeroSection.jsx"]
print(hero_jsx)
# Should contain: style={{backgroundColor: "#EF4444"}} (from AI)
# NOT: style={{backgroundColor: "bg-blue-500"}} (hardcoded)
```

**File:** [backend/ai/codegen.py](backend/ai/codegen.py) - Lines 1-50

---

## THE 4 KEY FILES EXPLAINED

### 1. **llm_client.py** - Actual AI (Gemini API Calls)

```python
# Line 31-47: Check if AI enabled
def is_ai_mode_on():
    return os.getenv("AI_MODE", "off").lower() == "on"

# Line 75-186: Call Gemini for image analysis
def analyze_image_with_llm(image_path):
    # Reads image
    # Encodes as base64
    # Sends to gemini-1.5-flash
    # Returns blueprint JSON
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content([system_prompt, image, user_prompt])
    blueprint = json.loads(response.text)
    return blueprint  # <-- THE AI RESULT
```

**The Actual AI Happens Here ↑↑↑**

---

### 2. **vision.py** - Orchestrator (Decides: AI or Stub?)

```python
# Line 24-48: Entry point for all image uploads
def image_to_raw_json(image_path):
    if llm_client.is_ai_mode_on():
        # TRY TO USE AI
        blueprint = llm_client.analyze_image_with_llm(image_path)
        if blueprint and _validate_blueprint_schema(blueprint):
            return blueprint  # <-- AI RESULT RETURNED
    
    # FALLBACK IF AI DISABLED OR FAILED
    return image_to_raw_json_stub(image_path)
```

**Controls When AI is Used ↑↑↑**

---

### 3. **edit_agent.py** - Edit Processor (Intelligent Changes)

```python
# Line 15-35: Handle natural language edits
def interpret_and_patch(command, blueprint):
    if llm_client.is_ai_mode_on():
        # SEND TO GEMINI FOR INTELLIGENT EDIT
        patched, summary = _apply_llm_edit(command, blueprint)
        if patched:
            return patched, summary  # <-- LLM MODIFIED BLUEPRINT
    
    # FALLBACK TO RULES
    return _apply_deterministic_edit(command, blueprint)
```

**AI-Powered Edits Happen Here ↑↑↑**

---

### 4. **codegen.py** - Code Generator (Uses AI Blueprint)

```python
# Line 30-50: Generate HeroSection.jsx
def _generate_hero_section(component, tokens):
    bg_color = component.get("visual", {}).get("bg_color")
    # ↑ This color comes from AI blueprint if AI_MODE=on
    
    return f'''
    <section style={{{{backgroundColor: "{bg_color}"}}}} >
      ...
    </section>
    '''
    # ↑ Generated React uses ACTUAL color from AI
```

**AI Colors Appear in React Here ↑↑↑**

---

## ENVIRONMENT VARIABLES (Required for AI)

```bash
# ENABLE AI
AI_MODE=on

# GOOGLE GEMINI API KEY (required if AI_MODE=on)
GOOGLE_API_KEY=AIzaSyChRPAhjFkxaUXzerm884yyeMk5jdoy64s

# These enable the entire Gemini pipeline:
# - llm_client.is_ai_mode_on() returns True
# - llm_client.call_gemini_chat() can connect to Gemini
# - llm_client.analyze_image_with_llm() can analyze images
```

---

## TEST CHECKLIST

- [ ] AI_MODE env var set to "on"
- [ ] GOOGLE_API_KEY env var set
- [ ] Backend running with those env vars
- [ ] Frontend running
- [ ] Upload an image
- [ ] Check blueprint JSON has your actual colors (not defaults)
- [ ] Check generated React code uses those colors
- [ ] Check HeroSection, FeatureCards, CTAButton all match your design

If all pass: **AI is working!** ✓

---

## DEBUGGING: Is AI Actually Being Used?

### Check 1: Environment Variables
```bash
# In PowerShell terminal
echo $env:AI_MODE          # Should print: on
echo $env:GOOGLE_API_KEY   # Should print: AIza...
```

### Check 2: Backend Console Logs
Look for messages like:
```
Gemini API response received
Blueprint extracted: 5 components
Vision confidence: 0.92
```

### Check 3: Generated Code Colors
Open generated React and search for:
```javascript
// If AI worked, you'll see YOUR actual colors:
style={{backgroundColor: "#EF4444"}}  // Your red
style={{backgroundColor: "#F97316"}}  // Your orange

// If AI didn't work, you'll see defaults:
style={{backgroundColor: "#3B82F6"}}  // Default blue
```

### Check 4: Blueprint JSON Colors
Upload returns:
```json
// AI_MODE=on (working):
"primary_color": "#EF4444"  // Your design's color

// AI_MODE=off (stub):
"primary_color": "#3B82F6"  // Default blue
```

---

## SUMMARY: 4 Functions = Whole AI Pipeline

| Function | File | What It Does | Is This AI? |
|----------|------|--------------|-----------|
| `is_ai_mode_on()` | llm_client.py | Checks env var | No (control) |
| `analyze_image_with_llm()` | llm_client.py | **Calls Gemini API** | **YES ← REAL AI** |
| `image_to_raw_json()` | vision.py | Routes to AI or stub | Conditional |
| `_apply_llm_edit()` | edit_agent.py | **Sends to Gemini for edits** | **YES ← REAL AI** |
| `generate_react_project()` | codegen.py | Uses blueprint colors | No (code gen) |

**The 2 functions with REAL AI are:**
1. `analyze_image_with_llm()` - Image analysis via Gemini
2. `_apply_llm_edit()` - Edit commands via Gemini
