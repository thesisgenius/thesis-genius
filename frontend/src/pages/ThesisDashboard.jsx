import React, { useState, useEffect } from "react";
import SplitPane, { Pane } from "split-pane-react";
import "../styles/SplitPane.css";
import apiClient from "../services/apiClient";
import { useParams } from "react-router-dom";

const ThesisDashboard = () => {
    const { thesisId } = useParams();
    const [sizes, setSizes] = useState(["50%", "50%"]);
    const [thesis, setThesis] = useState({});
    const [formattedContent, setFormattedContent] = useState("");

    // Fetch Thesis Details
    useEffect(() => {
        fetchThesis();
    }, [thesisId]);

    const fetchThesis = async () => {
        try {
            const response = await apiClient.get(`/thesis/${thesisId}`);
            setThesis(response.data.thesis);
            generateLivePreview(response.data.thesis);
        } catch (error) {
            console.error("Error fetching thesis:", error.response || error.message);
            if (error.response?.status === 404) {
                alert("Thesis not found!");
            } else {
                alert("An error occurred while fetching the thesis.");
            }
        }
    };

    const updateThesisSection = async (section, value) => {
        try {
            const data = { [section]: value };
            await apiClient.put(`/thesis/${thesisId}`, data);
            setThesis((prev) => ({ ...prev, ...data }));
            generateLivePreview({ ...thesis, ...data });
            console.log(`Successfully updated ${section}`);
        } catch (error) {
            console.error(`Error updating ${section}:`, error);
        }
    };

    const generateLivePreview = (data) => {
        const title = data.title
            ? `<h1 style="text-align: center; font-weight: bold; text-transform: capitalize; margin-bottom: 24px;">
            ${data.title}
           </h1>`
            : "";

        const abstract = data.abstract
            ? `<h2 style="text-align: center; font-weight: bold; margin-bottom: 12px;">Abstract</h2>
           <p style="text-align: justify; margin: 0; line-height: 2; text-indent: 0;">
            ${data.abstract}
           </p>`
            : "";

        const content = data.content
            ? `<h2 style="text-align: center; font-weight: bold; margin-top: 24px; margin-bottom: 12px;">Content</h2>
           <p style="text-align: justify; margin: 0; line-height: 2; text-indent: 0.5in;">
            ${data.content}
           </p>`
            : "";

        const apaPreview = `
        <div style="font-family: 'Times New Roman', serif; font-size: 12pt; line-height: 2; padding: 20px;">
            ${title}
            ${abstract}
            ${content}
        </div>
    `;

        setFormattedContent(apaPreview);
    };
    // Custom sash render function
    const sashRender = (index, active) => (
        <div
            className={`sash ${active ? "active" : ""}`}
            style={{
                width: "8px",
                background: active ? "#007acc" : "#ddd",
                cursor: "col-resize",
                transition: "background 0.3s ease",
            }}
        />
    );

    return (
        <div style={{height: "100vh", overflow: "hidden", background: "#fafafa"}}>
            <SplitPane
                split="vertical"
                sizes={sizes}
                onChange={setSizes}
                sashRender={sashRender}
            >
                {/* Left Pane: Editor */}
                <Pane>
                    <div style={editorPaneStyle}>
                        <h2>Edit Thesis Sections</h2>
                        <div style={inputGroupStyle}>
                            <h3>Title</h3>
                            <input
                                type="text"
                                placeholder="Title"
                                value={thesis.title || ""}
                                style={inputStyle}
                                onChange={(e) =>
                                    updateThesisSection("title", e.target.value)
                                }
                            />
                        </div>
                        <div style={inputGroupStyle}>
                            <h3>Abstract</h3>
                            <textarea
                                placeholder="Abstract"
                                value={thesis.abstract || ""}
                                style={textareaStyle}
                                onChange={(e) =>
                                    updateThesisSection("abstract", e.target.value)
                                }
                            />
                        </div>
                        <div style={inputGroupStyle}>
                            <h3>Content</h3>
                            <textarea
                                placeholder="Content"
                                value={thesis.content || ""}
                                style={textareaStyle}
                                onChange={(e) =>
                                    updateThesisSection("content", e.target.value)
                                }
                            />
                        </div>
                        <button style={buttonStyle} onClick={fetchThesis}>
                            Refresh Preview
                        </button>
                    </div>
                </Pane>

                {/* Right Pane: APA Preview */}
                <Pane>
                    <div style={previewPaneStyle}>
                        <h2>APA Formatted Preview</h2>
                        <div
                            dangerouslySetInnerHTML={{__html: formattedContent}}
                            style={livePreviewStyle}
                        ></div>
                    </div>
                </Pane>
            </SplitPane>
        </div>
    );
};

const editorPaneStyle = {
    padding: "20px",
    background: "#f4f4f4",
    height: "100%",
    overflowY: "auto",
};

const previewPaneStyle = {
    padding: "20px",
    background: "#ffffff",
    height: "100%",
    overflowY: "auto",
    textAlign: "left",
};

const inputGroupStyle = {
    marginBottom: "20px",
};

const inputStyle = {
    width: "100%",
    padding: "10px",
    fontSize: "16px",
    border: "1px solid #ccc",
    borderRadius: "4px",
};

const textareaStyle = {
    width: "100%",
    height: "150px",
    padding: "10px",
    fontSize: "16px",
    border: "1px solid #ccc",
    borderRadius: "4px",
    resize: "vertical",
};

const buttonStyle = {
    padding: "10px 20px",
    fontSize: "16px",
    color: "#fff",
    backgroundColor: "#007acc",
    border: "none",
    borderRadius: "4px",
    cursor: "pointer",
    marginTop: "20px",
};

const livePreviewStyle = {
    height: "100%",
    overflowY: "auto",
    padding: "20px",
    backgroundColor: "#fff",
    border: "1px solid #ddd",
    borderRadius: "4px",
};

export default ThesisDashboard;
