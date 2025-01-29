import apiClient from "./apiClient";

const statusAPI = {
    aliveCheck: async () => {
        try {
            const response = await apiClient.get("/status/alive");
            return response.data;
        } catch (error) {
            throw error;
        }
    },

    healthCheck: async () => {
        try {
            const response = await apiClient.get("/status/health");
            return response.data;
        } catch (error) {
            throw error;
        }
    },

    readinessCheck: async () => {
        try {
            const response = await apiClient.get("/status/ready");
            return response.data;
        } catch (error) {
            throw error;
        }
    },
};

export default statusAPI;