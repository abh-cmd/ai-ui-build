import React, { useState } from 'react';
import GeneratedWebsite from './GeneratedWebsite';

const CanvasArea = ({ generatedFiles, blueprint }) => {
    const [viewMode, setViewMode] = useState('preview'); // 'preview' or 'json'

    return (
        <div className="flex-1 bg-slate-100 relative overflow-hidden flex flex-col">
            {/* Toolbar / Breadcrumbs placeholder */}
            <div className="h-12 border-b border-slate-200 bg-white flex items-center px-4 justify-between">
                <div className="text-sm text-slate-500">
                    <span className="font-medium text-slate-900">Page</span>
                    <span className="mx-2">/</span>
                    Home
                </div>
                <div className="flex items-center gap-4">
                    {blueprint && (
                        <div className="flex gap-2">
                            <button
                                onClick={() => setViewMode('preview')}
                                className={`px-2 py-1 text-xs font-medium rounded ${
                                    viewMode === 'preview'
                                        ? 'bg-blue-100 text-blue-700'
                                        : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                                }`}
                            >
                                Preview
                            </button>
                            <button
                                onClick={() => setViewMode('json')}
                                className={`px-2 py-1 text-xs font-medium rounded ${
                                    viewMode === 'json'
                                        ? 'bg-blue-100 text-blue-700'
                                        : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                                }`}
                            >
                                JSON
                            </button>
                        </div>
                    )}
                    <div className="text-xs font-mono text-slate-400">
                        {generatedFiles ? '✓ Generated' : blueprint ? '✓ Blueprint Ready' : '1280px x 800px'}
                    </div>
                </div>
            </div>

            {/* Canvas */}
            <div className="flex-1 overflow-auto p-8 flex items-center justify-center">
                {/* Dotted Background */}
                <div className="absolute inset-0 opacity-[0.4] pointer-events-none"
                    style={{
                        backgroundImage: 'radial-gradient(#cbd5e1 1px, transparent 1px)',
                        backgroundSize: '24px 24px'
                    }}
                />

                {/* Preview Frame */}
                <div className="bg-white shadow-2xl rounded-lg overflow-hidden w-full max-w-6xl aspect-[16/9] ring-1 ring-slate-900/5 transform transition-transform duration-200 origin-center scale-[0.9]">
                    {generatedFiles ? (
                        <div className="w-full h-full flex items-center justify-center bg-gradient-to-br from-green-50 to-blue-50">
                            <div className="text-center">
                                <div className="inline-flex items-center justify-center w-16 h-16 bg-green-100 rounded-full mb-4">
                                    <span className="text-2xl">✓</span>
                                </div>
                                <h2 className="text-xl font-bold text-slate-900 mb-2">Code Generated!</h2>
                                <p className="text-slate-600 mb-4">Check the right panel for generated React files</p>
                                <div className="space-y-1 text-sm text-slate-600">
                                    {Object.keys(generatedFiles).map((file) => (
                                        <div key={file} className="flex items-center justify-center gap-2">
                                            <span className="text-green-600 font-semibold">→</span>
                                            {file}
                                        </div>
                                    ))}
                                </div>
                            </div>
                        </div>
                    ) : blueprint ? (
                        viewMode === 'json' ? (
                            <div className="w-full h-full overflow-auto p-6 bg-slate-950">
                                <pre className="text-slate-50 font-mono text-xs whitespace-pre-wrap break-words">
                                    {JSON.stringify(blueprint, null, 2)}
                                </pre>
                            </div>
                        ) : (
                            <div className="w-full h-full overflow-auto p-6 bg-slate-50">
                                <div className="max-w-2xl mx-auto">
                                    <h2 className="text-lg font-bold text-slate-900 mb-4">Blueprint Preview</h2>
                                    
                                    {/* Design Tokens */}
                                    {blueprint.tokens && (
                                        <div className="mb-6 p-4 bg-white rounded-lg border border-slate-200">
                                            <h3 className="font-semibold text-slate-900 mb-3">Design Tokens</h3>
                                            <div className="grid grid-cols-2 gap-3 text-sm">
                                                {blueprint.tokens.primary_color && (
                                                    <div className="flex items-center gap-2">
                                                        <div 
                                                            className="w-6 h-6 rounded border border-slate-300" 
                                                            style={{ backgroundColor: blueprint.tokens.primary_color }}
                                                        />
                                                        <span className="text-slate-600">Primary: {blueprint.tokens.primary_color}</span>
                                                    </div>
                                                )}
                                                {blueprint.tokens.accent_color && (
                                                    <div className="flex items-center gap-2">
                                                        <div 
                                                            className="w-6 h-6 rounded border border-slate-300" 
                                                            style={{ backgroundColor: blueprint.tokens.accent_color }}
                                                        />
                                                        <span className="text-slate-600">Accent: {blueprint.tokens.accent_color}</span>
                                                    </div>
                                                )}
                                                {blueprint.tokens.base_spacing && (
                                                    <div className="text-slate-600">Spacing: {blueprint.tokens.base_spacing}px</div>
                                                )}
                                                {blueprint.tokens.border_radius && (
                                                    <div className="text-slate-600">Radius: {blueprint.tokens.border_radius}px</div>
                                                )}
                                            </div>
                                        </div>
                                    )}

                                    {/* Components */}
                                    {blueprint.components && blueprint.components.length > 0 && (
                                        <div className="p-4 bg-white rounded-lg border border-slate-200">
                                            <h3 className="font-semibold text-slate-900 mb-3">
                                                Components ({blueprint.components.length})
                                            </h3>
                                            <div className="space-y-2 text-sm">
                                                {blueprint.components.map((comp, idx) => (
                                                    <div key={idx} className="flex items-center justify-between p-2 bg-slate-50 rounded">
                                                        <div>
                                                            <span className="font-mono text-blue-600">{comp.type}</span>
                                                            {comp.text && <span className="text-slate-600 ml-2">"{comp.text}"</span>}
                                                        </div>
                                                        {comp.bbox && (
                                                            <span className="text-xs text-slate-500 font-mono">
                                                                {comp.bbox.width}×{comp.bbox.height}
                                                            </span>
                                                        )}
                                                    </div>
                                                ))}
                                            </div>
                                        </div>
                                    )}
                                </div>
                            </div>
                        )
                    ) : (
                        <GeneratedWebsite />
                    )}
                </div>
            </div>

            {/* Zoom Indicator */}
            <div className="absolute bottom-4 right-4 bg-white border border-slate-200 px-3 py-1.5 rounded-lg shadow-sm text-xs font-medium text-slate-600">
                100%
            </div>
        </div>
    );
};

export default CanvasArea;
