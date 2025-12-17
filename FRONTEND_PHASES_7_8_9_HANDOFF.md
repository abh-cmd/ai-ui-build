# FRONTEND PHASES 7, 8, 9 - COMPLETE HANDOFF GUIDE

**Document Date:** December 17, 2025  
**Status:** Ready for implementation  
**Audience:** Frontend developer (your friend)  
**Backend Status:** ✅ PRODUCTION READY (do not modify)

---

## 🎯 Overview: What You're Building

You will implement the **frontend UI layer** for the design-to-code system while the main developer works on **Phase 11 (backend optimization)**. Your work is **100% independent** — the backend APIs are complete and ready.

### Three Phases to Complete (in any order):
1. **Phase 7:** Multi-page routing (Home, Store, About pages)
2. **Phase 8:** Live blueprint preview (visual rendering)
3. **Phase 9:** User iteration loop (edit commands, approve/reject)

**Total Estimated Work:** 8-12 hours across all three phases  
**Can be done in parallel or sequentially**

---

## 📋 System Architecture (Current State)

### Backend (READY - Don't Touch)
```
Frontend Upload (PNG/JPG)
    ↓
POST /upload/
    ↓ (Vision LLM analyzes design)
Blueprint JSON (design tokens + components)
    ↓
POST /edit/enhance (natural language commands)
    ↓ (Phase 10.2 multi-step executor)
Modified Blueprint (with rollback support)
    ↓
POST /generate/
    ↓ (Code generation)
React JSX files + Tailwind CSS
```

### Frontend (YOUR WORK)
```
Current State: Single Page App (SPA)
- Only UploadPage.jsx exists
- No routing framework
- No blueprint rendering
- No edit UI

Your Goal: Full-featured UI
- Phase 7: Add routing → multi-page support
- Phase 8: Add preview → visual rendering
- Phase 9: Add edit UI → user iteration
```

---

## 🏗️ Current Project Structure

```
frontend/
├── src/
│   ├── App.jsx                          ← Main entry point (NO ROUTING YET)
│   ├── main.jsx                         ← Vite entry
│   ├── index.css                        ← Tailwind CSS
│   ├── pages/
│   │   └── UploadPage.jsx               ← Only page that exists
│   └── components/
│       ├── BuilderLayout.jsx            ← Layout wrapper
│       ├── CanvasArea.jsx               ← Canvas rendering area
│       ├── GeneratedWebsite.jsx         ← Hard-coded landing page
│       ├── PreviewPanel.jsx             ← JSON display (will replace)
│       ├── EditCommandInput.jsx         ← Edit input (needs surfacing)
│       ├── BuilderSidebar.jsx           ← Sidebar (needs work)
│       ├── CodeViewer.jsx               ← Code display
│       ├── OptionPanels.jsx
│       ├── PropertiesPanel.jsx
│       └── UploadArea.jsx
├── package.json                         ← Dependencies (add React Router here)
├── vite.config.js
└── tailwind.config.js
```

### What Exists That You Can Use
- ✅ UploadPage.jsx (blueprint state management)
- ✅ BuilderLayout.jsx (layout structure)
- ✅ CanvasArea.jsx (rendering area)
- ✅ EditCommandInput.jsx (edit input field)
- ✅ PreviewPanel.jsx (display component - needs modification)
- ✅ Tailwind CSS configured

### What You Need to Build
- ❌ React Router setup
- ❌ Dynamic blueprint renderer
- ❌ Visual diff display
- ❌ Approval/rejection UI
- ❌ Edit history panel
- ❌ Page navigation UI

---

## 📡 Backend API Reference

### All Available Endpoints (Ready to use)

#### 1. Upload Design (Get Blueprint)
```
POST http://127.0.0.1:8000/upload/
Content-Type: multipart/form-data

Body: file=<image.png>

Response:
{
  "blueprint": {
    "tokens": {
      "primary_color": "#E63946",
      "accent_color": "#F1FAEE",
      "base_spacing": 16,
      "border_radius": 8,
      "font_scale": {"h1": 28, "h2": 20, "body": 14}
    },
    "components": [
      {
        "id": "navbar",
        "type": "navbar",
        "text": "Store Name",
        "bbox": [0, 0, 480, 60],
        "visual": {"color": "#FFFFFF", "bg_color": "#E63946", "height": 60}
      },
      // ... more components
    ]
  },
  "files": {
    "App.jsx": "... JSX code ...",
    "tokens.js": "... design tokens ...",
    // ... more files
  }
}
```

