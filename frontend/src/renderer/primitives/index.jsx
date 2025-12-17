import React from 'react';

// === Primitive Renderers ===

// 1. container
export const ContainerRenderer = ({ node, children, style }) => {
    return (
        <div
            id={node.id}
            className="flex flex-col relative"
            style={{
                ...style,
                minHeight: '50px', // Visual aid if empty
            }}
        >
            {children}
        </div>
    );
};

// 2. text
export const TextRenderer = ({ node, style }) => {
    const Tag = node.props?.tag || 'p'; // Default to p, allow h1-h6 via props
    return (
        <Tag
            id={node.id}
            style={style}
        >
            {node.props?.content || 'Empty Text'}
        </Tag>
    );
};

// 3. button
export const ButtonRenderer = ({ node, style }) => {
    return (
        <button
            id={node.id}
            className="transition-opacity hover:opacity-90 active:scale-95"
            style={{
                ...style,
                cursor: 'pointer'
            }}
        >
            {node.props?.label || 'Button'}
        </button>
    );
};

// 4. card
export const CardRenderer = ({ node, children, style }) => {
    return (
        <div
            id={node.id}
            className="flex flex-col overflow-hidden"
            style={{
                ...style,
                boxShadow: style.boxShadow || '0 4px 6px -1px rgb(0 0 0 / 0.1)',
            }}
        >
            {children}
        </div>
    );
};
