import React, { useState, useEffect } from "react";
import apiClient from "../services/apiClient";
import "./../styles/Thesis.css";

const Thesis = () => {
    const [theses, setTheses] = useState([]);
    const [newThesis, setNewThesis] = useState({ title: "", abstract: "", status: "Pending" });
    const [loading, setLoading] = useState(true);

    // Fetch all theses on component load
    useEffect(() => {
        const fetchTheses = async () => {
            try {
                const response = await apiClient.get("/thesis/theses");
                setTheses(response.data.theses);
            } catch (error) {
                console.error("Failed to fetch theses:", error);
            } finally {
                setLoading(false);
            }
        };

        fetchTheses();
    }, []);

    // Handle input changes for creating or editing a thesis
    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setNewThesis({ ...newThesis, [name]: value });
    };

    // Handle submission of a new thesis
    const handleCreateThesis = async (e) => {
        e.preventDefault();
        try {
            const response = await apiClient.post("/thesis/thesis", newThesis);
            setTheses((prevTheses) => [response.data.thesis, ...prevTheses]); // Add the new thesis to the list
            setNewThesis({ title: "", abstract: "", status: "Pending" }); // Reset the form
        } catch (error) {
            console.error("Failed to create thesis:", error);
        }
    };

    // Handle deletion of a thesis
    const handleDeleteThesis = async (id) => {
        try {
            await apiClient.delete(`/thesis/thesis/${id}`);
            setTheses((prevTheses) => prevTheses.filter((thesis) => thesis.id !== id)); // Remove the deleted thesis
        } catch (error) {
            console.error("Failed to delete thesis:", error);
        }
    };

    if (loading) {
        return <p>Loading theses...</p>;
    }

    return (
        <div className="thesis-container">
            <h1>Thesis Management</h1>

            {/* New Thesis Form */}
            <div className="create-thesis">
                <h2>Create a New Thesis</h2>
                <form onSubmit={handleCreateThesis}>
                    <label>Title</label>
                    <input
                        type="text"
                        name="title"
                        value={newThesis.title}
                        onChange={handleInputChange}
                        placeholder="Enter thesis title"
                        required
                    />
                    <label>Abstract</label>
                    <textarea
                        name="abstract"
                        value={newThesis.abstract}
                        onChange={handleInputChange}
                        placeholder="Enter thesis abstract"
                        required
                    ></textarea>
                    <label>Status</label>
                    <select name="status" value={newThesis.status} onChange={handleInputChange}>
                        <option value="Pending">Pending</option>
                        <option value="Approved">Approved</option>
                        <option value="Rejected">Rejected</option>
                    </select>
                    <button type="submit">Submit</button>
                </form>
            </div>

            {/* List of Theses */}
            <div className="theses">
                <h2>Your Theses</h2>
                {theses.length === 0 ? (
                    <p>No theses available.</p>
                ) : (
                    theses.map((thesis) => (
                        <div key={thesis.id} className="thesis">
                            <h3>{thesis.title}</h3>
                            <p>{thesis.abstract}</p>
                            <small>Status: {thesis.status}</small>
                            <br />
                            <small>Created on: {new Date(thesis.created_at).toLocaleString()}</small>
                            <button onClick={() => handleDeleteThesis(thesis.id)}>Delete</button>
                        </div>
                    ))
                )}
            </div>
        </div>
    );
};

export default Thesis;
