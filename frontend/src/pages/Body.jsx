import React, { useState } from "react";
import { Link } from "react-router-dom";
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap/dist/js/bootstrap.bundle.min.js";
import FadingBanner from "../components/FadingBanner";

const Body = () => {
    // State to manage the selected section and its content
    const [selectedSection, setSelectedSection] = useState("Literature Review");
    const [sectionContent, setSectionContent] = useState({
        "Literature Review":
            "The literature review is a critical analysis of the existing research on the topic of the dissertation. It provides an overview of the key findings and debates in the field. The literature review helps to situate the research within the broader context of the discipline and identify gaps in the existing research that the dissertation aims to address.",
        Methodology:
            "The methodology section outlines the research methods used in the study. It describes how the data was collected, analyzed, and interpreted.",
        Results:
            "The results section presents the findings of the study. It provides a detailed summary of the data, including tables, graphs, and statistical analyses.",
        Discussion:
            "The discussion section interprets the results of the study. It explains the significance of the findings and how they relate to the research questions and objectives.",
        Conclusion:
            "The conclusion section summarizes the main findings of the study and provides recommendations for future research.",
    });

    // Handler to change the selected section
    const handleSectionChange = (section) => {
        setSelectedSection(section);
    };

    // Handler to update the section content as the user types
    const handleContentChange = (event) => {
        setSectionContent({
            ...sectionContent,
            [selectedSection]: event.target.value,
        });
    };

    return (
        <div className="container">
            <div className="col-md-12">
                <h3 className="flex text-center">{selectedSection}</h3>
                <div className="row">
                    {/* Sidebar with Links */}
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

                    {/* Textarea for Editing */}
                    <div className="col-md-5 border">
            <textarea
                className="form-control"
                style={{ height: "200px" }}
                value={sectionContent[selectedSection]}
                onChange={handleContentChange}
            />
                    </div>

                    {/* Display Screen */}
                    <div className="col-md-5 border display-screen">
                        <h4>{selectedSection}</h4>
                        <p>{sectionContent[selectedSection]}</p>
                    </div>
                </div>
            </div>

            {/* Fading Banner */}
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

export default Body;