import React from 'react';
import UploadArea from './UploadArea';

const GeneratedWebsite = () => {
    return (
        <div className="min-h-screen bg-white flex flex-col font-sans text-slate-900">
            {/* Navbar */}
            <header className="fixed top-0 left-0 right-0 h-16 bg-white/80 backdrop-blur-md border-b border-slate-200 z-50">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-full flex items-center justify-between">
                    <div className="flex items-center gap-2">
                        <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
                            <span className="text-white font-bold text-lg">AI</span>
                        </div>
                        <h1 className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-indigo-600">
                            UI Builder
                        </h1>
                    </div>
                    <nav className="hidden md:flex items-center gap-6">
                        <a href="#" className="text-sm font-medium text-slate-600 hover:text-blue-600 transition-colors">Home</a>
                        <a href="#" className="text-sm font-medium text-slate-600 hover:text-blue-600 transition-colors">Store</a>
                        <a href="#" className="text-sm font-medium text-slate-600 hover:text-blue-600 transition-colors">About</a>
                        <div className="flex items-center gap-4 ml-2">
                            <button className="text-sm font-medium text-slate-600 hover:text-blue-600 transition-colors">
                                Login
                            </button>
                            <button className="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 transition-colors shadow-sm">
                                Order Now
                            </button>
                        </div>
                    </nav>
                </div>
            </header>

            {/* Main Content */}
            <main className="flex-1 pt-24 pb-12 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto w-full">
                <div className="grid lg:grid-cols-2 gap-12 lg:gap-24 items-center min-h-[calc(100vh-144px)]">

                    {/* Left Column: Hero Text */}
                    <div className="space-y-8 text-center lg:text-left">
                        <div className="space-y-4">
                            <h2 className="text-4xl sm:text-5xl lg:text-6xl font-extrabold tracking-tight text-slate-900 leading-[1.1]">
                                Design at the <br className="hidden lg:block" />
                                <span className="text-blue-600">Speed of Thought</span>
                            </h2>
                            <p className="text-lg sm:text-xl text-slate-600 leading-relaxed max-w-2xl mx-auto lg:mx-0">
                                Transform your sketches and screenshots into production-ready React code instantly.
                                Build beautiful interfaces without writing a single line of CSS.
                            </p>
                        </div>

                        <div className="flex flex-col sm:flex-row items-center gap-4 justify-center lg:justify-start">
                            <button className="w-full sm:w-auto px-8 py-3.5 text-base font-semibold text-white bg-blue-600 rounded-xl hover:bg-blue-500 shadow-lg shadow-blue-500/20 transition-all hover:-translate-y-0.5">
                                Start Building Free
                            </button>
                            <button className="w-full sm:w-auto px-8 py-3.5 text-base font-medium text-slate-700 bg-white border border-slate-200 rounded-xl hover:bg-slate-50 hover:border-slate-300 transition-all">
                                View Demo
                            </button>
                        </div>

                        <div className="pt-8 border-t border-slate-100 flex items-center justify-center lg:justify-start gap-8 text-slate-500">
                            <div className="flex flex-col">
                                <span className="text-2xl font-bold text-slate-900">10k+</span>
                                <span className="text-sm">Components Generated</span>
                            </div>
                            <div className="flex flex-col">
                                <span className="text-2xl font-bold text-slate-900">100%</span>
                                <span className="text-sm">Customizeable Code</span>
                            </div>
                        </div>
                    </div>

                    {/* Right Column: Upload Area */}
                    <div className="relative w-full max-w-xl mx-auto lg:max-w-none">
                        <div className="absolute -inset-4 bg-gradient-to-r from-blue-100 to-indigo-100 rounded-3xl opacity-50 blur-2xl -z-10" />
                        <div className="bg-white rounded-2xl shadow-xl shadow-slate-200/50 p-6 md:p-8 border border-white/50 backdrop-blur-sm">
                            <div className="flex items-center justify-between mb-6">
                                <div className="flex space-x-2">
                                    <div className="w-3 h-3 rounded-full bg-red-400" />
                                    <div className="w-3 h-3 rounded-full bg-amber-400" />
                                    <div className="w-3 h-3 rounded-full bg-green-400" />
                                </div>
                                <div className="text-xs font-mono text-slate-400">upload_preview.tsx</div>
                            </div>
                            <UploadArea />
                        </div>
                    </div>

                </div>
            </main>
        </div>
    );
};

export default GeneratedWebsite;
