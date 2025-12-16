import React from 'react';
import BuilderSidebar from './BuilderSidebar';
import CanvasArea from './CanvasArea';
import PropertiesPanel from './PropertiesPanel';

const BuilderLayout = () => {
    return (
        <div className="flex h-screen w-full overflow-hidden bg-white">
            <BuilderSidebar />
            <CanvasArea />
            <PropertiesPanel />
        </div>
    );
};

export default BuilderLayout;
