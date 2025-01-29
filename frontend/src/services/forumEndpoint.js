import apiClient from "./apiClient";

const forumAPI = {
    // Fetch a list of posts
    getPosts: async () => {
        try {
            const response = await apiClient.get("/forum/posts");
            return response.data;
        } catch (error) {
            throw error;
        }
    },

    // Get a specific post by ID
    getPostById: async (postId) => {
        try {
            const response = await apiClient.get(`/forum/posts/${postId}`);
            return response.data;
        } catch (error) {
            throw error;
        }
    },

    // Create a new post
    createPost: async (postData) => {
        try {
            const response = await apiClient.post("/forum/posts/new", postData);
            return response.data;
        } catch (error) {
            throw error;
        }
    },

    // Update an existing post
    updatePost: async (postId, postData) => {
        try {
            const response = await apiClient.put(`/forum/posts/${postId}`, postData);
            return response.data;
        } catch (error) {
            throw error;
        }
    },

    // Delete a specific post by ID
    deletePost: async (postId) => {
        try {
            const response = await apiClient.delete(`/forum/posts/${postId}`);
            return response.data;
        } catch (error) {
            throw error;
        }
    },

    // Add a comment to a post
    addComment: async (postId, commentData) => {
        try {
            const response = await apiClient.post(`/forum/posts/${postId}/comments`, commentData);
            return response.data;
        } catch (error) {
            throw error;
        }
    },

    // Delete a comment by ID
    deleteComment: async (postId, commentId) => {
        try {
            const response = await apiClient.delete(`/forum/posts/${postId}/comments/${commentId}`);
            return response.data;
        } catch (error) {
            throw error;
        }
    },

    // Delete all comments for a specific post
    deleteAllComments: async (postId) => {
        try {
            const response = await apiClient.delete(`/forum/posts/${postId}/comments`);
            return response.data;
        } catch (error) {
            throw error;
        }
    },

    // Get a specific comment
    getComment: async (postId, commentId) => {
        try {
            const response = await apiClient.get(`/forum/posts/${postId}/comments/${commentId}`);
            return response.data;
        } catch (error) {
            throw error;
        }
    },

    // Update a specific comment by ID
    updateComment: async (postId, commentId, commentData) => {
        try {
            const response = await apiClient.put(
                `/forum/posts/${postId}/comments/${commentId}`,
                commentData
            );
            return response.data;
        } catch (error) {
            throw error;
        }
    },
};

export default forumAPI;