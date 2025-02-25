import axios from "axios";

/**
 * Central Axios instance with:
 * - Base URL and JSON headers
 * - Credential support
 * - Automatic token injection
 * - 401 handling (logout + redirect)
 */
const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8557/api",
  headers: { "Content-Type": "application/json" },
  withCredentials: true,
});

apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("token");
    if (token) config.headers.Authorization = `Bearer ${token}`;
    return config;
  },
  (error) => Promise.reject(error),
);

apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error?.response?.status === 401) {
      localStorage.removeItem("token");
      window.location.href = "/signin";
    }
    return Promise.reject(error);
  },
);

/**
 * Generic helper to call the Axios instance and return either:
 *  - response.data (default), or
 *  - the entire Axios response if config.fullResponse = true
 *
 * @param {string} method - "get" | "post" | "put" | "delete"
 * @param {string} url - Endpoint path (relative to baseURL)
 * @param {any} [payload] - Body data (for POST/PUT) or query params (for GET/DELETE)
 * @param {object} [config] - Optional axios config overrides
 *   config.fullResponse: boolean (if true, returns full Axios response; otherwise returns response.data)
 *
 * @returns {Promise<any>} - Either response.data or the full response object
 */
export const request = async (method, url, payload, config = {}) => {
    // If config.fullResponse is set, store & remove so we don't pass it along to axios
    const { fullResponse = false, ...axiosConfig } = config;

    // For GET/DELETE, we pass payload as config params if needed
    const needsBody = ["post", "put", "patch"].includes(method.toLowerCase());

    const response = await apiClient({
        method,
        url,
        ...(needsBody ? { data: payload } : { params: payload }),
        ...axiosConfig,
    });

    // If fullResponse is true, return entire response (headers included).
    // Otherwise, return just response.data (the default).
    return fullResponse ? response : response.data;
};

export default apiClient;