#### 2. Apply Edit Command
```
POST http://127.0.0.1:8000/edit/enhance
Content-Type: application/json

Body:
{
  "command": "Make the button bigger",
  "blueprint": { ... entire blueprint ... }
}

Response:
{
  "modified_blueprint": { ... updated blueprint ... },
  "reasoning": "Changed button height from 44px to 60px",
  "success": true
}
```

#### 3. Generate Code From Blueprint
```
POST http://127.0.0.1:8000/generate/
Content-Type: application/json

Body:
{
  "blueprint": { ... blueprint ... }
}

Response:
{
  "files": {
    "App.jsx": "... React code ...",
    "tokens.js": "... CSS tokens ...",
    "components/Button.jsx": "... component ..."
  }
}
```

#### 4. Health Check
```
GET http://127.0.0.1:8000/health

Response:
{
  "status": "ok"
}
```

---

## ⚡ Phase 7: Multi-Page Routing

### What Phase 7 Does
- User uploads different designs (store.png, about.png, company.png)
- Each generates different pages
- Frontend switches between pages using React Router
- User sees different designs rendered based on selected page

### Requirements
- [x] Install React Router v6
- [x] Create route structure (Home, Store, About, etc.)
- [x] Add page navigation UI
- [x] Store multiple blueprints in state
- [x] Render different generated code per page

### Implementation Steps

**Step 1: Install React Router**
```bash
npm install react-router-dom
```

**Step 2: Create pages for each design**
```javascript
// frontend/src/pages/StorefrontPage.jsx
export default function StorefrontPage() {
  // Render storefront design
}

// frontend/src/pages/AboutPage.jsx
export default function AboutPage() {
  // Render about design
}

// frontend/src/pages/LandingPage.jsx
export default function LandingPage() {
  // Render landing design
}
```

**Step 3: Update App.jsx with routing**
```javascript
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import UploadPage from './pages/UploadPage'
import StorefrontPage from './pages/StorefrontPage'
import AboutPage from './pages/AboutPage'
import LandingPage from './pages/LandingPage'

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/storefront" element={<StorefrontPage />} />
        <Route path="/about" element={<AboutPage />} />
        <Route path="/upload" element={<UploadPage />} />
      </Routes>
    </BrowserRouter>
  )
}
```

**Step 4: Add navigation UI**
```javascript
import { Link } from 'react-router-dom'

// Add to layout or navbar:
<nav>
  <Link to="/">Home</Link>
  <Link to="/storefront">Storefront</Link>
  <Link to="/about">About</Link>
  <Link to="/upload">Upload New</Link>
</nav>
```

**Step 5: Store pages independently**
```javascript
// In UploadPage or global state (use Context/Redux if needed)
const [pages, setPages] = useState({
  storefront: null,
  about: null,
  landing: null
})

const handleUpload = async (blueprintData) => {
  // Determine page type from image filename
  const pageType = determinePageType(filename) // 'storefront', 'about', etc.
  
  // Generate code
  const response = await fetch('http://127.0.0.1:8000/generate/', {
    method: 'POST',
    body: JSON.stringify({ blueprint: blueprintData })
  })
  
  const { files } = await response.json()
  
  // Store in pages object
  setPages(prev => ({
    ...prev,
    [pageType]: files
  }))
}
```

### Files to Create/Modify
- ✅ Create: `frontend/src/pages/StorefrontPage.jsx`
- ✅ Create: `frontend/src/pages/AboutPage.jsx`
- ✅ Create: `frontend/src/pages/LandingPage.jsx`
- ✅ Modify: `frontend/src/App.jsx` (add Router)
- ✅ Modify: `frontend/src/pages/UploadPage.jsx` (multi-page state)
- ✅ Modify: `frontend/package.json` (add React Router)

### Success Criteria
- [ ] React Router installed and working
- [ ] 4+ routes working (/upload, /, /storefront, /about)
- [ ] Navigation links switch pages
- [ ] Can upload multiple designs to different pages
- [ ] Each page shows its own generated code

---

## 🎨 Phase 8: Live Blueprint Preview

### What Phase 8 Does
- After uploading design, show **visual preview** not just JSON
- User types edit command → preview updates **live** showing changes
- Visual **diff display** shows what changed (highlight new vs old)
- Real-time rendering of blueprint as JSON

