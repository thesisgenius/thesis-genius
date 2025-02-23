import apiClient from "./apiClient";

const userAPI = {
    // Get the current user's profile
    getUserProfile: async () => {
        try {
            const response = await apiClient.get("/user/profile");
            return response.data;
        } catch (error) {
            throw error;
        }
    },

    // Update the user's profile
    updateUserProfile: async (profileData) => {
        try {
            const response = await apiClient.put("/user/profile", profileData);
            return response.data;
        } catch (error) {
            throw error;
        }
    },

    // Upload profile picture
    uploadProfilePicture: async (formData) => {
        try {
            const response = await apiClient.post("/user/profile-picture", formData, {
                headers: {
                    "Content-Type": "multipart/form-data",
                },
            });
            return response.data;
        } catch (error) {
            throw error;
        }
    },

    // Activate a user by ID
    activateUser: async (userId) => {
        try {
            const response = await apiClient.put(`/user/activate/${userId}`);
            return response.data;
        } catch (error) {
            throw error;
        }
    },

    // Deactivate the current user
    deactivateUser: async () => {
        try {
            const response = await apiClient.put("/user/deactivate");
            return response.data;
        } catch (error) {
            throw error;
        }
    },

    // Delete a user by ID
    deleteUser: async (userId) => {
        try {
            const response = await apiClient.delete(`/user/${userId}`);
            return response.data;
        } catch (error) {
            throw error;
        }
    },
};

export default userAPI;