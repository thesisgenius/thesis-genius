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
    // Fetch user profile
    const fetchUser = async () => {
        try {
            const token = localStorage.getItem("token");
            if (!token) throw new Error("No token found");

            const user = await userAPI.getUserProfile();
            setUser(user);
            return user;
        } catch (error) {
            console.error("Failed to fetch user profile:", error);
            localStorage.removeItem("token");
            setUser(null);
            return null;
        } finally {
            setLoading(false);
        }
    };

    // On initialization
    useEffect(() => {
        (async () => {
            setLoading(true); // Show loading state during initialization
            await fetchUser(); // Fetch the user's profile
        })();
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
    const refreshUser = async () => {
        setLoading(true); // Show loading spinner during refresh
        await fetchUser(); // Refetch and update user details
    };

    // Memoize the context value to optimize re-renders
    const value = useMemo(
        () => ({
            user,
            loading,
            signIn,
            signOut,
            refreshUser: fetchUser, // Allow refreshUser to be triggered externally
        }),
        [user, loading]
    );

    return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};