import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import userAPI from "../services/userEndpoint";
import thesisAPI from "../services/thesisEndpoint";
import "../styles/Dashboard.css";
import "../styles/ThesisCreate.css";

const Dashboard = () => {
    const [user, setUser] = useState(null);
    const [theses, setTheses] = useState([]);
    const [newThesis, setNewThesis] = useState({ title: "", abstract: "", status: "Draft" });
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");
    const navigate = useNavigate();

    useEffect(() => {
        const fetchInitialData = async () => {
            try {
                const token = localStorage.getItem("token");
                if (!token) {
                    navigate("/signin");
                    return;
                }

                const [userProfile, thesesData] = await Promise.all([
                    userAPI.getUserProfile(),
                    thesisAPI.listTheses(),
                ]);

                setUser(userProfile.user);
                setTheses(thesesData.theses || []);
            } catch (error) {
                console.error("Error loading data:", error);
                setError("Failed to load data. Please try again.");
            } finally {
                setLoading(false);
            }
        };

        fetchInitialData();
    }, [navigate]);

    const handleInputChange = ({ target: { name, value } }) => {
        setNewThesis((prev) => ({ ...prev, [name]: value }));
    };

    const handleCreateThesis = async (e) => {
        e.preventDefault();
        try {
            const response = await thesisAPI.createThesis(newThesis);
            setTheses((prev) => [response.thesis, ...prev]);
            setNewThesis({ title: "", abstract: "", status: "Draft" });
        } catch (error) {
            console.error("Error creating thesis:", error);
            setError("Failed to create thesis. Please try again.");
        }
    };

    const handleDeleteThesis = async (id) => {
        if (window.confirm("Are you sure you want to delete this thesis? This action cannot be undone.")) {
            try {
                await thesisAPI.deleteThesis(id);
                setTheses((prev) => prev.filter((thesis) => thesis.id !== id));
            } catch (error) {
                console.error("Error deleting thesis:", error);
                setError("Failed to delete thesis. Please try again.");
            }
        }
    };

    const handleExport = async (thesisId, format) => {
        try {
            // Use the new exportThesis API function
            const response = await thesisAPI.exportThesis(thesisId, format);

            // Extract filename from response headers if available
            const contentDisposition = response.headers["content-disposition"];
            const fileName = contentDisposition
                ? contentDisposition.match(/filename="?([^;"]+)"?/)[1]
                : `thesis_${thesisId}.${format}`;

            // Create a download link
            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement("a");
            link.href = url;
            link.setAttribute("download", fileName);
            document.body.appendChild(link);
            link.click();
            link.parentNode.removeChild(link);
        } catch (error) {
            console.error("Error exporting thesis:", error);
            setError("Failed to export thesis. Please try again.");
        }
    };

    if (loading) return <p>Loading...</p>;
    if (error) return <div className="error-message">{error}</div>;

    return (
        <div className="dashboard-container">
            <header>
                <h1>Welcome, {user?.first_name}!</h1>
            </header>
            <main>
                {/* Create New Thesis Section */}
                <NewThesisForm
                    newThesis={newThesis}
                    onChange={handleInputChange}
                    onSubmit={handleCreateThesis}
                />

                {/* Thesis List */}
                <section className="theses-list">
                    <h2>Your Theses</h2>
                    {theses.length > 0 ? (
                        theses.map((thesis) => (
                            <ThesisCard
                                key={thesis.id}
                                thesis={thesis}
                                onView={() => navigate(`/thesis/${thesis.id}`)}
                                onExport={handleExport}
                                onDelete={handleDeleteThesis}
                            />
                        ))
                    ) : (
                        <p>No theses found. Start by creating one!</p>
                    )}
                </section>
            </main>
        </div>
    );
};

// Reusable Component: New Thesis Form
const NewThesisForm = ({ newThesis, onChange, onSubmit }) => (
    <div className="create-thesis">
        <h2>Create a New Thesis</h2>
        <form onSubmit={onSubmit}>
            <label>Title</label>
            <input
                type="text"
                name="title"
                value={newThesis.title}
                onChange={onChange}
                placeholder="Enter thesis title"
                required
            />
            <label>Status</label>
            <select name="status" value={newThesis.status} onChange={onChange}>
                <option value="Draft">Draft</option>
                <option value="Approved">Approved</option>
                <option value="Rejected">Rejected</option>
            </select>
            <button type="submit">Submit</button>
        </form>
    </div>
);

// Reusable Component: Thesis Card
const ThesisCard = ({ thesis, onView, onExport, onDelete }) => (
    <div className="thesis-item">
        <span className="title" onClick={onView}>
            {thesis.title}
        </span>
        <div className="export-buttons">
            <button onClick={() => onExport(thesis.id, "docx")}>Word (docx)</button>
            <button onClick={() => onExport(thesis.id, "pdf")}>PDF</button>
            <button className="danger" onClick={() => onDelete(thesis.id)}>
                Delete
            </button>
        </div>
    </div>
);

export default Dashboard;