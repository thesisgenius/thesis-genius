import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import apiClient from "../services/apiClient";

const Dashboard = () => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);
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

// Inline CSS Styles for simplicity
const styles = {
    container: {
        fontFamily: "Arial, sans-serif",
        padding: "20px",
        backgroundColor: "#f9f9f9",
        minHeight: "100vh",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
    },
    header: {
        width: "100%",
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        padding: "10px 20px",
        backgroundColor: "#007acc",
        color: "#fff",
    },
    logoutButton: {
        padding: "10px 20px",
        fontSize: "14px",
        backgroundColor: "#fff",
        color: "#007acc",
        border: "none",
        borderRadius: "4px",
        cursor: "pointer",
    },
    main: {
        flex: 1,
        width: "100%",
        maxWidth: "600px",
        marginTop: "20px",
    },
    profileCard: {
        backgroundColor: "#fff",
        padding: "20px",
        borderRadius: "8px",
        boxShadow: "0 2px 4px rgba(0, 0, 0, 0.1)",
    },
    centered: {
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
        minHeight: "100vh",
        fontFamily: "Arial, sans-serif",
        textAlign: "center",
    },
    button: {
        marginTop: "20px",
        padding: "10px 20px",
        fontSize: "16px",
        backgroundColor: "#007acc",
        color: "#fff",
        border: "none",
        borderRadius: "4px",
        cursor: "pointer",
    },
};
