import React from 'react';
import {
    ContainerRenderer,
    TextRenderer,
    ButtonRenderer,
    CardRenderer
} from './primitives';

// Mapping of node types to renderer components
const RENDERER_MAP = {
    'container': ContainerRenderer,
    'text': TextRenderer,
    'button': ButtonRenderer,
    'card': CardRenderer
};

// Recursive Node Renderer
const NodeRenderer = ({ node }) => {
    if (!node) return null;

    const Renderer = RENDERER_MAP[node.type];

    if (!Renderer) {
        console.warn(`No renderer found for type: ${node.type}`);
        return null; // Fail safely
    }

    // Prepare styles from blueprint tokens/style object
    const style = node.style || {};

    // Recursively render children if they exist
    const children = node.children?.map(child => (
        <NodeRenderer key={child.id} node={child} />
    ));

    return (
        <Renderer node={node} style={style}>
            {children}
        </Renderer>
    );
};

// Main Entry Point
const BlueprintRenderer = ({ blueprint }) => {
    if (!blueprint || !blueprint.elements || blueprint.elements.length === 0) {
        return (
            <div className="h-full w-full flex items-center justify-center text-slate-400">
                <div className="text-center">
                    <p>No Elements to Render</p>
                    <p className="text-xs mt-2">Add elements to the blueprint to see them here.</p>
                </div>
            </div>
        );
    }

    return (
        <div className="w-full h-full bg-white relative">
            {/* 
                We assume blueprint.elements is an array of root nodes.
                Typically a page has one root, but we support an array.
             */}
            {blueprint.elements.map(node => (
                <NodeRenderer key={node.id} node={node} />
            ))}
        </div>
    );
};

export default BlueprintRenderer;
