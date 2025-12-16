import { useState } from 'react'
import PreviewPanel from '../components/PreviewPanel'
import EditCommandInput from '../components/EditCommandInput'

export default function UploadPage() {
  const [file, setFile] = useState(null)
  const [blueprint, setBlueprint] = useState(null)
  const [generatedFiles, setGeneratedFiles] = useState(null)
  const [previewHTML, setPreviewHTML] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [activeTab, setActiveTab] = useState('blueprint')

  const handleFileChange = (e) => {
    setFile(e.target.files[0])
    setError(null)
  }

  const handleUpload = async (e) => {
    e.preventDefault()
    if (!file) {
      setError('Please select a file')
      return
    }

    setLoading(true)
    setError(null)
    // Clear previous generated files immediately for new upload
    setGeneratedFiles(null)
    setPreviewHTML(null)

    try {
      const formData = new FormData()
      formData.append('file', file)

      console.log('Uploading file:', file.name, 'to http://127.0.0.1:8000/upload/')
      
      const response = await fetch('http://127.0.0.1:8000/upload/', {
        method: 'POST',
        body: formData,
      })

      console.log('Upload response status:', response.status)

      if (!response.ok) {
        const errorText = await response.text()
        console.error('Upload error response:', errorText)
        throw new Error(`Upload failed: ${response.statusText}`)
      }

      const data = await response.json()
      console.log('Upload successful, blueprint:', data.blueprint)
      setBlueprint(data.blueprint)
      setActiveTab('blueprint')
      
      // Auto-generate code for new blueprint
      await generateCode(data.blueprint)
    } catch (err) {
      console.error('Upload error:', err)
      setError(`Upload failed: ${err.message}`)
    } finally {
      setLoading(false)
    }
  }

  const generateCode = async (blueprintData) => {
    if (!blueprintData) return

    try {
      console.log('Auto-generating code with blueprint:', blueprintData)
      
      const response = await fetch('http://127.0.0.1:8000/generate/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ blueprint: blueprintData }),
      })

      console.log('Generate response status:', response.status)

      if (!response.ok) {
        const errorText = await response.text()
        console.error('Generate error response:', errorText)
        throw new Error(`Generation failed: ${response.statusText}`)
      }

      const data = await response.json()
      console.log('Generation successful, files:', Object.keys(data.files))
      setGeneratedFiles(data.files)
      setActiveTab('generated')
    } catch (err) {
      console.error('Generate error:', err)
      setError(`Generation failed: ${err.message}`)
    }
  }

  const handleGenerate = async () => {
    if (!blueprint) return
    setLoading(true)
    await generateCode(blueprint)
    setLoading(false)
  }

  const handlePreview = async () => {
    if (!generatedFiles) {
      setError('Please generate files first')
      return
    }

    setLoading(true)
    setError(null)

    try {
      // For now, show a friendly message since JSX preview requires a build step
      setPreviewHTML('<div style="padding: 20px; font-family: sans-serif;"><p>Preview not available. JSX requires build step.</p><p>Generated files available in the "Generated Files" tab.</p></div>')
      setActiveTab('preview')
    } catch (err) {
      setError(`Preview failed: ${err.message}`)
    } finally {
      setLoading(false)
    }
  }

  const handleBlueprintUpdate = (patchedBlueprint) => {
    // Update blueprint state with patched version
    setBlueprint(patchedBlueprint)
    // Auto-regenerate code with new blueprint
    generateCode(patchedBlueprint)
  }

  return (
    <div className="w-full h-screen flex flex-col bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200 shadow-sm">
        <div className="max-w-7xl mx-auto px-6 py-6">
          <h1 className="text-3xl font-bold text-gray-900">AI UI Builder</h1>
          <p className="text-gray-600 mt-1">Upload a design sketch to generate storefront code</p>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 overflow-auto">
        <div className="max-w-7xl mx-auto px-6 py-8">
          {/* Upload Section */}
          <div className="bg-white rounded-lg shadow-md border border-gray-200 p-8 mb-8">
            <h2 className="text-xl font-semibold text-gray-900 mb-6">Step 1: Upload Design</h2>

            <form onSubmit={handleUpload} className="space-y-4">
              <div className="flex items-center gap-4">
                <input
                  type="file"
                  accept="image/*"
                  onChange={handleFileChange}
                  className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  disabled={loading}
                />
                <button
                  type="submit"
                  disabled={!file || loading}
                  className="px-6 py-2 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition"
                >
                  {loading ? 'Uploading...' : 'Upload'}
                </button>
              </div>
              {file && (
                <p className="text-sm text-gray-600">Selected: {file.name}</p>
              )}
            </form>

            {error && (
              <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
                {error}
              </div>
            )}
          </div>

          {/* Edit Command Section */}
          {blueprint && (
            <EditCommandInput 
              blueprint={blueprint}
              onBlueprointUpdate={handleBlueprintUpdate}
              disabled={loading}
            />
          )}

          {blueprint && (
            <div className="bg-white rounded-lg shadow-md border border-gray-200 p-8 mb-8">
              <h2 className="text-xl font-semibold text-gray-900 mb-6">Step 3: Generate & Preview</h2>
              <div className="flex gap-4">
                <button
                  onClick={handleGenerate}
                  disabled={loading}
                  className="px-6 py-2 bg-green-600 text-white font-medium rounded-lg hover:bg-green-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition"
                >
                  {loading ? 'Generating...' : 'Generate React Files'}
                </button>
                {generatedFiles && (
                  <button
                    onClick={handlePreview}
                    disabled={loading}
                    className="px-6 py-2 bg-purple-600 text-white font-medium rounded-lg hover:bg-purple-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition"
                  >
                    {loading ? 'Loading...' : 'Preview Design'}
                  </button>
                )}
              </div>
            </div>
          )}

          {/* Results Section */}
          {(blueprint || generatedFiles || previewHTML) && (
            <div className="bg-white rounded-lg shadow-md border border-gray-200 overflow-hidden">
              {/* Tabs */}
              <div className="border-b border-gray-200 flex">
                {blueprint && (
                  <button
                    onClick={() => setActiveTab('blueprint')}
                    className={`px-6 py-3 font-medium border-b-2 transition ${
                      activeTab === 'blueprint'
                        ? 'border-blue-600 text-blue-600'
                        : 'border-transparent text-gray-600 hover:text-gray-900'
                    }`}
                  >
                    Blueprint
                  </button>
                )}
                {generatedFiles && (
                  <button
                    onClick={() => setActiveTab('generated')}
                    className={`px-6 py-3 font-medium border-b-2 transition ${
                      activeTab === 'generated'
                        ? 'border-blue-600 text-blue-600'
                        : 'border-transparent text-gray-600 hover:text-gray-900'
                    }`}
                  >
                    Generated Files
                  </button>
                )}
                {previewHTML && (
                  <button
                    onClick={() => setActiveTab('preview')}
                    className={`px-6 py-3 font-medium border-b-2 transition ${
                      activeTab === 'preview'
                        ? 'border-blue-600 text-blue-600'
                        : 'border-transparent text-gray-600 hover:text-gray-900'
                    }`}
                  >
                    Preview
                  </button>
                )}
              </div>

              {/* Content */}
              <div className="p-6">
                {activeTab === 'blueprint' && blueprint && (
                  <PreviewPanel json={blueprint} />
                )}

                {activeTab === 'generated' && generatedFiles && (
                  <div className="space-y-6">
                    {Object.entries(generatedFiles).map(([filename, content]) => (
                      <div key={filename}>
                        <h3 className="font-mono text-sm font-semibold text-gray-900 mb-2">
                          {filename}
                        </h3>
                        <pre className="bg-gray-900 text-gray-100 p-4 rounded-lg overflow-auto max-h-96 text-xs">
                          {content}
                        </pre>
                      </div>
                    ))}
                  </div>
                )}

                {activeTab === 'preview' && previewHTML && (
                  <div className="border border-gray-200 rounded-lg overflow-hidden">
                    <iframe
                      className="w-full"
                      style={{ height: '600px' }}
                      srcDoc={previewHTML}
                      title="Design Preview"
                    />
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