### Requirements
- [x] Dynamic blueprint-to-React rendering
- [x] Live update on blueprint change
- [x] Visual diff display
- [x] Component change highlighting
- [x] Real-time preview

### Implementation Steps

**Step 1: Create dynamic blueprint renderer**
```javascript
// frontend/src/components/BlueprintRenderer.jsx
export default function BlueprintRenderer({ blueprint }) {
  // Render blueprint JSON as visual design
  // Use blueprint.tokens for styling
  // Use blueprint.components for structure
  
  return (
    <div style={{
      backgroundColor: blueprint.tokens.accent_color,
      padding: blueprint.tokens.base_spacing
    }}>
      {blueprint.components.map(component => (
        <Component 
          key={component.id}
          data={component}
          tokens={blueprint.tokens}
        />
      ))}
    </div>
  )
}

function Component({ data, tokens }) {
  // Render individual component based on type
  // Types: button, navbar, product, text, container, etc.
  
  if (data.type === 'button') {
    return (
      <button style={{
        backgroundColor: tokens.primary_color,
        padding: tokens.base_spacing,
        borderRadius: tokens.border_radius,
        height: data.visual?.height || 44
      }}>
        {data.text}
      </button>
    )
  }
  // ... handle other types
}
```

**Step 2: Create diff viewer**
```javascript
// frontend/src/components/BlueprintDiff.jsx
export default function BlueprintDiff({ oldBlueprint, newBlueprint }) {
  // Compare blueprints
  // Highlight what changed
  
  return (
    <div className="grid grid-cols-2 gap-4">
      <div>
        <h3>Before</h3>
        <BlueprintRenderer blueprint={oldBlueprint} style={{opacity: 0.6}} />
      </div>
      <div>
        <h3>After</h3>
        <BlueprintRenderer blueprint={newBlueprint} style={{opacity: 1}} />
      </div>
      {/* Show component-level changes */}
      <div className="col-span-2">
        <h4>Changes:</h4>
        {getChanges(oldBlueprint, newBlueprint).map(change => (
          <div key={change.id} className="bg-yellow-100 p-2 my-1">
            {change.description}
          </div>
        ))}
      </div>
    </div>
  )
}

function getChanges(old, new_bp) {
  const changes = []
  
  // Compare tokens
  Object.keys(new_bp.tokens).forEach(key => {
    if (old.tokens[key] !== new_bp.tokens[key]) {
      changes.push({
        id: `token-${key}`,
        description: `${key}: ${old.tokens[key]} → ${new_bp.tokens[key]}`
      })
    }
  })
  
  // Compare components
  new_bp.components.forEach((comp, idx) => {
    if (JSON.stringify(old.components[idx]) !== JSON.stringify(comp)) {
      changes.push({
        id: comp.id,
        description: `Component "${comp.id}" was modified`
      })
    }
  })
  
  return changes
}
```

**Step 3: Integrate into UploadPage**
```javascript
// frontend/src/pages/UploadPage.jsx
export default function UploadPage() {
  const [blueprint, setBlueprint] = useState(null)
  const [previousBlueprint, setPreviousBlueprint] = useState(null)
  const [showDiff, setShowDiff] = useState(false)

  const handleEdit = async (command) => {
    setPreviousBlueprint(blueprint) // Save old version
    
    const response = await fetch('http://127.0.0.1:8000/edit/enhance', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ command, blueprint })
    })
    
    const { modified_blueprint } = await response.json()
    setBlueprint(modified_blueprint)
    setShowDiff(true) // Show what changed
  }

  return (
    <div>
      {/* Upload area */}
      <UploadArea onUpload={setBlueprint} />
      
      {/* Edit command input */}
      {blueprint && (
        <EditCommandInput onEdit={handleEdit} />
      )}
      
      {/* Live preview */}
      {blueprint && (
        <>
          {showDiff && previousBlueprint && (
            <BlueprintDiff 
              oldBlueprint={previousBlueprint}
              newBlueprint={blueprint}
            />
          )}
          {!showDiff && (
            <BlueprintRenderer blueprint={blueprint} />
          )}
        </>
      )}
    </div>
  )
}
```

