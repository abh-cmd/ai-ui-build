import React from 'react';
import GeneratedWebsite from './GeneratedWebsite';

const CanvasArea = ({ activePageId, blueprint }) => {
    return (
        <div className="flex-1 bg-slate-100 relative overflow-hidden flex flex-col">
            {/* Toolbar / Breadcrumbs placeholder */}
            <div className="h-12 border-b border-slate-200 bg-white flex items-center px-4 justify-between">
                <div className="text-sm text-slate-500">
                    <span className="font-medium text-slate-900">Page</span>
                    <span className="mx-2">/</span>
                    {blueprint?.name || activePageId}
                </div>
                <div className="text-xs font-mono text-slate-400">1280px x 800px</div>
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
                    <GeneratedWebsite />
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
