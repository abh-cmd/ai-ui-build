import React, { useRef } from 'react';
import { Upload, Zap, Code, Download, ToggleRight } from 'lucide-react';

const BuilderSidebar = ({
    blueprint,
    setBlueprint,
    setGeneratedFiles,
    loading,
    setLoading,
    error,
    setError,
}) => {
    const fileInputRef = useRef(null);

    const handleUpload = async (event) => {
        const file = event.target.files?.[0];
        if (!file) return;

        setLoading(true);
        setError(null);

        try {
            const formData = new FormData();
            formData.append('file', file);

            const response = await fetch('http://127.0.0.1:8000/upload/', {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                throw new Error(`Upload failed: ${response.status}`);
            }

            const data = await response.json();
            console.log('Full response from /upload/:', data);
            console.log('Blueprint data:', data.blueprint);
            
            if (data.blueprint) {
                setBlueprint(data.blueprint);
                setGeneratedFiles(null); // Clear previous generated files
                console.log('Blueprint set successfully:', data.blueprint);
            } else {
                console.warn('No blueprint in response. Response keys:', Object.keys(data));
                setError('No blueprint returned from server');
            }
        } catch (err) {
            setError(err.message);
            console.error('Upload error:', err);
        } finally {
            setLoading(false);
        }
    };

    const handleGenerateCode = async () => {
        if (!blueprint) {
            setError('Please upload a design first');
            return;
        }

        setLoading(true);
        setError(null);

        try {
            const response = await fetch('http://127.0.0.1:8000/generate/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ blueprint }),
            });

            if (!response.ok) {
                throw new Error(`Generate failed: ${response.status}`);
            }

            const data = await response.json();
            setGeneratedFiles(data.files);
            console.log('Generated files:', data.files);
        } catch (err) {
            setError(err.message);
            console.error('Generate error:', err);
        } finally {
            setLoading(false);
        }
    };

    const handleDownloadReact = () => {
        if (!blueprint) {
            setError('Please upload a design first');
            return;
        }
        alert('Download React feature coming in Phase 7-9 frontend update');
    };

    const handleAutocorrect = () => {
        if (!blueprint) {
            setError('Please upload a design first');
            return;
        }
        alert('Autocorrect feature coming in Phase 7-9 frontend update');
    };

    return (
        <aside className="w-72 bg-white border-r border-slate-200 flex flex-col h-full bg-slate-50/50">
            {/* Header */}
            <div className="p-4 border-b border-slate-200 bg-white">
                <div className="flex items-center gap-2">
                    <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
                        <span className="text-white font-bold text-lg">AI</span>
                    </div>
                    <h1 className="text-lg font-bold text-slate-900">Builder</h1>
                </div>
            </div>

            <div className="flex-1 overflow-y-auto p-4 space-y-8">
                {/* Status Messages */}
                {error && (
                    <div className="p-3 bg-red-50 border border-red-200 rounded-lg">
                        <p className="text-sm text-red-700">{error}</p>
                    </div>
                )}

                {blueprint && (
                    <div className="p-3 bg-green-50 border border-green-200 rounded-lg">
                        <p className="text-sm text-green-700 font-medium">✓ Design Uploaded</p>
                        <p className="text-xs text-green-600 mt-1">
                            {blueprint.components?.length || 0} components detected
                        </p>
                    </div>
                )}

                {/* Upload Section */}
                <section>
                    <h3 className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-4">
                        Upload UI Sketch
                    </h3>
                    <input
                        ref={fileInputRef}
                        type="file"
                        accept="image/*"
                        onChange={handleUpload}
                        style={{ display: 'none' }}
                    />
                    <div
                        onClick={() => fileInputRef.current?.click()}
                        className="border-2 border-dashed border-slate-300 rounded-xl p-6 text-center hover:bg-slate-50 transition-colors cursor-pointer bg-white group"
                    >
                        <Upload className="w-8 h-8 text-slate-400 mx-auto mb-2 group-hover:text-blue-500 transition-colors" />
                        <span className="text-sm font-medium text-slate-600 group-hover:text-blue-600">
                            {loading ? 'Uploading...' : 'Choose File'}
                        </span>
                        <p className="text-xs text-slate-500 mt-1">PNG or JPG</p>
                    </div>
                </section>

                {/* Actions Section */}
                <section>
                    <h3 className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-4">
                        Actions
                    </h3>
                    <div className="space-y-2">
                        <button
                            onClick={handleAutocorrect}
                            disabled={loading || !blueprint}
                            className="w-full flex items-center gap-3 px-4 py-2.5 text-sm font-medium text-slate-700 bg-white border border-slate-200 rounded-lg hover:bg-slate-50 hover:border-slate-300 transition-all text-left disabled:opacity-50 disabled:cursor-not-allowed"
                        >
                            <Zap className="w-4 h-4 text-amber-500" />
                            Autocorrect UX
                        </button>
                        <button
                            onClick={handleGenerateCode}
                            disabled={loading || !blueprint}
                            className="w-full flex items-center gap-3 px-4 py-2.5 text-sm font-medium text-slate-700 bg-white border border-slate-200 rounded-lg hover:bg-slate-50 hover:border-slate-300 transition-all text-left disabled:opacity-50 disabled:cursor-not-allowed"
                        >
                            <Code className="w-4 h-4 text-blue-500" />
                            {loading ? 'Generating...' : 'Generate Code'}
                        </button>
                        <button
                            onClick={handleDownloadReact}
                            disabled={loading || !blueprint}
                            className="w-full flex items-center gap-3 px-4 py-2.5 text-sm font-medium text-slate-700 bg-white border border-slate-200 rounded-lg hover:bg-slate-50 hover:border-slate-300 transition-all text-left disabled:opacity-50 disabled:cursor-not-allowed"
                        >
                            <Download className="w-4 h-4 text-green-500" />
                            Download React
                        </button>
                    </div>
                </section>

                {/* Modes Section */}
                <section>
                    <h3 className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-4">
                        Modes
                    </h3>
                    <div className="flex items-center justify-between p-3 bg-white border border-slate-200 rounded-lg">
                        <span className="text-sm font-medium text-slate-700">Mock Mode</span>
                        <ToggleRight className="w-6 h-6 text-blue-500 cursor-pointer" />
                    </div>
                </section>
            </div>

            {/* User/Footer */}
            <div className="p-4 border-t border-slate-200 bg-white">
                <div className="flex items-center gap-3">
                    <div className="w-8 h-8 rounded-full bg-slate-200" />
                    <div className="text-sm">
                        <p className="font-medium text-slate-900">User</p>
                        <p className="text-xs text-slate-500">Free Plan</p>
                    </div>
                </div>
            </div>
        </aside>
    );
};

export default BuilderSidebar;