### Files to Create/Modify
- ✅ Create: `frontend/src/components/BlueprintRenderer.jsx`
- ✅ Create: `frontend/src/components/BlueprintDiff.jsx`
- ✅ Modify: `frontend/src/pages/UploadPage.jsx` (integrate preview)
- ✅ Replace: `frontend/src/components/PreviewPanel.jsx` (use new renderer)

### Success Criteria
- [ ] Blueprint renders as visual design (not JSON)
- [ ] Colors and spacing from tokens applied
- [ ] Edit command updates preview live
- [ ] Diff viewer shows before/after
- [ ] Changed components highlighted
- [ ] All component types render correctly

---

## ✏️ Phase 9: User Iteration Loop

### What Phase 9 Does
- User sees **current blueprint** (JSON or visual)
- User enters **edit command** ("make button bigger")
- System shows **proposed changes** with approve/reject buttons
- User **accepts or rejects** changes
- **Edit history** shows all changes made
- **Undo/Redo** functionality

### Requirements
- [x] Blueprint visibility in UI
- [x] Edit command input visible
- [x] Approve/reject buttons
- [x] Edit history display
- [x] Undo/redo functionality
- [x] Confidence score display

### Implementation Steps

**Step 1: Create blueprint editor panel**
```javascript
// frontend/src/components/BlueprintEditor.jsx
export default function BlueprintEditor({ blueprint, onBlueprintChange }) {
  const [showRaw, setShowRaw] = useState(false)
  
  return (
    <div className="w-full max-h-96 overflow-auto border rounded p-4">
      <div className="flex justify-between mb-4">
        <h3 className="text-lg font-bold">Current Blueprint</h3>
        <button 
          onClick={() => setShowRaw(!showRaw)}
          className="text-sm px-2 py-1 bg-gray-200 rounded"
        >
          {showRaw ? 'Hide' : 'Show'} Raw JSON
        </button>
      </div>
      
      {showRaw ? (
        <pre className="bg-gray-100 p-4 rounded text-xs overflow-auto">
          {JSON.stringify(blueprint, null, 2)}
        </pre>
      ) : (
        <BlueprintRenderer blueprint={blueprint} />
      )}
    </div>
  )
}
```

**Step 2: Create edit history panel**
```javascript
// frontend/src/components/EditHistory.jsx
export default function EditHistory({ history, onUndo, onRedo, onRevert }) {
  return (
    <div className="border-l-4 border-blue-500 p-4">
      <h3 className="text-lg font-bold mb-4">Edit History</h3>
      
      <div className="space-y-2 mb-4">
        {history.length === 0 ? (
          <p className="text-gray-500">No edits yet</p>
        ) : (
          history.map((edit, idx) => (
            <div 
              key={idx}
              className="bg-blue-50 border-l-4 border-blue-500 p-3 cursor-pointer hover:bg-blue-100"
              onClick={() => onRevert(idx)}
            >
              <div className="font-semibold">{edit.command}</div>
              <div className="text-sm text-gray-600">{edit.reasoning}</div>
              <div className="text-xs text-gray-500 mt-1">
                Status: {edit.approved ? '✓ Accepted' : '⏳ Pending'}
              </div>
            </div>
          ))
        )}
      </div>
      
      <div className="flex gap-2">
        <button 
          onClick={onUndo}
          disabled={history.length === 0}
          className="px-4 py-2 bg-gray-300 rounded disabled:opacity-50"
        >
          ← Undo
        </button>
        <button 
          onClick={onRedo}
          disabled={history.length === 0}
          className="px-4 py-2 bg-gray-300 rounded disabled:opacity-50"
        >
          Redo →
        </button>
      </div>
    </div>
  )
}
```

**Step 3: Create approval UI**
```javascript
// frontend/src/components/ChangeApproval.jsx
export default function ChangeApproval({ 
  oldBlueprint, 
  newBlueprint, 
  command,
  reasoning,
  onApprove, 
  onReject 
}) {
  return (
    <div className="fixed bottom-0 left-0 right-0 bg-white border-t-2 border-blue-500 p-6 shadow-lg">
      <div className="max-w-4xl mx-auto">
        <h4 className="text-lg font-bold mb-2">Proposed Changes</h4>
        <p className="text-gray-600 mb-4">
          <strong>Command:</strong> "{command}"
        </p>
        <p className="text-gray-600 mb-4">
          <strong>Reasoning:</strong> {reasoning}
        </p>
        
        {/* Show diff */}
        <BlueprintDiff 
          oldBlueprint={oldBlueprint}
          newBlueprint={newBlueprint}
        />
        
        {/* Approve/Reject buttons */}
        <div className="flex gap-4 mt-6">
          <button 
            onClick={onApprove}
            className="px-6 py-2 bg-green-600 text-white rounded font-semibold hover:bg-green-700"
          >
            ✓ Approve Changes
          </button>
          <button 
            onClick={onReject}
            className="px-6 py-2 bg-red-600 text-white rounded font-semibold hover:bg-red-700"
          >
            ✗ Reject Changes
          </button>
        </div>
      </div>
    </div>
  )
}
```

