import React from 'react';
import BuilderSidebar from './BuilderSidebar';
import CanvasArea from './CanvasArea';
import PropertiesPanel from './PropertiesPanel';

const BuilderLayout = ({ activePageId, blueprint }) => {
    return (
        <div className="flex h-screen w-full overflow-hidden bg-white">
            <BuilderSidebar activePageId={activePageId} />
            <CanvasArea activePageId={activePageId} blueprint={blueprint} />
            <PropertiesPanel />
        </div>
    );
};

export default BuilderLayout;
