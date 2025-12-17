import React from 'react';
import { Settings, Palette } from 'lucide-react';

const PropertiesPanel = () => {
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
};

export default PropertiesPanel;
