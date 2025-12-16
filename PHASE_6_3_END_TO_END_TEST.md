# COMPLETE END-TO-END SYSTEM TEST (PHASE 6.3)

## System Status

✅ **Backend:** http://127.0.0.1:8000 (AI_MODE=off, using stub blueprint)
✅ **Frontend:** http://localhost:5174 (port shifted due to 5173 in use)
✅ **Database:** In-memory (blueprint state)

---

## What You're Testing

**PHASE 6.3: Edit Commands Workflow**

```
1. Upload Image
   ↓
2. Get Blueprint (from AI or stub)
   ↓
3. Validate Blueprint
   ↓
4. User Types Edit Command
   ↓
5. POST /enhance (send blueprint + command)
   ↓
6. Backend patches blueprint
   ↓
7. Frontend updates canvas
   ↓
8. Code regenerates
```

---

## Step 1: Open Browser

Go to: **http://localhost:5174**

You should see:
```
┌─────────────────────────────────────────┐
│  AI UI Builder - Design to Code        │
├─────────────────────────────────────────┤
│                                         │
│  STEP 1: Upload Design                  │
│  ┌─────────────────────┐                │
│  │ Choose File         │                │
│  └─────────────────────┘                │
│                                         │
│  (STEP 2 and 3 appear after upload)     │
│                                         │
└─────────────────────────────────────────┘
```

---

## Step 2: Upload Any Image

**Action:** Click "Choose File" and select ANY image (jpg, png, etc.)

**Result:**
- File selected
- Click "Upload Design"
- Wait 2-3 seconds

**Expected Output:**
```
STEP 1 ✓ Complete
  Filename: design.jpg

STEP 2: Edit Design (NEW)
  ┌─────────────────────────────────────────┐
  │ Design Command                          │
  │ ┌─────────────────────────────────────┐ │
  │ │ Make button bigger                  │ │
  │ └─────────────────────────────────────┘ │
  │ [Apply Edit]                            │
  │                                         │
  │ Examples:                               │
  │ • "Make button bigger"                  │
  │ • "Change primary color to #FF5733"    │
  │ • "Increase padding 20px"              │
  └─────────────────────────────────────────┘

STEP 3: Generated Code
  (HTML, CSS, React code shown)
```

---

## Step 3: Check Blueprint

**Action:** Look at the "Blueprint" tab

**Expected Blueprint Structure:**

```json
{
  "screen_id": "landing",
  "screen_type": "landing",
  "orientation": "portrait",
  "tokens": {
    "primary_color": "#EF4444",
    "accent_color": "#F97316"
  },
  "components": [
    {
      "id": "hero_section_1",
      "type": "hero",        ← VALID (not "hero_section")
      "bbox": [0, 0, 375, 180],
      "text": "...",
      "role": "hero",
      "confidence": 0.96,
      "visual": {...}
    },
    {
      "id": "feature_card_1",
      "type": "card",        ← VALID (not "feature_card")
      "bbox": [12, 200, 363, 300],
      ...
    }
  ]
}
```

**Component types MUST be ONE of:**
```
✅ Valid: 
  "header", "title", "subtitle", "description", "text",
  "button", "cta", "image", "product_card", "container",
  "list", "card", "section", "hero", "footer"

❌ Invalid (WILL ERROR):
  "hero_section" ← WRONG
  "text_section" ← WRONG
  "feature_card" ← WRONG
  "bullet_list" ← WRONG
```

---

## Step 4: Apply First Edit Command

**Action:** In STEP 2, type in the input field:

```
Make button bigger
```

Then click "Apply Edit"

**Expected Flow:**

```
Frontend:
  1. POST /enhance endpoint
     Body: {
       "blueprint": {...},
       "command": "Make button bigger"
     }
  
  2. Wait for response (2-3 seconds)
  
  3. Success message appears:
     "Edit applied: Increased button height from 44px to 56px"
  
  4. Blueprint state updates
  
  5. Canvas re-renders (if using preview)
  
  6. Code regenerates
  
  7. Input clears, ready for next command

Backend:
  1. Validates command (PHASE 6.1)
  2. Validates blueprint (PHASE 6.2)
  3. Patches blueprint
  4. Returns:
     {
       "patched_blueprint": {...updated...},
       "summary": "Increased button height..."
     }
```

**Check Console (F12 → Console tab):**
```javascript
✅ Good:
  POST http://127.0.0.1:8000/enhance
  Status: 200
  Response: {patched_blueprint: {...}, summary: "..."}

❌ Bad:
  Error: Failed to fetch
  Error: Invalid blueprint...
  Error: Component X has invalid type...
```

---

## Step 5: Apply Second Edit (Edit Stacking)

**Action:** Type another command:

```
Change primary color to #FF5733
```

Click "Apply Edit"

**Expected:**
- First edit still applied (button size changed)
- Second edit now applied (color changed)
- Code shows both changes

**Verify in Blueprint:**
```json
{
  "components": [
    {
      "id": "hero_section_1",
      "type": "hero",
      "visual": {
        "bg_color": "#FF5733"  ← CHANGED
      }
    },
    {
      "id": "cta_button_3",
      "type": "button",
      "visual": {
        "height": 56  ← STILL CHANGED FROM STEP 4
      }
    }
  ]
}
```

---

## Step 6: Test Error Handling

