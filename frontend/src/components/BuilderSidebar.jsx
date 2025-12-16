import React from 'react';
import { Upload, Zap, Code, Download, ToggleRight } from 'lucide-react';

const BuilderSidebar = () => {
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
                {/* Upload Section */}
                <section>
                    <h3 className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-4">
                        Upload UI Sketch
                    </h3>
                    <div className="border-2 border-dashed border-slate-300 rounded-xl p-6 text-center hover:bg-slate-50 transition-colors cursor-pointer bg-white group">
                        <Upload className="w-8 h-8 text-slate-400 mx-auto mb-2 group-hover:text-blue-500 transition-colors" />
                        <span className="text-sm font-medium text-slate-600 group-hover:text-blue-600">
                            Choose File
                        </span>
                    </div>
                </section>

                {/* Actions Section */}
                <section>
                    <h3 className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-4">
                        Actions
                    </h3>
                    <div className="space-y-2">
                        <button className="w-full flex items-center gap-3 px-4 py-2.5 text-sm font-medium text-slate-700 bg-white border border-slate-200 rounded-lg hover:bg-slate-50 hover:border-slate-300 transition-all text-left">
                            <Zap className="w-4 h-4 text-amber-500" />
                            Autocorrect UX
                        </button>
                        <button className="w-full flex items-center gap-3 px-4 py-2.5 text-sm font-medium text-slate-700 bg-white border border-slate-200 rounded-lg hover:bg-slate-50 hover:border-slate-300 transition-all text-left">
                            <Code className="w-4 h-4 text-blue-500" />
                            Generate Code
                        </button>
                        <button className="w-full flex items-center gap-3 px-4 py-2.5 text-sm font-medium text-slate-700 bg-white border border-slate-200 rounded-lg hover:bg-slate-50 hover:border-slate-300 transition-all text-left">
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
