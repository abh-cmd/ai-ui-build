import React from 'react';
import { Upload } from 'lucide-react';

const UploadArea = () => {
    return (
        <div className="w-full h-full min-h-[400px] border-2 border-dashed border-slate-300 rounded-xl bg-slate-50 hover:bg-slate-100 hover:border-blue-400 transition-all cursor-pointer flex flex-col items-center justify-center group relative overflow-hidden">
            <div className="flex flex-col items-center gap-4 z-10">
                <div className="p-4 bg-white rounded-full shadow-sm group-hover:shadow-md transition-shadow">
                    <Upload className="w-8 h-8 text-slate-400 group-hover:text-blue-500 transition-colors" />
                </div>
                <div className="text-center space-y-2">
                    <p className="text-lg font-medium text-slate-700 group-hover:text-blue-600 transition-colors">
                        Click to upload image
                    </p>
                    <p className="text-sm text-slate-500">
                        or drag and drop here
                    </p>
                </div>
            </div>

            {/* Decorative background pattern */}
            <div className="absolute inset-0 opacity-[0.03] pointer-events-none bg-[radial-gradient(#475569_1px,transparent_1px)] [background-size:16px_16px]" />
        </div>
    );
};

export default UploadArea;