**Action:** Type an invalid command:

```
Redesign page
```

Click "Apply Edit"

**Expected:**
- Error message appears (RED)
- Message: "Invalid command: too vague, be specific"
- Blueprint NOT changed
- Code NOT changed
- Input still shows your text (for correction)

**Backend Response:**
```
Status: 400
{
  "error": "Invalid command: too vague, be specific"
}
```

---

## Complete Test Checklist

After running all tests, verify:

```
PHASE 6.3 TESTING CHECKLIST
===========================

[ ] 1. Upload Page Loads
      Blueprint data displayed

[ ] 2. Blueprint Validates
      No "Invalid type" errors
      All components have valid types
      (hero, card, text, list, header, button, etc.)

[ ] 3. Edit Command Input Appears
      Input field visible after upload
      "Apply Edit" button present
      Example commands shown

[ ] 4. Valid Command Works
      "Make button bigger" → Success
      Canvas updates (if preview enabled)
      Code regenerates
      Success message shows summary

[ ] 5. Second Command Stacks
      First edit still applied
      Second edit also applied
      Both visible in blueprint JSON
      Both visible in generated code

[ ] 6. Invalid Command Rejected
      "Redesign page" → Error 400
      Message explains why
      Design unchanged
      Code unchanged

[ ] 7. Console Clean
      No red errors
      POST requests complete 200
      JSON parsing works

[ ] 8. Multiple Edit Sequence
      Apply 3 different commands
      All edits compound
      Final blueprint has all changes
      Final code reflects all changes

RESULT: [ ] PASS  [ ] FAIL

If FAIL, which step failed? _________________
```

---

## If Tests Fail

### Scenario A: "Invalid blueprint: Component X has invalid type"

**Cause:** Component type not in ALLOWED_COMPONENT_TYPES

**Fix:**
1. Check blueprint JSON in browser
2. Find the component with invalid type
3. Compare against allowed list:
   - Valid: header, title, subtitle, description, text, button, cta, image, product_card, container, list, card, section, hero, footer
   - Invalid: hero_section, text_section, feature_card, bullet_list, cta_button (as types)
4. If invalid, vision_stub.py needs updating
5. Clear Python cache: `rm -r backend/__pycache__`
6. Restart server

### Scenario B: "/enhance endpoint returns 400 (Bad Request)"

**Check:** Command validator (PHASE 6.1)

**Common causes:**
- Command too vague ("Redesign page")
- Invalid syntax
- Missing required keywords

**Fix:**
- Use examples from UI
- Be specific: "Make button bigger" not "Update button"
- Use color format #RRGGBB not color names

### Scenario C: "/enhance endpoint returns 500 (Server Error)"

**Check:** Backend logs

**Common causes:**
- Blueprint missing required field
- Component ID mismatch
- Validation error

**Fix:**
- Check blueprint JSON structure
- Ensure all components have required fields
- Restart server

### Scenario D: Frontend not updating after edit

**Cause:** State not updating in React

**Fix:**
1. Check console for errors
2. Verify response has `patched_blueprint`
3. Check `handleBlueprintUpdate` in UploadPage.jsx
4. Hard refresh browser: Ctrl+Shift+R

---

## Success Criteria

✅ **PHASE 6.3 IS COMPLETE WHEN:**

1. Upload generates valid blueprint (valid component types)
2. Edit command input appears after upload
3. First edit command succeeds and returns patched blueprint
4. Second edit command stacks on first
5. Invalid command returns error 400 with reason
6. No page refresh needed between edits
7. Canvas updates (if using preview)
8. Code regenerates with each edit

---

## What Happens Behind the Scenes

### Upload Flow:
```
User uploads image
  ↓
Backend saves file to /uploads
  ↓
vision.py checks AI_MODE
  ↓
AI_MODE=off → Uses vision_stub.py
  ↓
Generates deterministic blueprint based on filename
  ↓
Validates blueprint schema
  ↓
Improves blueprint (spacing, tokens)
  ↓
Returns JSON
```

### Edit Flow:
```
User types: "Make button bigger"
  ↓
Frontend POSTs to /enhance
  Body: {blueprint, command}
  ↓
Backend validates command (PHASE 6.1 contract)
  ↓
Backend validates blueprint schema
  ↓
Backend patches blueprint (finds button, increases height)
  ↓
Backend returns:
  {
    patched_blueprint: {...updated...},
    summary: "Increased button height from 44px to 56px"
  }
  ↓
Frontend receives response
  ↓
Frontend updates blueprint state
  ↓
Canvas re-renders
  ↓
Code generator re-runs
  ↓
Updated code displayed
```

---

## Next Steps After Testing

✅ All 8 test points pass?
→ **PHASE 6.3 is PRODUCTION READY**
→ Ready to merge with Copilot backend

❌ Some points fail?
→ Fix issues using troubleshooting section
→ Re-run specific test
→ Document what failed

---

## Important Notes

- **AI_MODE is OFF by default** - This is correct!
- Blueprint comes from `vision_stub.py` - deterministic and reliable
- Edit commands use real Gemini-compatible patching logic
- All component types MUST be from ALLOWED_COMPONENT_TYPES
- IDs never change (hero_section_1 stays hero_section_1)
- Only component data mutates (text, colors, size, etc.)

Good luck! This should work end-to-end now. Report any failures with exact error message.
