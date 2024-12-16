import React, { useEffect, useState } from "react";
import axios from "axios";

const App = () => {
    const [theses, setTheses] = useState([]);
    const [newThesis, setNewThesis] = useState({ title: "", content: "" });

    // Fetch data from backend
    useEffect(() => {
        axios
            .get("http://localhost:5000/api/thesis")
            .then((response) => {
                setTheses(response.data); // Update state with fetched theses
            })
            .catch((error) => console.error("Error fetching theses:", error));
    }, []);

    // Handle form input changes
    const handleChange = (e) => {
        const { name, value } = e.target;
        setNewThesis((prev) => ({ ...prev, [name]: value }));
    };

    // Submit a new thesis to the backend
    const handleSubmit = (e) => {
        e.preventDefault();
        axios
            .post("http://localhost:5000/api/thesis", newThesis)
            .then((response) => {
                alert(response.data.message); // Show success message
                setNewThesis({ title: "", content: "" }); // Clear form
                // Refresh the theses list
                return axios.get("http://localhost:5000/api/thesis");
            })
            .then((response) => setTheses(response.data))
            .catch((error) => console.error("Error adding thesis:", error));
    };

    return (
        <div>
            <h1>Thesis Management</h1>

            {/* Display Theses */}
            <h2>Existing Theses</h2>
            <ul>
                {theses.map((thesis) => (
                    <li key={thesis.id}>
                        <strong>{thesis.title}</strong>: {thesis.content}
                    </li>
                ))}
            </ul>

            {/* Form to Add New Thesis */}
            <h2>Add a New Thesis</h2>
            <form onSubmit={handleSubmit}>
                <div>
                    <label>Title: </label>
                    <input
                        type="text"
                        name="title"
                        value={newThesis.title}
                        onChange={handleChange}
                        required
                    />
                </div>
                <div>
                    <label>Content: </label>
                    <textarea
                        name="content"
                        value={newThesis.content}
                        onChange={handleChange}
                        required
                    ></textarea>
                </div>
                <button type="submit">Add Thesis</button>
            </form>
        </div>
    );
};

export default App;
