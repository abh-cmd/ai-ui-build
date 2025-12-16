import { useState } from "react";
import axios from "axios";

export default function App() {
  const [file, setFile] = useState(null);
  const [blueprint, setBlueprint] = useState(null);
  const [command, setCommand] = useState("");
  const [code, setCode] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  async function uploadDesign() {
    if (!file) {
      setError("Please select a file");
      return;
    }
    try {
      setLoading(true);
      setError(null);
      const formData = new FormData();
      formData.append("file", file);
      const res = await axios.post(
        "http://127.0.0.1:8000/upload",
        formData
      );
      setBlueprint(res.data.blueprint);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  async function applyEdit() {
    if (!blueprint || !command) {
      setError("Please enter a command and have a blueprint");
      return;
    }
    try {
      setLoading(true);
      setError(null);
      const res = await axios.post(
        "http://127.0.0.1:8000/enhance",
        { blueprint, command }
      );
      setBlueprint(res.data.patched_blueprint);
      setCommand("");
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  async function generateCode() {
    if (!blueprint) {
      setError("Please upload a design first");
      return;
    }
    try {
      setLoading(true);
      setError(null);
      const res = await axios.post(
        "http://127.0.0.1:8000/generate",
        { blueprint }
      );
      setCode(res.data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={{ padding: "20px", fontFamily: "sans-serif", maxWidth: "1200px", margin: "0 auto" }}>
      <h1>🎨 AI UI Builder</h1>
      <p>Upload a design, edit with natural language, generate React code</p>

      {error && <div style={{ color: "red", padding: "10px", background: "#ffe6e6", borderRadius: "4px", marginBottom: "10px" }}>{error}</div>}

      <section style={{ border: "1px solid #ddd", padding: "15px", marginBottom: "20px", borderRadius: "4px" }}>
        <h3>Step 1: Upload Design</h3>
        <input 
          type="file" 
          onChange={e => setFile(e.target.files[0])}
          accept="image/*"
        />
        <button onClick={uploadDesign} disabled={loading} style={{ marginLeft: "10px", padding: "8px 16px", cursor: loading ? "not-allowed" : "pointer" }}>
          {loading ? "Uploading..." : "Upload Design"}
        </button>
      </section>

      <section style={{ border: "1px solid #ddd", padding: "15px", marginBottom: "20px", borderRadius: "4px" }}>
        <h3>Step 2: Edit with Natural Language</h3>
        <textarea
          placeholder="e.g., 'Make the CTA button larger' or 'Change colors to blue'"
          value={command}
          onChange={e => setCommand(e.target.value)}
          style={{ width: "100%", height: "60px", padding: "8px", borderRadius: "4px", border: "1px solid #ccc" }}
        />
        <button onClick={applyEdit} disabled={loading || !blueprint} style={{ marginTop: "10px", padding: "8px 16px", cursor: (loading || !blueprint) ? "not-allowed" : "pointer" }}>
          {loading ? "Applying..." : "Apply Edit"}
        </button>
      </section>

      <section style={{ border: "1px solid #ddd", padding: "15px", marginBottom: "20px", borderRadius: "4px" }}>
        <h3>Step 3: Generate React Code</h3>
        <button onClick={generateCode} disabled={loading || !blueprint} style={{ padding: "8px 16px", cursor: (loading || !blueprint) ? "not-allowed" : "pointer" }}>
          {loading ? "Generating..." : "Generate Code"}
        </button>
      </section>

      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "20px" }}>
        <section style={{ border: "1px solid #ddd", padding: "15px", borderRadius: "4px" }}>
          <h3>Blueprint JSON</h3>
          <pre style={{ background: "#f5f5f5", padding: "10px", borderRadius: "4px", overflowX: "auto", fontSize: "12px" }}>
            {blueprint ? JSON.stringify(blueprint, null, 2) : "No blueprint yet"}
          </pre>
        </section>

        <section style={{ border: "1px solid #ddd", padding: "15px", borderRadius: "4px" }}>
          <h3>Generated Code</h3>
          <pre style={{ background: "#f5f5f5", padding: "10px", borderRadius: "4px", overflowX: "auto", fontSize: "12px" }}>
            {code ? JSON.stringify(code, null, 2) : "No code yet"}
          </pre>
        </section>
      </div>
    </div>
  );
}
