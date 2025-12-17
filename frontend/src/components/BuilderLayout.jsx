import React from 'react';
import BuilderSidebar from './BuilderSidebar';
import CanvasArea from './CanvasArea';
import PropertiesPanel from './PropertiesPanel';

const BuilderLayout = ({
    blueprint,
    setBlueprint,
    generatedFiles,
    setGeneratedFiles,
    loading,
    setLoading,
    error,
    setError,
}) => {
    return (
        <div className="flex h-screen w-full overflow-hidden bg-white">
            <BuilderSidebar 
                blueprint={blueprint}
                setBlueprint={setBlueprint}
                setGeneratedFiles={setGeneratedFiles}
                loading={loading}
                setLoading={setLoading}
                error={error}
                setError={setError}
            />
            <CanvasArea blueprint={blueprint} generatedFiles={generatedFiles} />
            <PropertiesPanel generatedFiles={generatedFiles} />
        </div>
    );
};

export default BuilderLayout;
