import apiClient from "./apiClient";

const authAPI = {
    // Register a new user
    register: async (userData) => {
        try {
            const response = await apiClient.post("/auth/register", userData);
            return response.data;
        } catch (error) {
            throw error;
        }
    },

    // Sign in a user
    signIn: async (credentials) => {
        try {
            const response = await apiClient.post("/auth/signin", credentials);
            return response.data;
        } catch (error) {
            throw error;
        }
    },

    // Sign out the current user
    signOut: async () => {
        try {
            const response = await apiClient.post("/auth/signout");
            return response.data;
        } catch (error) {
            throw error;
        }
    },
};

export default authAPI;