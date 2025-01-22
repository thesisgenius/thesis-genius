import React, { createContext, useState, useEffect, useContext } from "react";
import apiClient from "../services/apiClient";

const AuthContext = createContext(null);

export const useAuth = () => {
    return useContext(AuthContext);
};

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const token = localStorage.getItem("token");
        if (!token) {
            console.log("No token found");
            setLoading(false); // Ensure loading ends if no token
            return;
        }

        apiClient.get("/user/profile")
            .then((response) => {
                console.log("User fetched:", response.data.user);
                setUser(response.data.user);
            })
            .catch(() => {
                console.log("Invalid token, removing...");
                localStorage.removeItem("token");
            })
            .finally(() => setLoading(false));
    }, []); // Ensure dependencies do not cause re-triggering

    const signIn = async (email, password) => {
        try {
            const response = await apiClient.post("/auth/signin", { email, password });
            const { token } = response.data;

            localStorage.setItem("token", token); // Save the token
            const userResponse = await apiClient.get("/user/profile");
            setUser(userResponse.data.user); // Update the user
            return true;
        } catch (error) {
            console.error("Sign-in failed:", error);
            return false;
        }
    };

    const signOut = async () => {
        try {
            await apiClient.post("/auth/signout"); // Ensure server logs out
        } catch (error) {
            console.error("Sign-out failed:", error);
        } finally {
            localStorage.removeItem("token");
            setUser(null);
        }
    };

    const value = {
        user,
        loading,
        signIn,
        signOut,
    };

    return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
