export const hardeningPayloads = {
    // 1. Deep Nesting (Testing recursion limits and styling cascade)
    deepNesting: {
        id: 'hardening-deep',
        type: 'container',
        style: { padding: '20px', border: '1px solid #ccc' },
        children: Array.from({ length: 10 }).reduce((acc, _, i) => [{
            id: `level-${i}`,
            type: 'container',
            style: { padding: '10px', backgroundColor: `rgba(0,0,255,${0.1})` },
            children: acc
        }], [{
            id: 'deep-text',
            type: 'text',
            props: { content: 'Level 10 Depth' }
        }])[0]
    },

    // 2. Unknown/Invalid Nodes (Testing safe failure)
    invalidNodes: {
        id: 'hardening-invalid',
        type: 'container',
        children: [
            {
                id: 'valid-1',
                type: 'text',
                props: { content: 'I am valid' }
            },
            {
                id: 'invalid-hero',
                type: 'carousel', // Does not exist
                props: { images: [] }
            },
            {
                id: 'invalid-2',
                type: 'undefined',
                props: {}
            },
            {
                id: 'valid-2',
                type: 'text',
                props: { content: 'I am also valid, rendering after errors.' }
            }
        ]
    },

    // 3. Extreme Styles (CSS Stress)
    extremeStyles: {
        id: 'hardening-styles',
        type: 'card',
        style: {
            background: 'linear-gradient(45deg, #ff0000, #0000ff)',
            padding: '50px',
            transform: 'rotate(5deg)',
            boxShadow: '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)',
            color: 'white'
        },
        children: [
            {
                id: 'rotated-text',
                type: 'text',
                props: { tag: 'h1', content: 'Extreme Styling' },
                style: { fontSize: '48px', textShadow: '2px 2px 4px black' }
            }
        ]
    },

    // 4. Large Volume (Perf Test)
    largeVolume: {
        id: 'hardening-volume',
        type: 'container',
        style: { display: 'grid', gridTemplateColumns: 'repeat(10, 1fr)', gap: '4px' },
        children: Array.from({ length: 200 }).map((_, i) => ({
            id: `vol-${i}`,
            type: 'container',
            style: { width: '100%', aspectRatio: '1', backgroundColor: '#cbd5e1' }
        }))
    }
};
