import { useState } from 'react'

export default function EditCommandInput({ blueprint, onBlueprointUpdate, disabled }) {
  const [command, setCommand] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [success, setSuccess] = useState(null)

  const handleApplyEdit = async (e) => {
    e.preventDefault()
    if (!command.trim() || !blueprint) {
      setError('Please enter a command')
      return
    }

    setLoading(true)
    setError(null)
    setSuccess(null)

    try {
      console.log('Applying edit command:', command)
      
      const response = await fetch('http://127.0.0.1:8000/enhance/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          blueprint,
          command,
        }),
      })

      console.log('Edit response status:', response.status)

      if (!response.ok) {
        const errorData = await response.json()
        console.error('Edit error:', errorData)
        setError(errorData.error || `Edit failed: ${response.statusText}`)
        return
      }

      const data = await response.json()
      console.log('Edit successful, patched blueprint:', data.patched_blueprint)
      
      // Update parent with patched blueprint
      onBlueprointUpdate(data.patched_blueprint)
      
      // Show success message
      setSuccess(`Edit applied: ${data.summary || 'Blueprint updated'}`)
      
      // Clear command input
      setCommand('')
      
      // Clear success message after 3 seconds
      setTimeout(() => setSuccess(null), 3000)
    } catch (err) {
      console.error('Edit error:', err)
      setError(`Edit failed: ${err.message}`)
    } finally {
      setLoading(false)
    }
  }

  if (!blueprint) {
    return null
  }

  return (
    <div className="bg-white rounded-lg shadow-md border border-gray-200 p-8 mb-8">
      <h2 className="text-xl font-semibold text-gray-900 mb-6">Step 2: Edit Design</h2>

      <form onSubmit={handleApplyEdit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Design Command
          </label>
          <div className="flex gap-2">
            <textarea
              value={command}
              onChange={(e) => {
                setCommand(e.target.value)
                setError(null)
                setSuccess(null)
              }}
              placeholder="e.g., Make button bigger, Change primary color to #FF5733"
              disabled={disabled || loading}
              className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100 resize-none"
              rows="3"
            />
          </div>
        </div>

        <button
          type="submit"
          disabled={!command.trim() || disabled || loading}
          className="px-6 py-2 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition"
        >
          {loading ? 'Applying...' : 'Apply Edit'}
        </button>
      </form>

      {error && (
        <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
          {error}
        </div>
      )}

      {success && (
        <div className="mt-4 p-4 bg-green-50 border border-green-200 rounded-lg text-green-700 text-sm">
          ✓ {success}
        </div>
      )}

      <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-lg text-sm">
        <p className="font-medium text-gray-900 mb-2">Valid commands:</p>
        <ul className="list-disc list-inside space-y-1 text-gray-700">
          <li>Make button bigger</li>
          <li>Change primary color to #FF5733</li>
          <li>Increase heading size</li>
          <li>Move CTA to bottom</li>
        </ul>
      </div>
    </div>
  )
}
