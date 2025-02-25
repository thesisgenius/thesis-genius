// frontend/src/context/AuthProvider.jsx
import React, { useState, useEffect, useMemo } from "react";
import { AuthContext } from "./authContext"; // <-- Import the context, not the provider
import authAPI from "../services/authEndpoint";
import userAPI from "../services/userEndpoint";

/**
 * AuthProvider is the React component that manages authentication state
 * and provides it to the rest of the app via AuthContext.
 *
 * If you want to force a top-level re-render for the entire app,
 * pass in `refreshApp` prop from, e.g., Root.jsx:
 *   <AuthProvider refreshApp={someFunction}>
 *     <App />
 *   </AuthProvider>
 */
export default function AuthProvider({ children, refreshApp }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  // Fetch user profile from the server
  async function fetchUser() {
    try {
      const token = localStorage.getItem("token");
      if (!token) throw new Error("No token found");
      const profile = await userAPI.getUserProfile();
      setUser(profile);
      return profile;
    } catch (error) {
      console.error("Failed to fetch user profile:", error);
      localStorage.removeItem("token");
      setUser(null);
      return null;
    } finally {
      setLoading(false);
    }
  }

  // On mount, attempt to load existing user
  useEffect(() => {
    setLoading(true);
    fetchUser();
  }, []);

  // Sign-in function
  async function signIn(email, password) {
    try {
      const { token } = await authAPI.signIn(email, password);
      localStorage.setItem("token", token);
      const newUser = await userAPI.getUserProfile();
      setUser(newUser);
      // If you want to re-init the entire app after sign-in:
      if (refreshApp) refreshApp();
      return true;
    } catch (error) {
      console.error("Sign-in failed:", error);
      return false;
    }
  }

  // Sign-out function
  async function signOut() {
    try {
      await authAPI.signOut();
    } catch (error) {
      console.error("Sign-out failed:", error);
    } finally {
      localStorage.removeItem("token");
      setUser(null);
      // Force a top-level re-render if desired
      if (refreshApp) refreshApp();
    }
  }

  // The context value provided to the rest of the app
  const value = useMemo(
    () => ({
      user,
      loading,
      signIn,
      signOut,
      refreshUser: fetchUser, // if you only need to reload user data
    }),
    [user, loading],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
