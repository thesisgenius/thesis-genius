import { useState, useEffect, useCallback } from "react";
import SplitPane, { Pane } from "split-pane-react";
import { useParams } from "react-router-dom";
import { debounce } from "lodash";
import DOMPurify from "dompurify";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faFile, faBook, faSyncAlt } from "@fortawesome/free-solid-svg-icons";
import thesisAPI from "../services/thesisEndpoint";
import "../styles/SplitPane.css";
import "../styles/apaStyle.css";

const SECTIONS = [
  { name: "Cover Page", icon: faFile },
  { name: "Table Of Contents", icon: faBook },
  { name: "Abstract", icon: faFile },
  { name: "Body", icon: faBook },
  { name: "Acknowledgements", icon: faFile },
  { name: "References", icon: faBook },
  { name: "Bibliography", icon: faBook },
  { name: "Footnote", icon: faFile },
  { name: "Figure", icon: faBook },
  { name: "Appendix", icon: faFile },
];

const ThesisDashboard = () => {
  const { thesisId } = useParams();
  const [sizes, setSizes] = useState(["20%", "40%", "40%"]);
  const [thesis, setThesis] = useState({});
  const [abstract, setAbstract] = useState("");
  const [bodyPages, setBodyPages] = useState([]);
  const [error, setError] = useState("");
  const [tableOfContents, setTableOfContents] = useState([]);
  const [coverPage, setCoverPage] = useState({
    title: "[Title of thesis]",
    author: "[Author's name]",
    affiliation: "[Affiliation of author]",
    course: "[Course of study]",
    instructor: "[Instructor's name]",
    due_date: new Date(
      new Date().getFullYear(),
      new Date().getMonth(),
      new Date().getDate() + 10,
    ),
  });
  const [formattedContent, setFormattedContent] = useState("");
  const [selectedSection, setSelectedSection] = useState("Cover Page");

  useEffect(() => {
    fetchThesis();
  }, [thesisId]);

  const fetchThesis = async () => {
    try {
      const thesisData = await thesisAPI.getThesis(thesisId);
      setThesis(thesisData.thesis);

      try {
        const tocData = await thesisAPI.getTableOfContents(thesisId);
        setTableOfContents(tocData || []);
      } catch (error) {
        console.error("Failed to fetch TOC:", error);
      }

      try {
        const coverData = await thesisAPI.getCoverPage(thesisId);
        setCoverPage(coverData || {});
      } catch (error) {
        console.error("Failed to fetch cover page:", error);
        setCoverPage({
          title: "[Title of thesis]",
          author: "[Author's name]",
          affiliation: "[Affiliation of author]",
          course: "[Course of study]",
          instructor: "[Instructor's name]",
          due_date: new Date(
            new Date().getFullYear(),
            new Date().getMonth(),
            new Date().getDate() + 10,
          ),
        });
      }

      try {
        const abstractData = await thesisAPI.getAbstract(thesisId);
        setAbstract(abstractData.abstract || "");
      } catch (error) {
        console.error("Failed to fetch abstract:", error);
        setAbstract("");
      }

      try {
        let bodyPagesData = await thesisAPI.getBodyPages(thesisId);

        // Ensure at least one blank page is always present
        if (!bodyPagesData || bodyPagesData.length === 0) {
          console.warn("No body pages found, adding a blank page.");
          bodyPagesData = [
            {
              page_number: 1,
              body: "(This page is intentionally left blank.)",
            },
          ];
        }

        setBodyPages(bodyPagesData);
      } catch (error) {
        console.error(
          "Failed to fetch body pages:",
          error.response?.data || error.message,
        );
        setBodyPages([
          { page_number: 1, body: "(This page is intentionally left blank.)" },
        ]);
      }

      generateLivePreview(thesisData.thesis, coverPage, abstract, bodyPages);
    } catch (error) {
      console.error("Error fetching thesis:", error);
      setError("An error occurred while fetching thesis data.");
    }
  };

  const handleCoverPageChange = (field, value) => {
    setCoverPage((prev) => ({ ...prev, [field]: value }));
    updateCoverPage(field, value); // Debounced API update
  };

  const updateCoverPage = useCallback(
    debounce(async (field, value) => {
      try {
        await thesisAPI.updateCoverPage(thesisId, { [field]: value });
        console.log(`Cover page ${field} updated successfully`);
      } catch (error) {
        setError(`Failed to update cover page ${field}.`);
        console.error(`Error updating cover page ${field}:`, error);
      }
    }, 500),
    [thesisId],
  );

  // Debounced API update for Table of Contents
  const updateTOC = debounce(async (updatedTOC) => {
    try {
      await thesisAPI.updateTableOfContents(thesisId, updatedTOC);
      console.log("TOC updated successfully");
    } catch (error) {
      console.error("Error updating TOC:", error);
    }
  }, 500);

  // React callback for handling state updates
  const handleTOCChange = useCallback(
    (index, field, value) => {
      // Create a new array to ensure immutability
      const updatedTOC = [...tableOfContents];

      // Update the specific field for the relevant TOC entry
      updatedTOC[index][field] = value;

      // Update state immediately to reflect changes in the UI
      setTableOfContents(updatedTOC);

      // Call the debounced API update function
      updateTOC(updatedTOC);
    },
    [tableOfContents], // Include dependencies like `tableOfContents`
  );

  // Debounced update function
  const updateAbstract = debounce(async (value) => {
    try {
      await thesisAPI.updateAbstract(thesisId, { text: value });
      generateLivePreview(thesis, value, bodyPages); // Ensure the live preview gets updated
      console.log("Abstract updated successfully");
    } catch (error) {
      setError("Failed to update abstract.");
      console.error("Error updating abstract:", error);
    }
  }, 500);

  // React callback for input handling
  const handleAbstractChange = useCallback(
    (e) => {
      const newValue = e.target.value;

      // Update the state immediately for a responsive UI
      setAbstract(newValue);

      // Call the debounced API update function
      updateAbstract(newValue);
    },
    [updateAbstract], // Include debounce function or dependencies if necessary
  );

  const handleAddBodyPage = async (thesisId) => {
    try {
      // Determine the next page number
      const nextPageNumber =
        bodyPages.length > 0
          ? Math.max(...bodyPages.map((p) => p.page_number)) + 1
          : 1;

      // Add page to the backend
      const newPage = await thesisAPI.addBodyPage(thesisId, {
        page_number: nextPageNumber,
        body: "",
      });

      // Update UI state
      setBodyPages((prev) => [
        ...prev,
        { id: newPage.page_id, page_number: nextPageNumber, body: "" },
      ]);
    } catch (error) {
      setError("Failed to add a new body page.");
      console.error("Error adding new body page:", error);
    }
  };

  const handleDeleteBodyPage = async (thesisId, pageId) => {
    try {
      await thesisAPI.deleteBodyPage(thesisId, pageId);
      setBodyPages((prev) => prev.filter((page) => page.id !== pageId));
    } catch (error) {
      setError("Failed to delete body page.");
      console.error("Error deleting body page:", error);
    }
  };

  const handleBodyPageChange = (thesisId, pageId, newValue) => {
    // Update UI immediately for better user experience
    setBodyPages((prev) =>
      prev.map((page) =>
        page.id === pageId ? { ...page, body: newValue } : page,
      ),
    );

    // Debounced API update
    updateBodyPage(thesisId, pageId, newValue);
  };

  const updateBodyPage = debounce(async (thesisId, pageId, value) => {
    try {
      await thesisAPI.updateBodyPage(thesisId, pageId, { body: value });
      console.log(`Page ${pageId} in Thesis ${thesisId} updated successfully`);
    } catch (error) {
      setError("Failed to update body page."); // Ensure setError is declared elsewhere
      console.error(
        `Error updating page ${pageId} in Thesis ${thesisId}:`,
        error,
      );
    }
  }, 500);

  /** Ensure preview updates correctly */
  const generateLivePreview = (
    thesisData,
    coverPageData,
    abstractData,
    bodyPagesData,
  ) => {
    let pageNumber = 1;
    const totalPages =
      1 + (abstractData ? 1 : 0) + (bodyPagesData.length || 1) + 1; // Total pages excluding cover

    // Cover Page
    const coverPage = `
            <div id="cover-page" class="apa-cover-page">
                <div class="apa-header">Running head: ${coverPageData.title?.toUpperCase()}</div>
                <h1 class="apa-title">${coverPageData.title}</h1>
                <p class="apa-cover-author">${coverPageData.author}</p>
                <p class="apa-cover-affiliation">${coverPageData.affiliation}</p>
                <p class="apa-cover-course">${coverPageData.course}</p>
                <p class="apa-cover-instructor">${coverPageData.instructor}</p>
                <p class="apa-cover-date">${coverPageData.due_date}</p>
                <span class="apa-page-number">Page ${pageNumber++} of ${totalPages}</span>
            </div>
        `;

    // Table of Contents (excluding Cover Page)
    const tocSection = `
        <div id="table-of-contents" class="apa-page">
            <div class="apa-header">${coverPageData.title?.toUpperCase()}</div>
            <h2 class="apa-heading-1">Table of Contents</h2>
            
            <div class="apa-toc">
                ${tableOfContents
                  .filter((entry) => entry.section_title !== "Cover Page") // Exclude Cover Page
                  .map(
                    (entry) => `
                        <p class="apa-toc-entry">
                            <span class="apa-toc-title">${entry.section_title}</span>
                            <span class="apa-toc-dots"> ................................................................ </span>
                            <span class="apa-toc-page">${entry.page_number}</span>
                        </p>
                    `,
                  )
                  .join("")}
            </div>

            <span class="apa-page-number">Page ${pageNumber++} of ${totalPages}</span>
        </div>
    `;

    // Abstract Page
    const abstractSection = abstractData
      ? `
            <div id="abstract" class="apa-page">
                <div class="apa-header">${coverPageData.title?.toUpperCase()}</div>
                <h2 class="apa-heading-1">Abstract</h2>
                <p class="apa-abstract">${abstractData}</p>
                <span class="apa-page-number">Page ${pageNumber++} of ${totalPages}</span>
            </div>
        `
      : "";

    // Body Pages with Page Breaks
    const bodySections = bodyPagesData
      .map(
        (page) => `
            <div id="body-page-${page.page_number}" class="apa-page">
                <div class="apa-header">${coverPageData.title?.toUpperCase()}</div>
                <h3 class="apa-heading-2">Page ${page.page_number}</h3>
                <p class="apa-paragraph">${page.body}</p>
                <span class="apa-page-number">Page ${pageNumber++} of ${totalPages}</span>
            </div>
        `,
      )
      .join("");

    // Reference Section
    const references = `
            <div id="references" class="apa-page">
                <div class="apa-header">${coverPageData.title?.toUpperCase()}</div>
                <h2 class="apa-heading-1">References</h2>
                <span class="apa-page-number">Page ${pageNumber++} of ${totalPages}</span>
            </div>
        `;

    // Combine all sections
    const previewContent = `
        <div class="apa-document">
            ${coverPage}
            ${tocSection}
            ${abstractSection}
            ${bodySections}
            ${references}
        </div>
    `;

    setFormattedContent(DOMPurify.sanitize(previewContent));
  };

  // Map section names to corresponding element IDs in the preview pane
  const handleNavigationClick = (section) => {
    setSelectedSection(section.name); // Adjust since SECTIONS now includes icons
    const sectionIdMap = {
      "Table Of Contents": "table-of-contents",
      Abstract: "abstract",
      Body: "body-page-1",
      References: "references",
    };
    const targetElementId =
      sectionIdMap[section.name] ||
      `body-page-${section.name.replace(/\D/g, "")}`;
    const targetElement = document.getElementById(targetElementId);
    if (targetElement) {
      targetElement.scrollIntoView({ behavior: "smooth", block: "start" });
    }
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
        {/* Leftmost Pane: Navigation Sidebar */}
        <Pane>
          <div style={sidebarStyle}>
            <h3>Thesis Sections</h3>
            <ul style={navListStyle}>
              {SECTIONS.map((section) => (
                <li
                  key={section.name}
                  style={
                    selectedSection === section.name
                      ? navItemActive
                      : navItemStyle
                  }
                  onClick={() => handleNavigationClick(section)}
                >
                  <FontAwesomeIcon
                    icon={section.icon}
                    style={{ marginRight: "10px" }}
                  />
                  {section.name}
                </li>
              ))}
            </ul>
          </div>
        </Pane>

        {/* Middle Pane: Editor */}
        <Pane>
          <div style={editorPaneStyle}>
            <h2>Edit {selectedSection}</h2>

            {selectedSection === "Table Of Contents" && (
              <div style={inputGroupStyle}>
                <h3>Table of Contents</h3>
                {tableOfContents.map((entry, index) => (
                  <div key={index}>
                    <input
                      type="text"
                      value={entry.section_title}
                      style={inputStyle}
                      onChange={(e) =>
                        handleTOCChange(index, "section_title", e.target.value)
                      }
                    />
                    <input
                      type="number"
                      value={entry.page_number}
                      style={inputStyle}
                      onChange={(e) =>
                        handleTOCChange(
                          index,
                          "page_number",
                          Number(e.target.value),
                        )
                      }
                    />
                  </div>
                ))}
              </div>
            )}

            {selectedSection === "Cover Page" && (
              <div style={inputGroupStyle}>
                <h3>Cover Page</h3>

                <label>Title:</label>
                <input
                  type="text"
                  value={coverPage.title || ""}
                  style={inputStyle}
                  onChange={(e) =>
                    handleCoverPageChange("title", e.target.value)
                  }
                />

                <label>Author:</label>
                <input
                  type="text"
                  value={coverPage.author || ""}
                  style={inputStyle}
                  onChange={(e) =>
                    handleCoverPageChange("author", e.target.value)
                  }
                />

                <label>Affiliation:</label>
                <input
                  type="text"
                  value={coverPage.affiliation || ""}
                  style={inputStyle}
                  onChange={(e) =>
                    handleCoverPageChange("affiliation", e.target.value)
                  }
                />

                <label>Course:</label>
                <input
                  type="text"
                  value={coverPage.course || ""}
                  style={inputStyle}
                  onChange={(e) =>
                    handleCoverPageChange("course", e.target.value)
                  }
                />

                <label>Instructor:</label>
                <input
                  type="text"
                  value={coverPage.instructor || ""}
                  style={inputStyle}
                  onChange={(e) =>
                    handleCoverPageChange("instructor", e.target.value)
                  }
                />

                <label>Due Date:</label>
                <input
                  type="date"
                  value={coverPage.due_date || ""}
                  style={inputStyle}
                  onChange={(e) =>
                    handleCoverPageChange("due_date", e.target.value)
                  }
                />
              </div>
            )}

            {selectedSection === "Abstract" && (
              <div style={inputGroupStyle}>
                <h3>Abstract</h3>
                <textarea
                  placeholder="Enter Abstract"
                  value={abstract}
                  style={textareaStyle}
                  onChange={handleAbstractChange}
                />
              </div>
            )}

            {selectedSection === "Body" && (
              <div style={inputGroupStyle}>
                <h3>Body Pages</h3>

                {bodyPages.map((page, index) => (
                  <div key={page.id || index} style={{ marginBottom: "12px" }}>
                    <h4>Page {page.page_number}</h4>
                    <textarea
                      placeholder={`Edit content for Page ${page.page_number}`}
                      value={page.body || ""}
                      style={textareaStyle}
                      onChange={(e) =>
                        handleBodyPageChange(thesisId, page.id, e.target.value)
                      }
                    />
                    <button
                      style={deleteButtonStyle}
                      onClick={() => handleDeleteBodyPage(thesisId, page.id)}
                    >
                      Delete Page
                    </button>
                  </div>
                ))}

                {/* Add New Page Button */}
                <button
                  style={addButtonStyle}
                  onClick={() => handleAddBodyPage(thesisId)}
                >
                  + Add New Page
                </button>
              </div>
            )}

            <button style={buttonStyle} onClick={fetchThesis}>
              <FontAwesomeIcon
                icon={faSyncAlt}
                style={{ marginRight: "5px" }}
              />
              Refresh Preview
            </button>
          </div>
        </Pane>

        {/* Rightmost Pane: Live Preview */}
        <Pane>
          <div style={previewPaneStyle}>
            <h2>APA Formatted Preview</h2>
            <div
              className="apa-document"
              dangerouslySetInnerHTML={{ __html: formattedContent }}
            ></div>
          </div>
        </Pane>
      </SplitPane>
    </div>
  );
};

