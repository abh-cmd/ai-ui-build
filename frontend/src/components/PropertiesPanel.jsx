import React, { useState } from 'react';
import { Settings, Palette, Code2, Copy, Check } from 'lucide-react';

const PropertiesPanel = ({ generatedFiles }) => {
    const [copied, setCopied] = useState(null);
    const [selectedFile, setSelectedFile] = useState(null);

    const copyToClipboard = (content, fileName) => {
        navigator.clipboard.writeText(content);
        setCopied(fileName);
        setTimeout(() => setCopied(null), 2000);
    };

    if (!generatedFiles) {
        return (
            <aside className="w-80 bg-white border-l border-slate-200 flex flex-col h-full">
                {/* Tabs */}
                <div className="flex border-b border-slate-200">
                    <button className="flex-1 py-3 text-sm font-medium text-blue-600 border-b-2 border-blue-600 flex items-center justify-center gap-2">
                        <Settings className="w-4 h-4" />
                        Properties
                    </button>
                    <button className="flex-1 py-3 text-sm font-medium text-slate-500 hover:text-slate-700 flex items-center justify-center gap-2">
                        <Palette className="w-4 h-4" />
                        Theme
                    </button>
                </div>

                {/* Empty State */}
                <div className="flex-1 flex flex-col items-center justify-center p-8 text-center bg-slate-50/50">
                    <div className="w-16 h-16 bg-slate-100 rounded-full flex items-center justify-center mb-4">
                        <Settings className="w-8 h-8 text-slate-300" />
                    </div>
                    <h3 className="text-slate-900 font-medium mb-1">No element selected</h3>
                    <p className="text-sm text-slate-500 max-w-[200px]">
                        Click on any element in the canvas to edit its properties
                    </p>
                </div>
            </aside>
        );
    }

    const fileNames = Object.keys(generatedFiles);
    const currentFile = selectedFile || fileNames[0];
    const currentContent = generatedFiles[currentFile] || '';

    return (
        <aside className="w-80 bg-white border-l border-slate-200 flex flex-col h-full">
            {/* Tabs */}
            <div className="flex border-b border-slate-200">
                <button className="flex-1 py-3 text-sm font-medium text-blue-600 border-b-2 border-blue-600 flex items-center justify-center gap-2">
                    <Code2 className="w-4 h-4" />
                    Generated Code
                </button>
            </div>

            {/* File List */}
            <div className="p-3 border-b border-slate-200 bg-slate-50 max-h-[120px] overflow-y-auto">
                <div className="space-y-1">
                    {fileNames.map((fileName) => (
                        <button
                            key={fileName}
                            onClick={() => setSelectedFile(fileName)}
                            className={`w-full text-left px-3 py-2 rounded text-sm font-mono transition-colors ${
                                currentFile === fileName
                                    ? 'bg-blue-100 text-blue-900'
                                    : 'bg-white text-slate-700 hover:bg-slate-100'
                            }`}
                        >
                            {fileName}
                        </button>
                    ))}
                </div>
            </div>

            {/* Code Content */}
            <div className="flex-1 overflow-hidden flex flex-col">
                {/* Copy Button */}
                <div className="p-3 border-b border-slate-200 flex justify-end">
                    <button
                        onClick={() => copyToClipboard(currentContent, currentFile)}
                        className="flex items-center gap-1 px-3 py-1 text-xs font-medium bg-blue-50 text-blue-600 rounded hover:bg-blue-100 transition-colors"
                    >
                        {copied === currentFile ? (
                            <>
                                <Check className="w-3 h-3" />
                                Copied!
                            </>
                        ) : (
                            <>
                                <Copy className="w-3 h-3" />
                                Copy
                            </>
                        )}
                    </button>
                </div>

                {/* Code Viewer */}
                <div className="flex-1 overflow-auto p-4 bg-slate-950 text-slate-50 font-mono text-xs leading-relaxed">
                    <pre>{currentContent}</pre>
                </div>
            </div>
        </aside>
    );
};

export default PropertiesPanel;
