# PHASE 6.1: Command UX Contract

**Status:** FROZEN (No backend implementation yet)

**Purpose:** Define what commands are allowed, what they do, and what they cannot do.

---

## Command Categories (Allowed)

### 1. Layout Commands
Modify component positioning, sizing, spacing within bounds.

**Valid examples:**
- "Make header smaller"
- "Increase padding"
- "Move CTA to bottom"
- "Make button wider"
- "Reduce spacing between sections"

**Implementation:** Modifies `bbox` (position/size), `spacing` tokens

---

### 2. Visual Commands
Change colors, opacity, borders, shadows.

**Valid examples:**
- "Change primary color to #FF5733"
- "Make button darker"
- "Change accent to blue"
- "Add border to product cards"

**Implementation:** Modifies `tokens` (primary_color, accent_color), `visual` object

---

### 3. Component Commands
Modify specific component properties (size, state, style).

**Valid examples:**
- "Make images larger"
- "Increase product image size"
- "Make CTA button bigger"
- "Make text bolder"

**Implementation:** Modifies component `bbox`, `visual.font_weight`, `visual.size`

---

### 4. CTA Commands
Modify call-to-action button specifically.

**Valid examples:**
- "Make CTA more prominent"
- "Make button taller"
- "Move button to top"

**Implementation:** Targets component with `role: "cta"`, modifies bbox/visual

---

### 5. Text Commands
Modify text styling (font size, weight, line height).

**Valid examples:**
- "Make title larger"
- "Make heading bold"
- "Increase font size"

**Implementation:** Modifies `font_size`, `font_weight`, `line_height` in visual

---

## Command Scope Resolution (Priority Order)

When a command doesn't explicitly name a component, resolve scope like this:

### 1. Explicit Component Match (Highest Priority)
```
"Make the BUTTON bigger"  → Targets component with type="button"
"Change the HEADER color" → Targets component with type="header"
"Make IMAGE larger"       → Targets component with type="image"
```

### 2. Role-Based Match
```
"Make CTA bigger"    → Targets component with role="cta"
"Change hero color"  → Targets component with role="hero"
"Increase content"   → Targets component with role="content"
```

### 3. Token-Level Change (Lowest Priority)
```
"Change primary color"  → Modifies tokens.primary_color (affects ALL components using it)
"Increase spacing"      → Modifies tokens.base_spacing
```

---

## Command Rejection Rules (STRICT)

These commands MUST be rejected with HTTP 400 + human error message:

### Vague/Design Commands (NO Implementation)
```
❌ "Redesign page"
❌ "Make it modern"
❌ "Improve UX"
❌ "Make it better"
❌ "Add more pizzazz"
❌ "Make it pop"
```

### Layout Restructuring (NO Schema Change)
```
❌ "Add a new button"
❌ "Remove the header"
❌ "Reorganize the layout"
❌ "Create a grid"
```

### Unsupported Transformations
```
❌ "Animate the button"
❌ "Add hover effects"
❌ "Change the theme completely"
❌ "Add dark mode"
```

### Invalid/Broken Commands
```
❌ "" (empty command)
❌ "Lorem ipsum" (gibberish)
❌ Very long rambling sentences (>100 words)
```

---

## Valid Command Structure

A valid command MUST:

1. ✅ Be 5-50 words
2. ✅ Target ONE measurable change
3. ✅ Use imperative voice ("Make", "Change", "Increase", "Move")
4. ✅ Reference valid properties (color, size, spacing, position)
5. ✅ Use valid values (hex colors, numbers, directions like "top"/"bottom")
6. ✅ NOT add/remove/restructure components
7. ✅ NOT invent new properties

---

## Property Modification Rules

### Properties That CAN Change

| Property | Type | Example | Constraint |
|----------|------|---------|-----------|
| `tokens.primary_color` | hex | #FF5733 | Valid hex only |
| `tokens.accent_color` | hex | #FFB300 | Valid hex only |
| `tokens.base_spacing` | number | 12 | Positive, ≤ 32 |
| `tokens.border_radius` | string | "12px" | Valid CSS |
| `components[].bbox[2]` | number | 220 | Width, positive |
| `components[].bbox[3]` | number | 52 | Height, positive |
| `components[].visual.font_size` | number | 24 | Positive, ≤ 72 |
| `components[].visual.font_weight` | string | "bold" | valid CSS |

### Properties That CANNOT Change

| Property | Reason |
|----------|--------|
| `screen_id` | Structural identity |
| `screen_type` | Schema definition |
| `components[].id` | Component identity |
| `components[].type` | Component type |
| `components[].role` | Component semantic role |
| `components` array length | No add/remove |

---

## Error Responses (HTTP Codes)

### 400 Bad Request
- Empty or null command
- Blueprint is invalid (missing keys, bad structure)
- Command is vague/rejected (redesign, etc.)
- Invalid color format

Example:
```json
{
  "error": "Invalid command: 'redesign page' is too vague",
  "code": "VAGUE_COMMAND"
}
```

### 422 Unsupported
- Command is valid but not yet implemented
- Feature requires schema change

Example:
```json
{
  "error": "Command not supported: animations",
  "code": "UNSUPPORTED_COMMAND"
}
```

### 500 Server Error
- Unexpected crash

---

## Command Examples (Accepted vs Rejected)

### ✅ ACCEPTED

| Command | Scope | Action |
|---------|-------|--------|
| "Make button bigger" | button component | Increase bbox height 20% |
| "Change primary color to #FF5733" | tokens | Update primary_color |
| "Increase heading size" | heading component | Increase font_size 20% |
| "Add more spacing" | tokens | Increase base_spacing |
| "Make CTA taller" | role:cta | Increase button height |
| "Move button to bottom" | role:cta | Modify bbox Y position |

### ❌ REJECTED

| Command | Reason |
|---------|--------|
| "Redesign page" | Vague, no measurable change |
| "Add a button" | Adds component (schema change) |
| "Make it modern" | Vague, no specific property |
| "Animate on click" | Unsupported feature |
| "" | Empty |
| "the quick brown fox..." | Gibberish |

---

## Implementation Checklist

- [ ] Command rules documented (THIS FILE)
- [ ] Scope resolution order defined
- [ ] Rejection rules frozen
- [ ] Property modification rules locked
- [ ] Error codes and responses standardized
- [ ] Example commands catalogued
- [ ] Shared with frontend team

---

## Frozen Effective Date

**Locked:** December 15, 2025

**Any changes require team alignment AND frontend/backend re-sync.**

---

Next Phase: **6.2 — Edit Agent API** (Implement /enhance endpoint)
