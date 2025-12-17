
import { hardeningPayloads } from './hardeningPayloads';

// Default data for the pages
export const initialBlueprints = {
    home: {
        id: 'home',
        name: 'Home',
        elements: [
            {
                id: 'root-container',
                type: 'container',
                style: {
                    padding: '40px',
                    backgroundColor: '#f8fafc',
                    height: '100%',
                    gap: '20px'
                },
                children: [
                    {
                        id: 'hero-card',
                        type: 'card',
                        style: {
                            backgroundColor: '#ffffff',
                            padding: '30px',
                            borderRadius: '12px',
                            gap: '16px'
                        },
                        children: [
                            {
                                id: 'hero-title',
                                type: 'text',
                                props: {
                                    tag: 'h1',
                                    content: 'Welcome to Your AI Store'
                                },
                                style: {
                                    fontSize: '32px',
                                    fontWeight: 'bold',
                                    color: '#1e293b'
                                }
                            },
                            {
                                id: 'hero-desc',
                                type: 'text',
                                props: {
                                    tag: 'p',
                                    content: 'This UI is rendered entirely from JSON blueprint data. No hardcoded React components here!'
                                },
                                style: {
                                    fontSize: '16px',
                                    color: '#64748b'
                                }
                            },
                            {
                                id: 'hero-btn',
                                type: 'button',
                                props: {
                                    label: 'Start Building'
                                },
                                style: {
                                    backgroundColor: '#3b82f6',
                                    color: 'white',
                                    padding: '12px 24px',
                                    borderRadius: '8px',
                                    fontWeight: '500',
                                    width: 'fit-content',
                                    border: 'none'
                                }
                            }
                        ]
                    }
                ]
            }
        ],
        tokens: {},
        history: [],
        version: 1
    },
    about: {
        id: 'about',
        name: 'About',
        elements: [
            {
                id: 'about-container',
                type: 'container',
                style: { padding: '40px' },
                children: [
                    {
                        id: 'about-title',
                        type: 'text',
                        props: { tag: 'h1', content: 'About Us' },
                        style: { fontSize: '24px', fontWeight: 'bold' }
                    }
                ]
            }
        ],
        tokens: {},
        history: [],
        version: 1
    },
    store: {
        id: 'store',
        name: 'Store',
        elements: [],
        tokens: {},
        history: [],
        version: 1
    },
    hardening: {
        id: 'hardening',
        name: 'Hardening Lab',
        elements: [
            {
                id: 'lab-root',
                type: 'container',
                style: { padding: '20px', gap: '40px', backgroundColor: '#f0f9ff', height: '100%', overflow: 'auto' },
                children: [
                    hardeningPayloads.deepNesting,
                    hardeningPayloads.invalidNodes,
                    hardeningPayloads.extremeStyles,
                    hardeningPayloads.largeVolume
                ]
            }
        ],
        tokens: {},
        history: [],
        version: 1
    }
};
