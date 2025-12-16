# AI UI Builder - Temporary Frontend

This is a **temporary, minimal testing frontend** for validating backend API flows. It is NOT a final product UI.

## Purpose

- Test `/upload` endpoint (image → blueprint)
- Test `/enhance` endpoint (blueprint + command → patched blueprint)
- Test `/generate` endpoint (blueprint → React code files)
- Debug backend intelligence responses
- Enable rapid iteration on backend features

## Features

- **📤 Upload Image**: Upload a mockup image to generate blueprint
- **✏️ Edit Blueprint**: Apply natural language commands to modify blueprint
- **💻 Generate Code**: Convert blueprint to React component files
- **📋 Blueprint Viewer**: Inspect JSON blueprint in real-time
- **🔄 Iteration Loop**: Edit → Regenerate → Inspect

## Quick Start

### Prerequisites
- Node.js 16+
- Backend running on `http://127.0.0.1:8000`

### Installation

```bash
cd frontend_temp
npm install
```

### Run Development Server

```bash
npm run dev
```

The frontend will start on `http://127.0.0.1:5174`

### Build for Production

```bash
npm run build
```

## UI Layout

```
┌─────────────────┬──────────────────┬─────────────────┐
│   UPLOAD &      │   BLUEPRINT      │   GENERATED     │
│   EDIT          │   JSON           │   CODE          │
│                 │                  │                 │
│ • File Input    │ {               │ • filename.jsx  │
│ • Edit Textarea │   "components": │ • content...    │
│ • Apply Edit    │   [             │                 │
│ • Generate Code │     {...}       │ • filename.css  │
│                 │   ]             │ • content...    │
└─────────────────┴──────────────────┴─────────────────┘
```

## API Integration

### Upload Endpoint
```
POST /upload
Content-Type: multipart/form-data
Body: { file: <image file> }

Response: { blueprint: {...} }
```

### Edit Endpoint
```
POST /enhance
Content-Type: application/json
Body: { blueprint: {...}, command: "user command" }

Response: { patched_blueprint: {...}, summary: "..." }
```

### Generate Endpoint
```
POST /generate
Content-Type: application/json
Body: { blueprint: {...} }

Response: { files: [{filename: "...", content: "..."}, ...] }
```

## Testing Workflow

1. **Upload a mockup image**
   - Select an image file
   - Backend extracts components → blueprint JSON
   - View blueprint in middle panel

2. **Edit the blueprint**
   - Type a natural language command
   - Click "Apply Edit"
   - Blueprint updates with changes
   - Old code clears (user must regenerate)

3. **Generate code**
   - Click "⚡ Generate Code"
   - Backend converts blueprint → React files
   - View code in right panel

4. **Iterate**
   - Make more edits
   - Regenerate
   - Inspect changes

## Error Handling

- Network errors display in bottom-right error box
- Backend validation errors are shown with API error details
- Loading spinner prevents double-clicks during API calls
- Disabled buttons prevent invalid operations

## Styling

- **Plain CSS** (no Tailwind to avoid conflicts)
- **3-column responsive grid** (adapts to smaller screens)
- **Dark code viewers** for readability
- **Color-coded buttons** (green for edit, blue for generate)

## Notes

- This frontend is TEMPORARY and will be replaced
- Do NOT use in production
- Backend is the source of truth
- Focus on API intelligence validation
- Frontend refactoring can wait until backend is stable

## Dependencies

- **React 18.2.0**: UI framework
- **Vite 5.0.0**: Fast bundler
- **Axios 1.6.0**: HTTP client
- Plain CSS (no frameworks)

## Project Structure

```
frontend_temp/
├── src/
│   ├── App.jsx          (Main app logic)
│   ├── main.jsx         (React entry point)
│   └── index.css        (Styling)
├── index.html           (HTML template)
├── vite.config.js       (Vite configuration)
├── package.json         (Dependencies)
└── README.md            (This file)
```

## Troubleshooting

**Issue: "Cannot connect to backend"**
- Ensure backend is running on `http://127.0.0.1:8000`
- Check CORS settings if backend is on different origin

**Issue: "Generate Code button disabled"**
- Upload an image first to create a blueprint
- Blueprint must exist before code generation

**Issue: "Edit failed" error**
- Command may be too complex or malformed
- Check backend logs for validation errors
- Try simpler commands

---

**This is a development/testing frontend. Keep it minimal and focused.**
