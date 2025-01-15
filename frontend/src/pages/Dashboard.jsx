import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import apiClient from "../services/apiClient";

const Dashboard = () => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);
    const navigate = useNavigate();

    useEffect(() => {
        // Self-invoking function for async logic
        (async () => {
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
                navigate("/signin");
            } finally {
                setLoading(false);
            }
        })();
    }, [navigate]);

    if (loading) {
        return <p>Loading...</p>;
    }

    if (!user) {
        return <p>Failed to load user data. Please try again.</p>;
    }

    return (
        <div>
            <h1>Welcome, {user.first_name}!</h1>
            <p>Email: {user.email}</p>
        </div>
    );
};

export default Dashboard;
