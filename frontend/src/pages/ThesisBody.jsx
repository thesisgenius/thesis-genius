import React, { useState } from "react";
import { Link } from "react-router-dom";
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap/dist/js/bootstrap.bundle.min.js";
import ReactQuill from "react-quill";
import "react-quill/dist/quill.snow.css"; // Import Quill's CSS
import FadingBanner from "../components/FadingBanner";

const ThesisBody = () => {
  // State for selected section and content
  const [selectedSection, setSelectedSection] = useState(
    "Chapter I: Introduction"
  );
  const [sectionContent, setSectionContent] = useState({
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
  });

  // Function to change selected section
  const handleSectionChange = (section) => {
    setSelectedSection(section);
  };

  // Function to update content dynamically
  const handleContentChange = (value) => {
    setSectionContent({
      ...sectionContent,
      [selectedSection]: value, // Store HTML content
    });
  };

  return (
    <div className="container">
      <div className="col-md-12">
        <h3 className="flex">{selectedSection}</h3>
        <div className="row">
          {/* Sidebar Navigation */}
          <div className="col-md-2">
            <ul className="list-group">
              {Object.keys(sectionContent).map((section) => (
                <li
                  key={section}
                  className="list-group-item"
                  onClick={() => handleSectionChange(section)}
                  style={{
                    cursor: "pointer",
                    backgroundColor:
                      selectedSection === section ? "#e9ecef" : "white",
                  }}
                >
                  {section}
                </li>
              ))}
            </ul>
          </div>

          {/* Rich Text Editor */}
          <div className="col-md-5 border">
            <ReactQuill
              theme="snow"
              value={sectionContent[selectedSection]}
              onChange={handleContentChange}
              modules={{
                toolbar: [
                  [{ header: [1, 2, 3, false] }],
                  ["bold", "italic", "underline"],
                  [{ list: "ordered" }, { list: "bullet" }],
                  ["blockquote", "code-block"],
                  ["link", "image"], // Allows inserting images
                  ["clean"], // Clears formatting
                ],
              }}
            />
          </div>

          {/* Display Screen (Renders HTML Content) */}
          <div className="col-md-5 border display-screen">
            <h4>{selectedSection}</h4>
            <div
              dangerouslySetInnerHTML={{
                __html: sectionContent[selectedSection],
              }}
            />
          </div>
        </div>
      </div>

      {/* Fading Banner */}
      <div className="row">
        <FadingBanner />
      </div>
      <div className="col-md-2">
        <Link to="/dashboard" className="btn btn-primary mb-3">
          Back to Dashboard
        </Link>
      </div>
    </div>
  );
};

export default ThesisBody;
