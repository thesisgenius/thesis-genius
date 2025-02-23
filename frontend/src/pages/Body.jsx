import React, { useState } from "react";
import { Link } from "react-router-dom";
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap/dist/js/bootstrap.bundle.min.js";
import FadingBanner from "../components/FadingBanner";

// Constants
const INITIAL_SECTIONS = {
  "Chapter I: Introduction":
      "This is where the introduction content of the thesis will go...",
  "Chapter II: Literature Review":
      "The literature review is a critical analysis of the existing research on the topic of the dissertation. It provides an overview of the key findings and debates in the field. The literature review helps to situate the research within the broader context of the discipline and identify gaps in the existing research that the dissertation aims to address.",
  "Chapter III: Methods":
      "The methodology section outlines the research methods used in the study. It describes how the data was collected, analyzed, and interpreted.",
  "Chapter IV: Results":
      "The results section presents the findings of the study. It provides a detailed summary of the data, including tables, graphs, and statistical analyses.",
  "Chapter V: Discussion":
      "The discussion section interprets the results of the study. It explains the significance of the findings and how they relate to the research questions and objectives.",
};

// Shared Styles
const sidebarLinkStyles = {
  cursor: "pointer",
};

const Body = () => {
  // State
  const [activeSection, setActiveSection] = useState("Chapter II: Literature Review");
  const [sectionContent, setSectionContent] = useState(INITIAL_SECTIONS);

  // Handlers
  const onSectionChange = (newSection) => setActiveSection(newSection);

  const onContentChange = (event) => {
    setSectionContent((prevContent) => ({
      ...prevContent,
      [activeSection]: event.target.value,
    }));
  };

  // Helper Functions
  const renderSidebarLinks = () =>
      Object.keys(sectionContent).map((section) => (
          <li
              key={section}
              className="list-group-item"
              onClick={() => onSectionChange(section)}
              style={{
                ...sidebarLinkStyles,
                backgroundColor: activeSection === section ? "#e9ecef" : "white",
              }}
          >
            {section}
          </li>
      ));

  return (
      <div className="container">
        <div className="col-md-12">
          <h3 className="text-center">{activeSection}</h3>
          <div className="row">
            {/* Sidebar */}
            <div className="col-md-2">
              <ul className="list-group">{renderSidebarLinks()}</ul>
            </div>
            {/* Textarea Editor */}
            <div className="col-md-5 border">
            <textarea
                className="form-control"
                style={{ height: "200px" }}
                value={sectionContent[activeSection]}
                onChange={onContentChange}
            />
            </div>
            {/* Display Section */}
            <div className="col-md-5 border">
              <h4>{activeSection}</h4>
              <p>{sectionContent[activeSection]}</p>
            </div>
          </div>
        </div>
        {/* Fading Banner */}
        <div className="row">
          <FadingBanner />
        </div>
        {/* Dashboard Link */}
        <div className="col-md-2">
          <Link to="/dashboard" className="btn btn-primary mb-3">
            Back to Dashboard
          </Link>
        </div>
      </div>
  );
};

export default Body;