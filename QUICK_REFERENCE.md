# QUICK REFERENCE CARD

## System URLs
```
Backend:    http://127.0.0.1:8000
Frontend:   http://localhost:5174
Health:     http://127.0.0.1:8000/health
```

## Key Endpoints
```
POST /upload/     - Upload image → Blueprint
POST /generate/   - Blueprint → React/HTML/CSS code
POST /enhance/    - Blueprint + Command → Patched Blueprint
```

## What Was Fixed

| Issue | File(s) | Fix |
|-------|---------|-----|
| Invalid types | `vision_stub.py` | Changed hero_section→hero, text_section→text, etc. |
| API port | `UploadPage.jsx`, `EditCommandInput.jsx` | Changed 8002→8000 |
| Python cache | `__pycache__/` | Cleared all bytecode |
| AI_MODE fixed | `run_server.py` | Now reads from env variable |

## Valid Component Types

✅ Valid:
```
header, title, subtitle, description, text,
button, cta, image, product_card, container,
list, card, section, hero, footer
```

❌ Invalid (Don't use as type):
```
hero_section, text_section, feature_card, 
bullet_list, cta_button (as type only)
```

## Edit Command Examples

✅ Valid:
```
"Make button bigger"
"Change primary color to #FF5733"
"Increase heading size"
"Move CTA to bottom"
"Add padding 20px"
```

❌ Invalid:
```
"Redesign page" (too vague)
"Make it pretty" (too vague)
"Do something" (not specific)
```

## Blueprint Structure

```json
{
  "screen_id": "landing",
  "screen_type": "landing",
  "orientation": "portrait",
  "tokens": {
    "primary_color": "#EF4444",
    "accent_color": "#F97316",
    "base_spacing": 16
  },
  "components": [
    {
      "id": "hero_section_1",
      "type": "hero",           ← VALID (not hero_section)
      "bbox": [0, 0, 375, 180],
      "text": "...",
      "role": "hero",
      "confidence": 0.96,
      "visual": {
        "bg_color": "#EF4444"
      }
    }
  ]
}
```

## Edit Workflow

```
1. User Types:     "Make button bigger"
2. Frontend POSTs: {blueprint, command} → /enhance
3. Backend:        Validates → Patches → Returns patched blueprint
4. Frontend:       Updates state → Re-renders → Regenerates code
5. Result:         User sees design update in real-time
```

## Response Codes

| Code | Meaning | Example |
|------|---------|---------|
| 200 | Success | "Edit applied: Increased height..." |
| 400 | Invalid command | "Command too vague, be specific" |
| 422 | Unsupported command | "Animations not yet supported" |
| 500 | Server error | Backend crashed |

## Testing Checklist

Quick 1-minute test:
```
[ ] Backend running (port 8000)
[ ] Frontend running (port 5174)
[ ] Upload image (no errors)
[ ] Blueprint displays (valid types)
[ ] Edit input appears
[ ] Type "Make button bigger"
[ ] Click "Apply Edit"
[ ] See success message
[ ] Blueprint updates
```

## Environment Variables

```powershell
# Use stub (default)
AI_MODE=off

# Use Gemini
AI_MODE=on
GOOGLE_API_KEY=your-key-here
```

## Important Notes

1. **Component IDs are PERMANENT**
   - hero_section_1 → always hero_section_1
   - IDs NEVER change during edits

2. **Component types MUST be valid**
   - Must be from allowed list
   - Not internal names

3. **Edits STACK**
   - Multiple commands compound
   - No data loss
   - Each edit on previous result

4. **State is local**
   - React hooks
   - Upload clears state
   - No server-side persistence

## Troubleshooting

### "Invalid blueprint: Component X has invalid type"
→ Check vision_stub.py types
→ Clear __pycache__ and restart

### "Failed to fetch"
→ Check backend running on 8000
→ Check frontend calling 8000 (not 8002)

### "Invalid command"
→ Be more specific
→ Use examples from UI

### Edits not applying
→ Check browser console (F12)
→ Check backend logs
→ Verify blueprint valid

### Code not regenerating
→ Check handleBlueprintUpdate called
→ Check generateCode runs after edit
→ Verify state updated

## Documentation

Start here:
```
EXECUTIVE_SUMMARY.md ← Overview
SYSTEM_READY_FOR_TESTING.md ← Architecture
DETAILED_FIX_LOG.md ← Exact changes made
PHASE_6_3_END_TO_END_TEST.md ← 8 full tests
```

## One-Minute Sanity Check

```python
# Run in Python terminal
from backend.ai.vision_stub import _create_landing_blueprint
from backend.models.schemas import ALLOWED_COMPONENT_TYPES

blueprint = _create_landing_blueprint()
for c in blueprint['components']:
    if c['type'] not in ALLOWED_COMPONENT_TYPES:
        print(f"ERROR: {c['id']} has invalid type {c['type']}")
    else:
        print(f"OK: {c['id']} type '{c['type']}' is valid")

# Expected: All OK
```

## Success Indicators

✅ Blueprint loads without validation errors
✅ Edit input appears after upload
✅ Can type and submit edit command
✅ Blueprint updates
✅ Code regenerates
✅ Multiple edits stack
✅ Invalid commands show error

## Production Readiness

- [ ] All component types valid
- [ ] API port correct (8000)
- [ ] Frontend integration working
- [ ] Edit stacking verified
- [ ] Error handling working
- [ ] Code regenerates
- [ ] No console errors
- [ ] Multiple tests pass

All checked → **READY TO MERGE**

---

**Status: System Fixed and Ready**

Open http://localhost:5174 now

