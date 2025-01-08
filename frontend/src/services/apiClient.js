import axios from "axios";

// Create an Axios instance
const apiClient = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8557/api", // Backend API URL
    headers: { "Content-Type": "application/json" },
});

// Add request interceptor to include JWT token
apiClient.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem("token");
        if (token) {
            config.headers["Authorization"] = `Bearer ${token}`;
        }
        return config;
    },
    (error) => Promise.reject(error)
);

// Add response interceptor for error handling
apiClient.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response && error.response.status === 401) {
            localStorage.removeItem("token");
            window.location.href = "/signin"; // Redirect to sign-in
        }
        return Promise.reject(error);
    }
);

export default apiClient;
