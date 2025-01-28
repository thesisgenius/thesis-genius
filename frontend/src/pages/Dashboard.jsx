import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import apiClient from "../services/apiClient";
import "../styles/Dashboard.css";

const Dashboard = () => {
    const [user, setUser] = useState(null);
    const [theses, setTheses] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");
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

    const fetchTheses = async () => {
        try {
            const response = await apiClient.get("/thesis/theses");
            setTheses(response.data.theses || []);
        } catch (error) {
            console.error("Failed to fetch theses:", error);
            setError("Failed to load theses. Please try again.");
        }
    };

    const handleExport = async (thesisId, format) => {
        try {
            const response = await apiClient.get(`/format/apa/${thesisId}`, {
                params: { format },
                responseType: "blob",
            });
            let thesisName;
            thesisName = theses.find((thesis) => thesis.id === thesisId)?.title;
            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement("a");
            link.href = url;
            link.setAttribute("download", `${thesisName}.${format}`);
            document.body.appendChild(link);
            link.click();
            link.parentNode.removeChild(link);
        } catch (error) {
            console.error("Error exporting thesis:", error);
        }
    };

    // Handle deletion of a thesis
    const handleDeleteThesis = async (id) => {
        const confirmDelete = window.confirm(
            "Are you sure you want to delete this thesis? This action cannot be undone."
        );

        if (!confirmDelete) {
            return; // Exit the function if the user cancels
        }

        try {
            await apiClient.delete(`/thesis/${id}`);
            setTheses((prevTheses) => prevTheses.filter((thesis) => thesis.id !== id)); // Remove the deleted thesis
        } catch (error) {
            console.error("Failed to delete thesis:", error);
        }
    };

    useEffect(() => {
        fetchUserProfile();
        fetchTheses();
    }, []);

    if (loading) {
        return <p>Loading...</p>;
    }

    if (error) {
        return (
            <div style={styles.centered}>
                <p>{error}</p>
            </div>
        );
    }

    return (
        <div style={styles.container}>
            <header>
                <h2>Welcome, {user?.first_name}!</h2>
            </header>

            <main style={styles.main}>
                <div>
                    <h3>Theses</h3>
                    <ul style={{ listStyle: "none", padding: 0 }}>
                        {theses.map((thesis) => (
                            <li key={thesis.id} style={{ marginBottom: "10px" }}>
                                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                                    <button
                                        style={{
                                            background: "none",
                                            border: "none",
                                            color: "#007acc",
                                            cursor: "pointer",
                                            textDecoration: "underline",
                                        }}
                                        onClick={() => navigate(`/thesis/${thesis.id}`)}
                                    >
                                        {thesis.title}
                                    </button>
                                    <div>
                                        <button
                                            style={styles.button}
                                            onClick={() => handleExport(thesis.id, "docx")}
                                        >
                                            Word (docx)
                                        </button>
                                        <button
                                            style={{...styles.button, marginLeft: "10px"}}
                                            onClick={() => handleExport(thesis.id, "pdf")}
                                        >
                                            PDF
                                        </button>
                                        <button
                                            style={{...styles.button, marginLeft: "10px", backgroundColor: "#ff0000"}}
                                            onClick={() => handleDeleteThesis(thesis.id)}>Delete
                                        </button>
                                    </div>
                                </div>
                            </li>
                        ))}
                    </ul>
                </div>
            </main>
        </div>
    );
};

export default Dashboard;

// Inline styles for simplicity
const styles = {
    container: {
        padding: "20px",
        maxWidth: "800px",
        margin: "0 auto",
        fontFamily: "Arial, sans-serif",
    },
    list: {
        listStyleType: "none",
        padding: 0,
    },
    thesisItem: {
        marginBottom: "15px",
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
    },
    thesisTitle: {
        cursor: "pointer",
        textDecoration: "underline",
        color: "#007acc",
    },
    button: {
        marginLeft: "10px",
        padding: "5px 10px",
        backgroundColor: "#007acc",
        color: "#fff",
        border: "none",
        borderRadius: "4px",
        cursor: "pointer",
    },
};

