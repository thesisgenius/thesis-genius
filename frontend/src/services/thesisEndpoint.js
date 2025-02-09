import apiClient from "./apiClient";

const thesisAPI = {
    // Create a new thesis
    createThesis: async (thesisData) => {
        try {
            const response = await apiClient.post("/thesis/new", thesisData);
            return response.data;
        } catch (error) {
            throw error;
        }
    },

    // Get a list of theses
    listTheses: async () => {
        try {
            const response = await apiClient.get("/thesis/theses");
            return response.data;
        } catch (error) {
            throw error;
        }
    },

    // Get a specific thesis by ID
    getThesis: async (thesisId) => {
        try {
            const response = await apiClient.get(`/thesis/${thesisId}`);
            return response.data;
        } catch (error) {
            throw error;
        }
    },
    // Get Cover Page
    getCoverPage: async (thesisId) => {
        try {
            const response = await apiClient.get(`/thesis/${thesisId}/cover-page`);
            return response.data.cover_page; // Ensure this matches the backend response format
        } catch (error) {
            throw error;
        }
    },


    // Update Cover Page
    updateCoverPage: async (thesisId, coverData) => {
        try {
            const response = await apiClient.put(`/thesis/${thesisId}/cover-page`, coverData);
            return response.data.cover_page;
        } catch (error) {
            throw error;
        }
    },

    // Fetch TOC
    getTableOfContents: async (thesisId) => {
        try {
            const response = await apiClient.get(`/thesis/${thesisId}/table-of-contents`);
            return response.data.table_of_contents;
        } catch (error) {
            throw error;
        }
    },

    // Update TOC
    updateTableOfContents: async (thesisId, tocData) => {
        try {
            const response = await apiClient.put(`/thesis/${thesisId}/table-of-contents`, {table_of_contents: tocData});
            return response.data.table_of_contents;
        } catch (error) {
            throw error;
        }
    },

    // Get the abstract of a thesis
    getAbstract: async (thesisId) => {
        try {
            const response = await apiClient.get(`/thesis/${thesisId}/abstract`);
            return response.data;
        } catch (error) {
            throw error;
        }
    },

    // Update or create an abstract for a thesis
    updateAbstract: async (thesisId, abstractData) => {
        try {
            const response = await apiClient.post(`/thesis/${thesisId}/abstract`, abstractData);
            return response.data;
        } catch (error) {
            throw error;
        }
    },

    // Delete the abstract of a thesis
    deleteAbstract: async (thesisId) => {
        try {
            const response = await apiClient.delete(`/thesis/${thesisId}/abstract`);
            return response.data;
        } catch (error) {
            throw error;
        }
    },

    // Get all body pages of a thesis
    getBodyPages: async (thesisId) => {
        try {
            const response = await apiClient.get(`/thesis/${thesisId}/body-pages`);
            return response.data.body_pages;
        } catch (error) {
            console.error("Error fetching body pages:", error.response?.data || error.message);
            throw error;
        }
    },

    // Add a body page to a thesis
    addBodyPage: async (thesisId, bodyPageData) => {
        try {
            const response = await apiClient.post(`/thesis/${thesisId}/body-pages`, bodyPageData);
            return response.data;
        } catch (error) {
            throw error;
        }
    },

    // Update a specific body page
    updateBodyPage: async (thesisId, pageId, pageData) => {
        try {
            const response = await apiClient.put(`/thesis/${thesisId}/body-pages/${pageId}`, pageData);
            return response.data;
        } catch (error) {
            throw error;
        }
    },

    // Delete a specific body page
    deleteBodyPage: async (thesisId, pageId) => {
        try {
            const response = await apiClient.delete(`/thesis/${thesisId}/body-pages/${pageId}`);
            return response.data;
        } catch (error) {
            throw error;
        }
    },


    // Delete a thesis by ID
    deleteThesis: async (thesisId) => {
        try {
            const response = await apiClient.delete(`/thesis/${thesisId}`);
            return response.data;
        } catch (error) {
            throw error;
        }
    },

    // Additional routes for figures, tables, etc.
    addFigure: async (thesisId, figureData) => {
        try {
            const response = await apiClient.post(`/thesis/${thesisId}/figures`, figureData);
            return response.data;
        } catch (error) {
            throw error;
        }
    },

    deleteFigure: async (figureId) => {
        try {
            const response = await apiClient.delete(`/thesis/figure/${figureId}`);
            return response.data;
        } catch (error) {
            throw error;
        }
    },

    // Export a formatted thesis
    exportThesis: async (thesisId, format) => {
        try {
            const response = await apiClient.get(`/format/apa/${thesisId}`, {
                params: {format},
                responseType: "blob", // Ensure it's returned as a file blob
            });
            return response;
        } catch (error) {
            throw error;
        }
    },
};

export default thesisAPI;