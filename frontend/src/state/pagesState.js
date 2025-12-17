import { initialBlueprints } from '../data/initialBlueprints';

// In-memory registry for page states
// Each page owns: blueprint, history, uiState
const pageRegistry = {
    home: {
        blueprint: { ...initialBlueprints.home },
        history: [],
        uiState: {
            selection: null,
            zoom: 100,
            pan: { x: 0, y: 0 }
        }
    },
    about: {
        blueprint: { ...initialBlueprints.about },
        history: [],
        uiState: {
            selection: null,
            zoom: 100,
            pan: { x: 0, y: 0 }
        }
    },
    store: {
        blueprint: { ...initialBlueprints.store },
        history: [],
        uiState: {
            selection: null,
            zoom: 100,
            pan: { x: 0, y: 0 }
        }
    }
};

/**
 * Retrieves the full state object for a specific page.
 * @param {string} pageId - The ID of the page (home, about, store)
 * @returns {object|null} - The page state object or null if not found
 */
export const getPageState = (pageId) => {
    return pageRegistry[pageId] || null;
};

/**
 * Updates the blueprint for a specific page.
 * @param {string} pageId 
 * @param {object} newBlueprint 
 */
export const updatePageBlueprint = (pageId, newBlueprint) => {
    if (pageRegistry[pageId]) {
        pageRegistry[pageId].blueprint = newBlueprint;
    }
};

/**
 * Getting the list of available pages for navigation
 */
export const getAvailablePages = () => {
    return Object.keys(pageRegistry).map(key => ({
        id: key,
        name: pageRegistry[key].blueprint.name
    }));
};
