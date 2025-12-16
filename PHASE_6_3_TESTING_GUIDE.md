# PHASE 6.3 TESTING GUIDE

## Prerequisites

### 1. Start Backend
```powershell
cd c:\Users\ASUS\Desktop\design-to-code\ai-ui-builder
python run_server.py
```
**Expected:** Backend running on `http://127.0.0.1:8002`

Check endpoints:
- `POST /enhance` → Available
- Responds with `{patched_blueprint, summary}`

### 2. Start Frontend
```powershell
cd frontend
npm run dev
```
**Expected:** Frontend running on `http://localhost:5173`

### 3. Verify Both Running
```
✅ Backend: http://127.0.0.1:8002
✅ Frontend: http://localhost:5173
```

---

## Test 1: Component Loads

**Steps:**
1. Open browser → `http://localhost:5173`
2. Upload a test image (any design image)
3. Wait for blueprint to generate

**Expected:**
```
Upload Page visible with:
  ├─ Step 1: Upload Section
  ├─ Step 2: Edit Design (NEW)
  │   ├─ Design Command input field
  │   ├─ Apply Edit button
  │   └─ Example commands shown
  └─ Step 3: Generated Code (was Step 2)
```

**Verify:**
- [ ] EditCommandInput component renders
- [ ] Input field is enabled (blueprint loaded)
- [ ] "Apply Edit" button visible
- [ ] Example commands displayed

---

## Test 2: Valid Command - Make Button Bigger

**Setup:**
- Blueprint loaded from image upload

**Steps:**
1. Click in "Design Command" field
2. Type: `Make button bigger`
3. Click "Apply Edit"
4. Wait 2-3 seconds

**Expected:**
```
Console Output:
  POST http://127.0.0.1:8002/enhance
  Status: 200
  Response: {
    "patched_blueprint": {...},
    "summary": "Increased button height from..."
  }

Frontend Display:
  ├─ Success message appears (green)
  ├─ Shows: "Edit applied: Increased button..."
  ├─ Canvas re-renders (design changes)
  ├─ Code regenerates automatically
  └─ Input clears, ready for next command
```

**Verify:**
- [ ] No console errors
- [ ] /enhance POST sent
- [ ] Success message shows
- [ ] Design actually changes on canvas
- [ ] Code box updates

---

## Test 3: Valid Command - Change Color

**Setup:**
- Previous edit still applied

**Steps:**
1. Type: `Change primary color to #FF5733`
2. Click "Apply Edit"
3. Wait 2-3 seconds

**Expected:**
```
Backend Response:
  {
    "patched_blueprint": {
      ...
      "components": [{...color: "#FF5733"...}]
    },
    "summary": "Changed primary color from..."
  }

Frontend:
  ├─ Success message appears
  ├─ Canvas shows new colors
  ├─ Code regenerates
  └─ Previous edit (button size) STILL APPLIED
```

**Verify:**
- [ ] Second edit stacks on first
- [ ] Design shows both changes
- [ ] Code has both changes

---

## Test 4: Invalid Command - Too Vague

**Steps:**
1. Type: `Redesign page`
2. Click "Apply Edit"

**Expected:**
```
Backend Response (400):
  {
    "error": "Invalid command: too vague, be specific"
  }

Frontend:
  ├─ Error message appears (red)
  ├─ Shows: "Invalid command: too vague, be specific"
  ├─ Design UNCHANGED
  ├─ Code UNCHANGED
  └─ Input still has text (user can fix)
```

**Verify:**
- [ ] Error message appears
- [ ] No design changes
- [ ] Input kept for user correction

---

## Test 5: Unsupported Command - Not Yet Implemented

**Steps:**
1. Type: `Add AI animation`
2. Click "Apply Edit"

**Expected:**
```
Backend Response (422):
  {
    "error": "Command not yet supported: animations"
  }

Frontend:
  ├─ Error message appears (orange)
  ├─ Shows: "Command not yet supported: animations"
  ├─ Design UNCHANGED
  └─ Input kept
```

**Verify:**
- [ ] Distinguishes from invalid (400) vs unsupported (422)
- [ ] Design not changed

---

## Test 6: No Blueprint Loaded

**Steps:**
1. Refresh page
2. Look at Step 2 (Edit Design section)

**Expected:**
```
Edit Design section appears BUT:
  ├─ Input field: DISABLED
  ├─ Button: DISABLED
  ├─ Text: "Load a design first"
  └─ NO error message
```

**Verify:**
- [ ] Component gracefully handles missing blueprint
- [ ] User sees clear message

---

## Test 7: Server Error (500)

**Setup:**
- Backend crashes or returns error

**Steps:**
1. Stop backend server
2. Type command in frontend
3. Click "Apply Edit"
4. Wait for error

**Expected:**
```
Frontend Error:
  ├─ "Server error" message appears (red)
  ├─ No design change
  ├─ Input kept
```

**Verify:**
- [ ] Handles server unavailable gracefully
- [ ] Shows error message

---

