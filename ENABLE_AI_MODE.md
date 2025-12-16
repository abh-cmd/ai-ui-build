# ENABLE FULL AI MODE (VISION + LLM + EVERYTHING)

## What You're Currently Testing
```
AI_MODE=off → Uses deterministic stub
Only tests: Edit commands (PHASE 6.3)
Skips: Vision processing, LLM analysis, real image handling
```

## What You SHOULD Test
```
AI_MODE=on → Uses real Gemini vision API
Tests: 
  ✓ Upload real image → Vision analyzes it
  ✓ LLM extracts blueprint structure
  ✓ Component detection works
  ✓ Confidence scores generated
  ✓ Edit commands applied to REAL blueprint
  ✓ Everything end-to-end
```

---

## Step 1: Get Google API Key (2 minutes)

1. Go to: **https://aistudio.google.com/apikey**
2. Click: **"Create API Key"**
3. Choose: **"Create API key in new project"** (or existing)
4. Copy the key (looks like: `AIzaSy...`)
5. Keep it safe - this is your secret!

**Note:** Google gives free tier (60 requests/minute), perfect for testing

---

## Step 2: Install Google Package

```powershell
pip install google-generativeai
```

---

## Step 3: Set Environment Variables & Enable AI_MODE

### Option A: Command Line (Current Session Only)

```powershell
$env:GOOGLE_API_KEY = "your-api-key-from-step-1"
$env:AI_MODE = "on"
python run_server.py
```

### Option B: Permanent (.env File)

1. Create file: `C:\Users\ASUS\Desktop\design-to-code\ai-ui-builder\.env`

2. Add these lines:
```
GOOGLE_API_KEY=your-api-key-from-step-1
AI_MODE=on
```

3. Load it before running:
```powershell
Get-Content .env | ForEach-Object {
  if ($_ -match '^([^=]+)=(.+)$') {
    [Environment]::SetEnvironmentVariable($matches[1], $matches[2])
  }
}
python run_server.py
```

---

## Step 4: Start Backend With AI Enabled

```powershell
# Kill old process first
Stop-Process -Name python -Force -ErrorAction SilentlyContinue

# Start with AI enabled
$env:GOOGLE_API_KEY = "your-key-here"
$env:AI_MODE = "on"
python run_server.py
```

**Expected Output:**
```
Starting server with AI_MODE=on (using Gemini API)...
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000
```

---

## Step 5: Test Full Pipeline

### Test 1: Vision Processing (NEW)
```
1. Open: http://localhost:5174
2. Upload: Any REAL image (design, screenshot, etc.)
3. Watch: Browser console for Gemini API call
4. See: Blueprint extracted from YOUR image (not stub!)
```

**What's happening:**
```
Upload Image
  ↓
Backend receives file
  ↓
Calls Gemini vision API
  ↓
"Analyze this image and extract components"
  ↓
Gemini returns: [header, button, form, footer, etc.]
  ↓
Backend creates blueprint with YOUR components
  ↓
Frontend displays REAL blueprint
```

### Test 2: Edit Commands on REAL Blueprint
```
1. After image uploads
2. Type: "Make button bigger"
3. Click: "Apply Edit"
4. See: Edit applies to REAL component (not stub)
```

### Test 3: Multiple Edits Stacking
```
1. Type: "Make button bigger" → Apply
2. Type: "Change primary color to #FF5733" → Apply
3. Type: "Increase heading size" → Apply
4. Verify: All 3 edits visible in final blueprint
```

---

## Full Test Checklist (With AI Enabled)

```
VISION & LLM TESTS
=================

[ ] 1. Backend starts with AI_MODE=on
      Console shows: "Starting server with AI_MODE=on"

[ ] 2. Google API key set correctly
      Backend doesn't show warning about missing key

[ ] 3. google-generativeai package installed
      No import errors in backend

[ ] 4. Upload real image (not stub)
      See Gemini analyzing image
      Blueprint components from YOUR image

[ ] 5. Blueprint valid
      All component types valid (hero, card, etc.)
      Not the hardcoded stub

[ ] 6. Edit command on REAL blueprint
      "Make button bigger" works on actual button
      Not stub button

[ ] 7. Multiple edits stack
      3+ edits all visible in final blueprint

[ ] 8. Error handling
      Invalid command → Error 400
      Unsupported command → Error 422

[ ] 9. Code generation
      React code matches REAL blueprint
      Not stub code

[ ] 10. Canvas updates
       Design changes visible after each edit
       Multiple edits show compound effects

RESULT: [ ] ALL PASS ← Ready for production
```

