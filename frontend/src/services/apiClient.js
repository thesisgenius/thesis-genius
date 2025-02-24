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
 * Generic helper to call the Axios instance and return .data
 * @param {string} method - "get" | "post" | "put" | "delete"
 * @param {string} url - Endpoint path
 * @param {any} [payload] - Body data or config
 * @param {object} [config] - Optional axios config overrides
 */
export const request = async (method, url, payload, config = {}) => {
  // For GET/DELETE, we pass payload as config params if needed
  const needsBody = ["post", "put"].includes(method);
  const response = await apiClient({
    method,
    url,
    ...(needsBody ? { data: payload } : {}),
    ...(!needsBody ? { params: payload } : {}),
    ...config,
  });
  return response.data;
};

export default apiClient;