## Test 8: Edit Stacking (Sequential Edits)

**Setup:**
- Fresh blueprint loaded

**Steps:**
```
1. Type: "Make button bigger"        → Apply
2. Type: "Increase padding 20px"    → Apply
3. Type: "Change text to bold"      → Apply
```

**Expected:**
```
After Step 1:
  Blueprint: {button.height: 60}
  
After Step 2:
  Blueprint: {button.height: 60, padding: 20}
  
After Step 3:
  Blueprint: {button.height: 60, padding: 20, text.bold: true}
  
Final Code:
  ✅ Button is bigger
  ✅ Has padding
  ✅ Text is bold
  (All changes visible)
```

**Verify:**
- [ ] Each edit compounds on previous
- [ ] No data loss between edits
- [ ] Final code has all changes

---

## Test 9: Network Latency

**Setup:**
- Chrome DevTools open (F12)

**Steps:**
1. Go to Network tab
2. Set throttle to "Slow 3G"
3. Type command and submit
4. Watch network tab

**Expected:**
```
Network Tab:
  ├─ POST /enhance shows (takes 3-5s)
  ├─ Response body shows patched blueprint
  
Frontend UI:
  ├─ Button shows "Loading..." state
  ├─ Input disabled during request
  ├─ After response: displays result
```

**Verify:**
- [ ] UI doesn't break on slow network
- [ ] User can't double-submit

---

## Test 10: Special Characters in Command

**Steps:**
1. Type: `Change text to "Hello & Welcome!"`
2. Click "Apply Edit"

**Expected:**
```
Backend Receives:
  {
    "blueprint": {...},
    "command": "Change text to \"Hello & Welcome!\""
  }

Processing:
  ✅ JSON escaping handled correctly
  ✅ Special chars not corrupted
  
Frontend:
  ✅ Success message shows
  ✅ Design updates
```

**Verify:**
- [ ] JSON encoding/decoding works
- [ ] No corruption of special characters

---

## Browser Console Checks

During all tests, console should show:

✅ **Good:**
```javascript
POST http://127.0.0.1:8002/enhance
{blueprint: {...}, command: "..."}
Response: 200 OK
{patched_blueprint: {...}, summary: "..."}
```

❌ **Bad:**
```javascript
Uncaught Error: EditCommandInput is not defined
Failed to fetch - CORS error
JSON.parse() error
undefined is not a function
```

**Check Console:**
- [ ] No red errors
- [ ] No CORS warnings
- [ ] Network calls complete successfully

---

## Debugging Checklist

If a test fails:

### Test 1 Failed (Component not rendering)
```powershell
# Check EditCommandInput.jsx exists
ls frontend/src/components/EditCommandInput.jsx

# Check import in UploadPage.jsx
grep "EditCommandInput" frontend/src/pages/UploadPage.jsx
```

### Test 2 Failed (Command not received)
```powershell
# Check backend logs
# Should see: "Received command: Make button bigger"

# Check fetch in EditCommandInput
# Look for: POST http://127.0.0.1:8002/enhance
```

### Test 3 Failed (Edits not stacking)
```python
# In run_server.py terminal, look for:
# POST /enhance (first call)
# POST /enhance (second call with updated blueprint)

# If not stacking, check handleBlueprintUpdate in UploadPage
```

### Test 8 Failed (Design doesn't update)
```javascript
// In console, check:
console.log(blueprint) // Should show updated values
console.log(generatedFiles) // Should show new code
```

---

## Test Summary Template

After running all tests, fill this:

```
PHASE 6.3 TEST RESULTS
=====================

Test 1 (Component Loads):        [ PASS / FAIL ]
Test 2 (Valid Command - Button): [ PASS / FAIL ]
Test 3 (Valid Command - Color):  [ PASS / FAIL ]
Test 4 (Invalid Command):        [ PASS / FAIL ]
Test 5 (Unsupported Command):    [ PASS / FAIL ]
Test 6 (No Blueprint):           [ PASS / FAIL ]
Test 7 (Server Error):           [ PASS / FAIL ]
Test 8 (Edit Stacking):          [ PASS / FAIL ]
Test 9 (Network Latency):        [ PASS / FAIL ]
Test 10 (Special Characters):    [ PASS / FAIL ]

Console Errors:       [ 0 / N ]
Network Errors:       [ 0 / N ]

Status: [ READY TO MERGE / NEEDS FIXES ]
```

---

## Quick Test (5 minutes)

If time is short, run these only:

1. ✅ Component loads (Test 1)
2. ✅ Valid command works (Test 2)
3. ✅ Invalid command handled (Test 4)
4. ✅ Edit stacking (Test 8)

**If all 4 pass → GREEN LIGHT for integration**

---

## Full Test (20 minutes)

Run all 10 tests in order.

**If all 10 pass → PRODUCTION READY**

---

## Next Steps

After testing:
1. Document any failures
2. Fix issues in EditCommandInput.jsx or UploadPage.jsx
3. Re-run failing tests
4. Get to all PASS
5. Merge into main branch
