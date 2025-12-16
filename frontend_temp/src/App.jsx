import React, { useState } from 'react'
import axios from 'axios'
import './App.css'

export default function App() {
  const [blueprint, setBlueprint] = useState(null)
  const [generatedCode, setGeneratedCode] = useState(null)
  const [editCommand, setEditCommand] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const [editSummary, setEditSummary] = useState('')

  const API_BASE = 'http://127.0.0.1:8000'

  // 1. UPLOAD IMAGE
  const handleUpload = async (event) => {
    const file = event.target.files?.[0]
    if (!file) return

    setLoading(true)
    setError('')
    setGeneratedCode(null)
    setEditSummary('')

    try {
      const formData = new FormData()
      formData.append('file', file)

      const response = await axios.post(`${API_BASE}/upload`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })

      setBlueprint(response.data.blueprint)
      console.log('✓ Blueprint received from /upload')
    } catch (err) {
      const msg = err.response?.data?.detail || err.message
      setError(`Upload failed: ${msg}`)
      console.error('✗ Upload error:', msg)
    } finally {
      setLoading(false)
    }
  }

  // 2. GENERATE CODE
  const handleGenerate = async () => {
    if (!blueprint) {
      setError('No blueprint loaded. Upload an image first.')
      return
    }

    setLoading(true)
    setError('')

    try {
      const response = await axios.post(`${API_BASE}/generate`, {
        blueprint: blueprint
      })

      console.log('✓ Raw response from /generate:', response.data)
      
      // Handle different response formats
      let files = []
      
      if (Array.isArray(response.data.files)) {
        // Format: { files: [{filename, content}, ...] }
        files = response.data.files
      } else if (typeof response.data.files === 'object' && response.data.files !== null) {
        // Format: { files: {filename: content, filename: content} } <- Backend returns this
        files = Object.entries(response.data.files).map(([filename, content]) => ({
          filename,
          content
        }))
      } else if (Array.isArray(response.data)) {
        // Format: [{filename, content}, ...]
        files = response.data
      } else if (response.data.code) {
        // Format: { code: "..." }
        files = [{ filename: 'generated.jsx', content: response.data.code }]
      } else {
        // Fallback: show entire response
        console.warn('Unexpected response format:', response.data)
        files = [{ filename: 'response.json', content: JSON.stringify(response.data, null, 2) }]
      }

      setGeneratedCode(files)
      console.log('✓ Code generated from /generate, files count:', files.length)
    } catch (err) {
      console.error('✗ Full error object:', err)
      const msg = err.response?.data?.detail || err.response?.data?.message || err.message
      const fullError = err.response?.data ? JSON.stringify(err.response.data, null, 2) : msg
      setError(`Generation failed: ${msg}\n\nDetails: ${fullError}`)
      console.error('✗ Generate error details:', fullError)
    } finally {
      setLoading(false)
    }
  }

  // 3. EDIT BLUEPRINT WITH COMMAND
  const handleEditCommand = async () => {
    if (!blueprint) {
      setError('No blueprint loaded. Upload an image first.')
      return
    }

    if (!editCommand.trim()) {
      setError('Enter a command to edit.')
      return
    }

    setLoading(true)
    setError('')
    setEditSummary('')

    try {
      const response = await axios.post(`${API_BASE}/enhance`, {
        blueprint: blueprint,
        command: editCommand
      })

      setBlueprint(response.data.patched_blueprint)
      setEditSummary(response.data.summary || 'Edit applied successfully')
      setEditCommand('')
      setGeneratedCode(null) // Clear old code, user should regenerate
      console.log('✓ Blueprint edited via /enhance')
    } catch (err) {
      const msg = err.response?.data?.detail || err.message
      setError(`Edit failed: ${msg}`)
      console.error('✗ Enhance error:', msg)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app-container">
      {/* LEFT PANEL: UPLOAD & EDIT */}
      <div className="panel left-panel">
        <h2>📤 Upload Image</h2>
        <input
          type="file"
          accept="image/*"
          onChange={handleUpload}
          disabled={loading}
          className="file-input"
        />

        <h2 style={{ marginTop: '2rem' }}>✏️ Edit Blueprint</h2>
        <textarea
          placeholder="Enter natural language command (e.g., 'Change background to blue', 'Add a new button below the header')"
          value={editCommand}
          onChange={(e) => setEditCommand(e.target.value)}
          disabled={!blueprint || loading}
          className="edit-textarea"
        />
        <button
          onClick={handleEditCommand}
          disabled={!blueprint || !editCommand.trim() || loading}
          className="btn btn-edit"
        >
          {loading ? 'Processing...' : 'Apply Edit'}
        </button>

        {editSummary && (
          <div className="success-box">
            <strong>Edit Summary:</strong>
            <p>{editSummary}</p>
          </div>
        )}

        {blueprint && (
          <button
            onClick={handleGenerate}
            disabled={loading}
            className="btn btn-generate"
            style={{ marginTop: '1rem' }}
          >
            {loading ? 'Generating...' : '⚡ Generate Code'}
          </button>
        )}
      </div>

      {/* MIDDLE PANEL: BLUEPRINT JSON */}
      <div className="panel middle-panel">
        <h2>📋 Blueprint JSON</h2>
        {blueprint ? (
          <pre className="json-viewer">{JSON.stringify(blueprint, null, 2)}</pre>
        ) : (
          <div className="placeholder">Upload an image to see blueprint</div>
        )}
      </div>

      {/* RIGHT PANEL: GENERATED CODE */}
      <div className="panel right-panel">
        <h2>💻 Generated Code</h2>
        {generatedCode ? (
          <div className="code-list">
            {generatedCode.map((file, idx) => (
              <div key={idx} className="code-file">
                <div className="file-header">{file.filename}</div>
                <pre className="code-viewer">{file.content}</pre>
              </div>
            ))}
          </div>
        ) : (
          <div className="placeholder">Click "Generate Code" to see output</div>
        )}
      </div>

      {/* ERROR BOX */}
      {error && (
        <div className="error-box">
          <strong>Error:</strong> {error}
        </div>
      )}

      {/* LOADING OVERLAY */}
      {loading && (
        <div className="loading-overlay">
          <div className="spinner"></div>
          <p>Processing...</p>
        </div>
      )}
    </div>
  )
}
