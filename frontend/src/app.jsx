import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import EditorPage from './pages/EditorPage';

function App() {
    return (
        <BrowserRouter>
            <Routes>
                {/* Default redirect to editor/home */}
                <Route path="/" element={<Navigate to="/editor/home" replace />} />

                {/* Editor Route capturing the pageId */}
                <Route path="/editor/:pageId" element={<EditorPage />} />

                {/* Catch-all redirect */}
                <Route path="*" element={<Navigate to="/editor/home" replace />} />
            </Routes>
        </BrowserRouter>
    );
}

export default App;
