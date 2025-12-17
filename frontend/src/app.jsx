import React, { useState } from 'react';
import BuilderLayout from './components/BuilderLayout';

function App() {
    const [blueprint, setBlueprint] = useState(null);
    const [generatedFiles, setGeneratedFiles] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    return (
        <BuilderLayout 
            blueprint={blueprint}
            setBlueprint={setBlueprint}
            generatedFiles={generatedFiles}
            setGeneratedFiles={setGeneratedFiles}
            loading={loading}
            setLoading={setLoading}
            error={error}
            setError={setError}
        />
    );
}

export default App;
