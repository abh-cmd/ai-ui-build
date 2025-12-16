# PHASE 6.3: Frontend Patch Application

**Status:** SPECIFICATION (Not yet implemented - Frontend team responsibility)

**Date:** December 15, 2025

---

## Objective

Wire frontend to apply patched blueprints after `/enhance` response.

**Flow:**
```
User Types Command
  ↓
Frontend POST /enhance
  ↓
Backend returns {patched_blueprint, summary}
  ↓
Frontend replaces state.blueprint = patched_blueprint
  ↓
Canvas re-renders
  ↓
Codegen re-runs
  ↓
React code updated
  ↓
User sees change instantly
```

---

## Frontend Requirements

### 1. Command Input UI
- Single text input field
- Submit button
- Clear on success
- Show summary message
- No chat history

### 2. API Call Handler
```javascript
async function applyEdit(command, blueprint) {
  const response = await fetch('/enhance', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
      command: command,
      blueprint: blueprint
    })
  });
  
  if (!response.ok) {
    const error = await response.json();
    return { error: error.error, code: error.code };
  }
  
  return await response.json();  // {patched_blueprint, summary}
}
```

### 3. State Update Pattern
```javascript
// Before: state.blueprint = original_blueprint

// After command submission:
const {patched_blueprint, summary} = await applyEdit(command, blueprint);

if (patched_blueprint) {
  setBlueprint(patched_blueprint);  // Update state
  setMessage(summary);              // Show feedback
  // Canvas auto-updates (watching blueprint state)
}
```

### 4. Error Handling
```javascript
if (error) {
  if (code === 'INVALID_COMMAND') {
    showError("Command not allowed: " + error);
  } else if (code === 'INVALID_BLUEPRINT') {
    showError("Blueprint structure invalid");
  } else if (code === 'UNSUPPORTED_COMMAND') {
    showError("Command not yet supported");
  } else {
    showError("Server error: " + error);
  }
}
```

### 5. Canvas Re-render Trigger
```javascript
// Canvas component watches blueprint state
useEffect(() => {
  if (blueprint) {
    renderCanvas(blueprint);  // Update visual display
    generateCode(blueprint);  // Re-run codegen
  }
}, [blueprint]);
```

### 6. No Page Reload
- State update only (React)
- No `window.location.reload()`
- No navigation
- Instant feedback

---

## Backend Guarantees (Already Implemented)

✅ `/enhance` endpoint returns valid blueprint
✅ Schema always preserved
✅ Component IDs never change
✅ Component count unchanged
✅ Blueprint is safe to replace

---

## Testing Checklist

- [ ] Command input accepts text
- [ ] POST /enhance called with correct payload
- [ ] Error responses handled (400, 422, 500)
- [ ] Success response updates blueprint state
- [ ] Canvas re-renders immediately
- [ ] Codegen runs on new blueprint
- [ ] Summary message displays
- [ ] No page reload
- [ ] Multiple sequential commands work
- [ ] Mock mode still works

---

## Success Criteria

✅ User types "Make button bigger"
✅ Canvas shows bigger button instantly
✅ No page refresh
✅ Can apply multiple edits in sequence
✅ Error messages are clear
✅ Works in mock mode (no API required)

---

## Files to Modify (Frontend)

These files will be in `Antigravity/...` repo:

1. **Command Input Component**
   - New or modify existing editor
   - Single command field
   - Submit button

2. **API Client**
   - Add /enhance endpoint call
   - Error handling

3. **State Management**
   - Blueprint state update on /enhance response
   - Trigger canvas re-render

4. **Canvas Component**
   - Watch blueprint state changes
   - Re-render on change

---

## Expected Integration

```
Antigravity Frontend (Copilot to modify)
  ↓
  POST /enhance (Copilot backend)
  ↓
Copilot Backend (Already done)
  ↓
  Return {patched_blueprint, summary}
  ↓
Antigravity Frontend
  ↓
  Update state
  ↓
Canvas re-renders
```

---

## Merge Conditions (STRICT)

Merge is allowed ONLY WHEN:

✅ PHASE 6.1: Command contract frozen
✅ PHASE 6.2: /enhance endpoint live
✅ PHASE 6.3: Frontend wired to apply patches
✅ End-to-end test: Command → Patch → Render works
✅ Mock mode still functional
✅ No page reloads
✅ Schema preserved

---

## Note

**PHASE 6.3 is FRONTEND WORK.**

Backend (PHASE 6.1, 6.2) is COMPLETE.

Frontend integration is specified but not implemented.

Merge happens after frontend completes integration.

---
