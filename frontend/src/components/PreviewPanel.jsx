export default function PreviewPanel({ json }) {
  return (
    <div className="bg-gray-900 rounded-lg overflow-hidden">
      <pre className="text-gray-100 p-6 overflow-auto max-h-96 text-xs font-mono">
        {JSON.stringify(json, null, 2)}
      </pre>
    </div>
  )
}
