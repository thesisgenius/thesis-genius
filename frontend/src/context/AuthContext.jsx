import React, { createContext, useState, useEffect, useContext, useMemo } from "react";
import authAPI from "../services/authEndpoint";
import userAPI from "../services/userEndpoint";

export const AuthContext = createContext(null);

export const useAuth = () => useContext(AuthContext);

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    // ✅ Fetch user profile only if token exists
    const fetchUser = async () => {
        const token = localStorage.getItem("token");

        if (!token) {
            setLoading(false); // Stop loading if no token exists
            return null;       // ✅ No error thrown, just skip fetch
        }

        try {
            const user = await userAPI.getUserProfile();
            setUser(user);
            return user;
        } catch (error) {
            console.error("Failed to fetch user profile:", error);
            localStorage.removeItem("token"); // Clear invalid token
            setUser(null);
            return null;
        } finally {
            setLoading(false);
        }
    };

    // 🏃‍♂️ Initialize: Fetch user profile if token is present
    useEffect(() => {
        (async () => {
            setLoading(true); 
            await fetchUser(); 
        })();
    }, []);

    // 🔑 Sign-in flow: Save token, fetch user, and refresh page
    const signIn = async (email, password) => {
        try {
            const { token } = await authAPI.signIn(email, password);
            localStorage.setItem("token", token); 
            await fetchUser();                      // Fetch profile after setting token
            window.location.reload();               // 🔄 Refresh UI
            return true;
        } catch (error) {
            console.error("Sign-in failed:", error);
            return false;
        }
    };

    // 🔓 Sign-out flow: Remove token and reset user
    const signOut = async () => {
        try {
            await authAPI.signOut(); 
        } catch (error) {
            console.error("Sign-out failed:", error);
        } finally {
            localStorage.removeItem("token");
            setUser(null); 
            window.location.reload();  // ✅ Refresh after logout
        }
    };

    const refreshUser = async () => {
        setLoading(true); 
        await fetchUser(); // Refetch user info
    };

    const value = useMemo(() => ({
        user,
        loading,
        signIn,
        signOut,
        refreshUser: fetchUser, // External refresh capability
    }), [user, loading]);

    return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
