import React, { createContext, useState, useEffect, useContext } from "react";
import apiClient from "../services/apiClient";

// Create the AuthContext
const AuthContext = createContext(null);

// Create a custom hook to use the AuthContext
export const useAuth = () => {
    return useContext(AuthContext);
};

// AuthProvider component
export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    // Check for token and fetch user profile on initial load
    useEffect(() => {
        const token = localStorage.getItem("token");
        console.log("Token:", token);
        setTimeout(() => {
            if (token) {
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
            } else {
                console.log("No token found");
                setLoading(false);
            }
        }, 2000);
    }, []);

    // SignIn function
    const signIn = async (email, password) => {
        try {
            const response = await apiClient.post("/auth/signin", { email, password });
            const { token } = response.data;

            localStorage.setItem("token", token); // Save the token
            const userResponse = await apiClient.get("/user/profile");
            setUser(userResponse.data.user); // Set the user
            return true;
        } catch (error) {
            console.error("Sign-in failed:", error);
            return false;
        }
    };

    // SignOut function
    const signOut = () => {
        localStorage.removeItem("token");
        setUser(null);
    };

    const value = {
        user,
        loading,
        signIn,
        signOut,
    };

    return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
