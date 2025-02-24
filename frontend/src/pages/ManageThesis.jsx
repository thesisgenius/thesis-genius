// ManageThesis.jsx
import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import userAPI from "../services/userEndpoint";
import thesisAPI from "../services/thesisEndpoint";

import "../styles/Dashboard.css";
import "../styles/ThesisCreate.css";

// 1) Import the ThesisContext hook
import { useThesis } from "../context/thesisContext";

const ManageThesis = () => {
  const [user, setUser] = useState(null);
  const [theses, setTheses] = useState([]);
  const [newThesis, setNewThesis] = useState({
    title: "",
    abstract: "",
    status: "Draft",
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const navigate = useNavigate();

  // 2) Destructure from ThesisContext
  const { activeThesisId, setActiveThesisId } = useThesis();

  useEffect(() => {
    const fetchInitialData = async () => {
      try {
        const token = localStorage.getItem("token");
        if (!token) {
          navigate("/signin");
          return;
        }

        // Using the existing userProfile + theses calls
        const [userProfile, thesesData] = await Promise.all([
          userAPI.getUserProfile(),
          thesisAPI.listTheses(),
        ]);

        setUser(userProfile.user);
        // The example code suggests your API returns { theses: [...] }
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
      // The code suggests the result might look like { thesis: { ... } }
      setTheses((prev) => [response.thesis, ...prev]);
      setNewThesis({ title: "", abstract: "", status: "Draft" });
    } catch (error) {
      console.error("Error creating thesis:", error);
      setError("Failed to create thesis. Please try again.");
    }
  };

  const handleDeleteThesis = async (id) => {
    if (
      window.confirm(
        "Are you sure you want to delete this thesis? This action cannot be undone.",
      )
    ) {
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
      const response = await thesisAPI.exportThesis(thesisId, format);
      // Attempt to parse 'content-disposition' header for filename
      const contentDisposition = response.headers["content-disposition"];
      const fileName = contentDisposition
        ? contentDisposition.match(/filename="?([^;"]+)"?/)[1]
        : `thesis_${thesisId}.${format}`;

      // Download logic
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

  // 3) A new helper function to set the active thesis in context
  const handleSelectThesis = async (thesisId) => {
    setActiveThesisId(thesisId);
    navigate(`/app/${activeThesisId}/title`);
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
                onView={() => handleSelectThesis(thesis.id)} // Existing route usage
                onExport={handleExport}
                onDelete={handleDeleteThesis}
                // 4) Pass our new "select thesis" method to each card
                // onSelect={() => handleSelectThesis(thesis.id)}
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
      <button className="danger" onClick={() => onDelete(thesis.id)}>
        Delete
      </button>
      {/* 5) A new "Select" button that sets the active thesis in context */}
      {/* <button onClick={onSelect}>Select Active</button> */}
    </div>
  </div>
);

export default ManageThesis;