**Step 4: Integrate into builder**
```javascript
// frontend/src/components/BuilderWorkspace.jsx
export default function BuilderWorkspace() {
  const [blueprint, setBlueprint] = useState(null)
  const [editHistory, setEditHistory] = useState([])
  const [historyIndex, setHistoryIndex] = useState(-1)
  const [pendingChange, setPendingChange] = useState(null)

  const handleEdit = async (command) => {
    if (!blueprint) return
    
    const response = await fetch('http://127.0.0.1:8000/edit/enhance', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ command, blueprint })
    })
    
    const { modified_blueprint, reasoning } = await response.json()
    
    // Show approval UI
    setPendingChange({
      command,
      reasoning,
      oldBlueprint: blueprint,
      newBlueprint: modified_blueprint
    })
  }

  const handleApprove = () => {
    const newHistory = editHistory.slice(0, historyIndex + 1)
    newHistory.push({
      command: pendingChange.command,
      reasoning: pendingChange.reasoning,
      blueprint: pendingChange.newBlueprint,
      approved: true
    })
    
    setBlueprint(pendingChange.newBlueprint)
    setEditHistory(newHistory)
    setHistoryIndex(newHistory.length - 1)
    setPendingChange(null)
  }

  const handleReject = () => {
    setPendingChange(null)
  }

  const handleUndo = () => {
    if (historyIndex > 0) {
      setHistoryIndex(historyIndex - 1)
      setBlueprint(editHistory[historyIndex - 1].blueprint)
    }
  }

  const handleRedo = () => {
    if (historyIndex < editHistory.length - 1) {
      setHistoryIndex(historyIndex + 1)
      setBlueprint(editHistory[historyIndex + 1].blueprint)
    }
  }

  return (
    <div className="grid grid-cols-3 gap-4">
      {/* Left: Editor panel */}
      <div>
        <BlueprintEditor blueprint={blueprint} />
      </div>
      
      {/* Middle: Canvas */}
      <div>
        <CanvasArea blueprint={blueprint} />
      </div>
      
      {/* Right: History */}
      <div>
        <EditHistory 
          history={editHistory.slice(0, historyIndex + 1)}
          onUndo={handleUndo}
          onRedo={handleRedo}
        />
      </div>
      
      {/* Edit input */}
      {blueprint && (
        <EditCommandInput onEdit={handleEdit} />
      )}
      
      {/* Approval modal */}
      {pendingChange && (
        <ChangeApproval
          {...pendingChange}
          onApprove={handleApprove}
          onReject={handleReject}
        />
      )}
    </div>
  )
}
```

### Files to Create/Modify
- ✅ Create: `frontend/src/components/BlueprintEditor.jsx`
- ✅ Create: `frontend/src/components/EditHistory.jsx`
- ✅ Create: `frontend/src/components/ChangeApproval.jsx`
- ✅ Create: `frontend/src/components/BuilderWorkspace.jsx`
- ✅ Modify: `frontend/src/components/EditCommandInput.jsx` (surface to UI)
- ✅ Modify: `frontend/src/pages/UploadPage.jsx` (integrate workspace)

### Success Criteria
- [ ] Blueprint visible in editor panel (JSON and visual)
- [ ] Edit command input visible and responsive
- [ ] Approval UI shows before/after changes
- [ ] Accept/Reject buttons work
- [ ] Edit history displays all changes
- [ ] Undo/Redo buttons functional
- [ ] Can revert to any previous state

---

## 🔄 Git Workflow & Merge Strategy

### Your Workflow

**Step 1: Create your branch**
```bash
git checkout -b feature/phases-7-8-9
```

