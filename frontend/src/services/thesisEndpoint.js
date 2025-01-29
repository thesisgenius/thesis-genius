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

    // Edit a thesis by ID
    editThesis: async (thesisId, thesisData) => {
        try {
            const response = await apiClient.put(`/thesis/${thesisId}`, thesisData);
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
                params: { format },
                responseType: "blob", // Ensure it's returned as a file blob
            });
            return response;
        } catch (error) {
            throw error;
        }
    },
};

export default thesisAPI;