import React, { createContext, useState, useEffect, useContext, useMemo } from "react";
import authAPI from "../services/authEndpoint"; // Import the authAPI
import userAPI from "../services/userEndpoint"; // Import the userAPI

export const AuthContext = createContext(null);

// Custom hook for using the Auth context
export const useAuth = () => {
    return useContext(AuthContext);
};

// AuthProvider component to manage authentication state
export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    // Check for an existing token and fetch user profile on mount
    useEffect(() => {
        const token = localStorage.getItem("token");
        if (!token) {
            console.log("No token found");
            setUser(null);
            setLoading(false); // End loading if no token
            return;
        }

        userAPI
            .getUserProfile() // Fetch user profile using userAPI
            .then((user) => {
                console.log("User fetched:", user);
                setUser(user);
            })
            .catch(() => {
                console.log("Invalid token, removing...");
                localStorage.removeItem("token");
            })
            .finally(() => setLoading(false)); // Ensure loading ends
    }, []);

    // Sign-in function
    const signIn = async (email, password) => {
        try {
            const { token } = await authAPI.signIn(email, password); // Get token
            localStorage.setItem("token", token);

            const user = await userAPI.getUserProfile(); // Fetch user profile
            setUser(user);

            return true;
        } catch (error) {
            console.error("Sign-in failed:", error);
            return false;
        }
    };

    // Sign-out function
    const signOut = async () => {
        try {
            await authAPI.signOut(); // Ensure the server logs out
        } catch (error) {
            console.error("Sign-out failed:", error);
        } finally {
            localStorage.removeItem("token");
            setUser(null);
        }
    };

    // Refresh user explicitly
    const refreshUser = () => {
        setLoading(true);
        fetchUser();
    };

    // Memoize the context value to optimize re-renders
    const value = useMemo(
        () => ({
            user,
            loading,
            signIn,
            signOut,
        }),
        [user, loading] // Dependencies that trigger re-computation
    );

    return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};