**Step 2: Work on all three phases**
```bash
# Phase 7 work
git commit -m "Phase 7: Add React Router, page routing, multi-page navigation"

# Phase 8 work
git commit -m "Phase 8: Dynamic blueprint rendering, visual diff, live preview"

# Phase 9 work
git commit -m "Phase 9: Edit UI, command input, approve/reject, history panel"
```

**Step 3: Push when complete**
```bash
git push origin feature/phases-7-8-9
```

### Main Developer's Merge Strategy

When you're done, the main developer will:

**Step 1: Fetch and review**
```bash
git fetch origin feature/phases-7-8-9
git diff main feature/phases-7-8-9 --stat  # See what changed
```

**Step 2: Test your branch**
```bash
git checkout feature/phases-7-8-9
npm install  # If you added packages
npm run dev  # Test locally
```

**Step 3: Squash merge into main**
```bash
git checkout main
git merge --squash feature/phases-7-8-9
git commit -m "Merge: Phases 7, 8, 9 - Frontend UI complete"
git push origin main
```

### Why Squash Merge?
- ✅ **Clean history:** All your commits become ONE coherent commit
- ✅ **Easy rollback:** If something breaks, they revert one commit
- ✅ **Clear attribution:** One message shows what was delivered
- ✅ **No merge conflicts:** Your branch stays independent

### If Merge Conflicts Occur
```bash
# Main developer resolves by taking your files:
git checkout --theirs frontend/src/*
git add .
git commit -m "Merge: Phases 7, 8, 9 - Frontend UI complete"
```

---

## 📊 Before You Start: Checklist

- [ ] Backend is running: `python run_server.py` (main developer)
- [ ] You can access http://127.0.0.1:8000/health
- [ ] Frontend dev server runs: `npm run dev`
- [ ] You have git access to feature branch
- [ ] You read backend APIs section above
- [ ] You understand all three phases
- [ ] You have React/JavaScript experience

---

## 🆘 Common Issues & Solutions

### Issue: "API returns 404"
```
Solution: Ensure backend is running on port 8000
Check: curl http://127.0.0.1:8000/health
```

### Issue: "Can't import React Router"
```
Solution: Run npm install react-router-dom
Verify: Check package.json has "react-router-dom": "^6.x"
```

### Issue: "Blueprint doesn't render visually"
```
Solution: Check blueprint structure in console
Verify: blueprint.tokens exists
Verify: blueprint.components is array
Debug: Log the blueprint object
```

### Issue: "Edits don't apply"
```
Solution: Check backend response has "modified_blueprint"
Verify: Command string is not empty
Debug: Log the API response
```

---

## 📞 Communication Points

### When You're Ready to Start
"Starting Phase 7, 8, 9 implementation on feature/phases-7-8-9 branch"

### When You Have Questions
Ask about:
- Backend API behavior
- Expected data formats
- Performance requirements
- UI/UX preferences

### When You're Done
"Phases 7, 8, 9 complete - ready for review on feature/phases-7-8-9"

Main developer will then:
1. Review your code
2. Test on their machine
3. Squash merge to main
4. Verify all tests pass

---

## 📚 Reference Documents

**Backend Documentation:**
- Backend API Summary: `BACKEND_SUMMARY_FOR_FRONTEND.md`
- Phase 10.2 Details: `PHASE_10_2_CERTIFICATION.md`
- System Overview: `SYSTEM_LIVE.md`

**Blueprint Schema:**
- See `backend/models/schemas.py`
- Components: navbar, button, product, text, container, etc.
- Tokens: primary_color, accent_color, base_spacing, border_radius, font_scale

**Current Frontend Code:**
- Starting point: `frontend/src/pages/UploadPage.jsx`
- Layout structure: `frontend/src/components/BuilderLayout.jsx`
- Rendering area: `frontend/src/components/CanvasArea.jsx`

---

## ✅ Definition of Done

**Phase 7 Complete When:**
- [ ] React Router v6 installed
- [ ] 4+ routes working
- [ ] Page navigation functional
- [ ] Multiple designs can be stored

**Phase 8 Complete When:**
- [ ] Blueprint renders visually (not JSON)
- [ ] Edit updates preview live
- [ ] Diff viewer shows changes
- [ ] All component types render

**Phase 9 Complete When:**
- [ ] Blueprint editor visible
- [ ] Edit command input works
- [ ] Approval UI shown
- [ ] History tracking works
- [ ] Undo/Redo functional

---

**Good luck! Ask questions, commit frequently, and ship it! 🚀**
