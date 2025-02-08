import React, { useState, useEffect } from "react";
import SplitPane, { Pane } from "split-pane-react";
import "../styles/SplitPane.css";
import apiClient from "../services/apiClient";
import { useParams } from "react-router-dom";
import { debounce } from "lodash";

const ThesisDashboard = () => {
    const { thesisId } = useParams();
    const [sizes, setSizes] = useState(["50%", "50%"]);
    const [thesis, setThesis] = useState({});
    const [localThesis, setLocalThesis] = useState({});
    const [formattedContent, setFormattedContent] = useState("");
    const [error, setError] = useState("");

    // Fetch Thesis Details
    useEffect(() => {
        fetchThesis();
    }, [thesisId]);

    const fetchThesis = async () => {
        try {
            const response = await apiClient.get(`/thesis/${thesisId}`);
            setThesis(response.data.thesis);
            setLocalThesis(response.data.thesis);
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

    const updateThesisSection = debounce(async (section, value) => {
        try {
            const data = { [section]: value };
            await apiClient.put(`/thesis/${thesisId}`, data);
            setThesis((prev) => ({ ...prev, ...data }));
            generateLivePreview({ ...localThesis, ...data });
            console.log(`Successfully updated ${section}`);
        } catch (error) {
            setError(`Failed to update ${section}. Please try again.`);
            console.error(error);
        }
    }, 300);

    const updateBodyPage = debounce(async (pageId, value) => {
        try {
            await apiClient.put(`/thesis/${thesisId}/body-pages/${pageId}`, { body: value });
            const updatedPages = localThesis.bodyPages.map((page) =>
                page.id === pageId ? { ...page, body: value } : page
            );
            setLocalThesis((prev) => ({ ...prev, bodyPages: updatedPages }));
            generateLivePreview({ ...localThesis, bodyPages: updatedPages });
            console.log(`Successfully updated body page ${pageId}`);
        } catch (error) {
            setError("Failed to update body page. Please try again.");
            console.error(error);
        }
    }, 300);

    const generateLivePreview = (data) => {
        const title = data.title
            ? `<h1 style="text-align: center; font-weight: bold; text-transform: capitalize; margin-bottom: 24px;">
                ${data.title}
               </h1>`
            : "";

        const abstract = data.abstract
            ? `<h2 style="text-align: center; font-weight: bold; margin-bottom: 12px;">Abstract</h2>
               <p style="text-align: justify; margin: 0; line-height: 2;">
                ${data.abstract}
               </p>`
            : "";

        const tableOfContents = data.tableOfContents
            ? `<h2 style="text-align: center; font-weight: bold; margin-bottom: 12px;">Table of Contents</h2>
               <ul style="list-style-type: none; padding: 0; margin: 0;">
                ${data.tableOfContents
                .sort((a, b) => a.order - b.order)
                .map(
                    (entry) => `<li style="margin: 4px 0;">
                            ${entry.order}. ${entry.sectionTitle} (Page ${entry.pageNumber})
                        </li>`
                )
                .join("")}
               </ul>`
            : "";

        const bodyPages = data.bodyPages
            ? data.bodyPages
                .sort((a, b) => a.pageNumber - b.pageNumber)
                .map(
                    (page) => `<div style="margin-top: 24px;">
                          <h3 style="text-align: left; font-weight: bold; margin-bottom: 12px;">
                            Page ${page.pageNumber}
                          </h3>
                          <p style="text-align: justify; margin: 0; line-height: 2; text-indent: 0.5in;">
                            ${page.body}
                          </p>
                      </div>`
                )
                .join("")
            : "";

        const previewContent = `
            <div style="font-family: 'Times New Roman', serif; font-size: 12pt; line-height: 2; padding: 20px;">
                ${title}
                ${abstract}
                ${tableOfContents}
                ${bodyPages}
            </div>
        `;

        setFormattedContent(previewContent);
    };

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
        <div style={{ height: "100vh", overflow: "hidden", background: "#fafafa" }}>
            {error && <p style={{ color: "red", textAlign: "center" }}>{error}</p>}
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
                                value={localThesis.title || ""}
                                style={inputStyle}
                                onChange={(e) => {
                                    const newValue = e.target.value;
                                    setLocalThesis((prev) => ({
                                        ...prev,
                                        title: newValue,
                                    }));
                                    updateThesisSection("title", newValue);
                                }}
                            />
                        </div>
                        <div style={inputGroupStyle}>
                            <h3>Abstract</h3>
                            <textarea
                                placeholder="Abstract"
                                value={localThesis.abstract || ""}
                                style={textareaStyle}
                                onChange={(e) => {
                                    const newValue = e.target.value;
                                    setLocalThesis((prev) => ({
                                        ...prev,
                                        abstract: newValue,
                                    }));
                                    updateThesisSection("abstract", newValue);
                                }}
                            />
                        </div>

                        <div style={inputGroupStyle}>
                            <h3>Body Pages</h3>
                            {localThesis.bodyPages?.map((page) => (
                                <div key={page.id} style={{ marginBottom: "12px" }}>
                                    <h4>Page {page.pageNumber}</h4>
                                    <textarea
                                        placeholder={`Content for Page ${page.pageNumber}`}
                                        value={page.body || ""}
                                        style={textareaStyle}
                                        onChange={(e) => {
                                            const newValue = e.target.value;
                                            updateBodyPage(page.id, newValue);
                                        }}
                                    />
                                </div>
                            ))}
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
                            dangerouslySetInnerHTML={{ __html: formattedContent }}
                            style={livePreviewStyle}
                        ></div>
                    </div>
                </Pane>
            </SplitPane>
        </div>
    );
};
// Styles
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