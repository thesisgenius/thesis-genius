import React from "react";
import { useAuth } from "../context/AuthContext";

const ProtectedRoute = ({ children }) => {
    const { user, loading } = useAuth();

    // Prevent rendering until loading is complete
    if (loading) return <p>Loading...</p>;

    // Render children if authenticated
    return children;
};

export default ProtectedRoute;