---

## What Changes With AI_MODE=on

### Vision Flow Changes
```
BEFORE (AI_MODE=off):
  Upload → Filename check → Stub blueprint
  (design.jpg → landing blueprint)
  
AFTER (AI_MODE=on):
  Upload → Save file → Gemini vision analysis → Real blueprint
  (any image → Gemini analyzes → Components extracted)
```

### Example: Real Image Processing

**Your image:** Screenshot of Shopify store

**Gemini sees:**
```
- Header with logo and navigation
- Hero section with banner image
- Product grid (6 products)
- Filter sidebar
- Footer with links
```

**Blueprint generated:**
```json
{
  "components": [
    {"id": "header_1", "type": "header", ...},
    {"id": "hero_1", "type": "hero", ...},
    {"id": "product_grid_1", "type": "container", ...},
    {"id": "filter_sidebar_1", "type": "container", ...},
    {"id": "footer_1", "type": "footer", ...}
  ]
}
```

**NOT the stub landing page!**

---

## Fallback Behavior

If Gemini API fails for ANY reason:
```
Upload image
  ↓
Try Gemini (needs API key)
  ↓
API error? (quota, timeout, invalid key)
  ↓
Auto-fallback to deterministic stub
  ↓
User gets working blueprint (not error!)
```

**System stays stable even if API fails** ✓

---

## Cost Note

Google Gemini is **FREE** for testing:
- 60 requests per minute (free tier)
- Perfect for 1-2 hour testing session
- No credit card needed

After free tier: $0.075 per 1M input tokens

For testing: You'll spend $0-0.10 max

---

## Troubleshooting

### "GOOGLE_API_KEY not set" in logs
→ Environment variable not loaded
→ Restart PowerShell, set again
→ Use Option B (.env file) for persistence

### "INVALID API KEY" error
→ Check key format (AIzaSy...)
→ Go back to https://aistudio.google.com/apikey
→ Get new key, try again

### "ModuleNotFoundError: No module named 'google'"
→ Run: `pip install google-generativeai`
→ Restart backend

### "Quota exceeded"
→ Hit free tier limit (60 req/min)
→ Wait a minute, try again
→ Or use stub mode temporarily

### Gemini returns wrong blueprint
→ API analyzed correctly, but structure doesn't match schema
→ Backend auto-falls back to stub
→ Check backend logs for details

---

## How to Verify AI Mode is ON

### Method 1: Check Startup Message
```powershell
# Look for this line:
# "Starting server with AI_MODE=on (using Gemini API)..."

# NOT this:
# "Starting server with AI_MODE=off (using deterministic stub)..."
```

### Method 2: Check Backend Logs During Upload
```
Look for:
  "Calling Gemini to analyze image..."
  or
  "Gemini API response: {...}"

NOT:
  "Using stub blueprint"
```

### Method 3: Check Blueprint Differs From Stub
```
Upload your image
  ↓
Look at blueprint JSON
  ↓
If it has your image's components (not landing page stub)
  → AI_MODE is working ✓
```

---

## Complete Command to Start With AI

```powershell
# Set API key and enable AI mode
$env:GOOGLE_API_KEY = "AIzaSy..." # Replace with your key
$env:AI_MODE = "on"

# Kill old process
Stop-Process -Name python -Force -ErrorAction SilentlyContinue

# Start backend fresh
cd C:\Users\ASUS\Desktop\design-to-code\ai-ui-builder
python run_server.py
```

**Expected output:**
```
Starting server with AI_MODE=on (using Gemini API)...
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000
```

---

## After API Key Ready

1. Give me your API key ✓
2. I'll set up the environment ✓
3. Start backend with AI_MODE=on ✓
4. Test full pipeline ✓
5. Verify everything works ✓

**Then you'll have complete end-to-end testing with:**
- ✓ Real image upload
- ✓ Gemini vision analysis
- ✓ Blueprint extraction
- ✓ Edit commands
- ✓ Code generation

All working together!

---

**Ready to enable full AI? Get your API key and I'll set it up.**