// Sidebar Styles
const sidebarStyle = {
  padding: "20px",
  background: "#2c3e50",
  height: "100%",
  color: "#fff",
  overflowY: "auto",
};
const navListStyle = { listStyle: "none", padding: 0, margin: 0 };
const navItemStyle = {
  padding: "10px",
  cursor: "pointer",
  borderBottom: "1px solid rgba(255, 255, 255, 0.2)",
};
const navItemActive = { ...navItemStyle, backgroundColor: "#34495e" };

// Editor & Preview Styles
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

// Input & Button Styles
const inputStyle = {
  width: "100%",
  padding: "10px",
  fontSize: "16px",
  border: "1px solid #ccc",
  borderRadius: "4px",
};
const inputGroupStyle = {
  marginBottom: "20px",
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
const addButtonStyle = {
  padding: "10px 15px",
  fontSize: "14px",
  color: "#fff",
  backgroundColor: "#007acc",
  border: "none",
  borderRadius: "4px",
  cursor: "pointer",
  marginTop: "10px",
  marginLeft: "auto", // Push the button to the right in a flex container
  display: "inline-block", // Ensures proper alignment as an inline block element
};
const deleteButtonStyle = {
  padding: "6px 12px",
  fontSize: "12px",
  color: "#fff",
  backgroundColor: "#cc0000",
  border: "none",
  borderRadius: "4px",
  cursor: "pointer",
  marginLeft: "auto", // Push the button to the right in a flex container
  display: "inline-block", // Ensures proper alignment as an inline block element
};

export default ThesisDashboard;
