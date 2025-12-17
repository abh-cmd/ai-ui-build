import React, { useState, useEffect } from 'react';
import { useParams, Navigate } from 'react-router-dom';
import BuilderLayout from '../components/BuilderLayout';
import { getPageState } from '../state/pagesState';

const EditorPage = () => {
    const { pageId } = useParams();
    const [pageState, setPageState] = useState(null);
    const [isLoading, setIsLoading] = useState(true);

    // Effect to load the correct page state when the URL changes
    useEffect(() => {
        setIsLoading(true);
        const state = getPageState(pageId);
        setPageState(state);
        setIsLoading(false);
    }, [pageId]);

    // If invalid page, redirect to home
    if (!isLoading && !pageState) {
        return <Navigate to="/editor/home" replace />;
    }

    if (isLoading) {
        return <div className="h-screen w-full flex items-center justify-center bg-slate-50">Loading...</div>;
    }

    // Pass the specific page data down to the layout
    // The Layout and its children will be "dumb" consumers of this data
    return (
        <BuilderLayout
            key={pageId} // Force re-mount on page change to ensure deep state reset if needed
            activePageId={pageId}
            blueprint={pageState.blueprint}
        // Future: pass setters for mutation here
        />
    );
};

export default EditorPage;
