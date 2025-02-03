import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import apiClient from "../services/apiClient";

const Dashboard = () => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null); // Add error state
    const navigate = useNavigate();

    const fetchUserProfile = async () => {
        try {
            const token = localStorage.getItem("token");
            if (!token) {
                navigate("/signin");
                return;
            }

            const response = await apiClient.get("/user/profile");
            setUser(response.data.user);
        } catch (error) {
            console.error("Failed to fetch user profile:", error);
            setError("Failed to load user data. Please try again.");
        } finally {
            setLoading(false);
        }
    };

    const handleLogout = () => {
        localStorage.removeItem("token");
        navigate("/signin");
    };

    useEffect(() => {
        fetchUserProfile();
    }, [navigate]);

    if (loading) {
        return <p>Loading...</p>;
    }

    if (error) {
        return <p>{error}</p>;
    }

    return (
        <div>
            <h1>Welcome, {user.name}</h1>
            <button onClick={handleLogout}>Logout</button>
        </div>
    );
};

export default Dashboard;