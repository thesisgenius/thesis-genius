import React, { useState } from "react";
import { Link } from "react-router-dom";
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap/dist/js/bootstrap.bundle.min.js";
import ReactQuill from "react-quill";
import "react-quill/dist/quill.snow.css"; // Import Quill's CSS
import FadingBanner from "../components/FadingBanner";

const DynamicPart = ({ headerText, sections }) => {
  const [selectedSection, setSelectedSection] = useState(sections[0].title); // Default to first section
  const [sectionContent, setSectionContent] = useState(
    sections.reduce((acc, section) => {
      acc[section.title] = section.content || "";
      return acc;
    }, {})
  );

  // Handle section change
  const handleSectionChange = (section) => {
    setSelectedSection(section);
  };

  // Handle content change
  const handleContentChange = (value) => {
    setSectionContent((prevContent) => ({
      ...prevContent,
      [selectedSection]: value,
    }));
  };

  return (
    <div className="container">
      <div className="col-md-12">
        <h3 className="flex text-center">{headerText}</h3>
        <p>
          An attached example{" "}
          <a
            href="https://apastyle.apa.org/instructional-aids/abstract-keywords-guide.pdf"
            target="_blank"
            rel="noopener noreferrer"
          >
            example linked
          </a>
        </p>
        <p>
          Relevant AP{" "}
          <a
            href="https://apastyle.apa.org/style-grammar-guidelines"
            target="_blank"
            rel="noopener noreferrer"
          >
            Rules Linked
          </a>
        </p>
        <div className="row">
          {/* Sidebar Navigation */}
          <div className="col-md-2">
            <ul className="list-group">
              {sections.map((section) => (
                <li
                  key={section.title}
                  className={`list-group-item ${
                    selectedSection === section.title ? "active" : ""
                  }`}
                  onClick={() => handleSectionChange(section.title)}
                  style={{ cursor: "pointer" }}
                >
                  {section.title}
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
                  ["link", "image"],
                  ["clean"],
                ],
              }}
            />
          </div>

          {/* Live Preview */}
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

      <div className="row">
        <FadingBanner />
      </div>
      <div className="col-md-2">
        <Link to="/dash" className="btn btn-primary mb-3">
          Back to Dashboard
        </Link>
      </div>
    </div>
  );
};

export default DynamicPart;
