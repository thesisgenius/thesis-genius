import axios from "axios";
import apiClient from "../services/apiClient";
import { vi, describe, it, expect, beforeEach } from "vitest";

// Mock axios
vi.mock("axios", () => {
    const mockAxiosInstance = {
        interceptors: {
            request: { use: vi.fn() },
            response: { use: vi.fn() },
        },
        get: vi.fn(),
        post: vi.fn(),
        put: vi.fn(),
        delete: vi.fn(),
        defaults: { headers: { common: {} } },
    };

    return {
        default: {
            create: vi.fn(() => mockAxiosInstance),
        },
        __esModule: true,
    };
});

describe("apiClient", () => {
    let mockAxios;

    beforeEach(() => {
        // Reinitialize mockAxios before each test
        mockAxios = axios.create();
        localStorage.clear();
    });

    it("sets the authorization header with token", () => {
        const token = "test-token";
        localStorage.setItem("token", token);

        // Simulate the request interceptor that sets the Authorization header
        mockAxios.interceptors.request.use.mockImplementation((config) => {
            const token = localStorage.getItem("token");
            if (token) {
                config.headers.Authorization = `Bearer ${token}`;
            }
            return config;
        });

        // Trigger the request interceptor manually for testing
        const config = { headers: {} };
        mockAxios.interceptors.request.use.mock.calls[0][0](config);

        // Verify that the Authorization header is correctly set
        expect(config.headers.Authorization).toBe(`Bearer ${token}`);
    });

    it("should call get method correctly", async () => {
        const mockResponse = { data: { success: true } };
        mockAxios.get.mockResolvedValueOnce(mockResponse);

        const response = await apiClient.get("/test-endpoint");

        // Validate the mocked response
        expect(response).toEqual(mockResponse);

        // Ensure the mocked `get` method is called with the correct arguments
        expect(mockAxios.get).toHaveBeenCalledWith("/test-endpoint");
    });
});
