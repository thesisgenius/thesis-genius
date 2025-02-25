// Part.jsx
import React, { useState, useEffect, useCallback, useMemo } from "react";
import { Link, useParams } from "react-router-dom";
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap/dist/js/bootstrap.bundle.min.js";
import "react-quill/dist/quill.snow.css";
import "../styles/apaStyle.css";
import { debounce } from "lodash";
import DOMPurify from "dompurify";

import ReactQuill from "react-quill";
import thesisAPI from "../services/thesisEndpoint";

/**
 * Part component for single-page sections (Title, TOC, Abstract, Dedication, etc.).
 *
 *  1) Loads existing content from the backend on mount (depending on headerText),
 *  2) Provides either <input> fields or a Quill editor for user edits,
 *  3) Updates the server via debounced calls,
 *  4) Builds an APA-styled preview in the right column, similar to ThesisDashboard.jsx.
 */
const Part = ({ headerText, textAreaPlaceholder }) => {
  const { thesisId } = useParams();

  // ---------- State for various "parts" ----------
  const [coverPage, setCoverPage] = useState({
    title: "",
    author: "",
    affiliation: "",
    course: "",
    instructor: "",
    due_date: "",
  });

  const [tableOfContents, setTableOfContents] = useState([]);
  const [abstractText, setAbstractText] = useState("");
  const [dedicationText, setDedicationText] = useState("");
  const [listOfFiguresText, setListOfFiguresText] = useState("");
  const [listOfTablesText, setListOfTablesText] = useState("");
  const [appendicesText, setAppendicesText] = useState("");
  const [referencesText, setReferencesText] = useState("");
  const [otherInfoText, setOtherInfoText] = useState("");
  const [signatureText, setSignatureText] = useState("");
  const [copyrightText, setCopyrightText] = useState("");

  // Single Quill text fallback for parts that we handle with a rich-text editor
  // (We will only use this if the part doesn't have a special state set up.)
  const [genericText, setGenericText] = useState("");

  // For rendering the final APA preview
  const [formattedContent, setFormattedContent] = useState("");

  // Loading & error states
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  // ==============================
  // 1) FETCH data on mount
  // ==============================
  useEffect(() => {
    setLoading(true);
    setError("");

    (async () => {
      try {
        // We'll switch by headerText to load the correct data from the server
        switch (headerText) {
          case "Title Page": {
            const coverData = await thesisAPI.getCoverPage(thesisId);
            setCoverPage({
              title: coverData?.title || "",
              author: coverData?.author || "",
              affiliation: coverData?.affiliation || "",
              course: coverData?.course || "",
              instructor: coverData?.instructor || "",
              // If due_date is a date string, slice(0,10) ensures "YYYY-MM-DD" in <input type="date" />
              due_date: coverData?.due_date?.slice(0, 10) || "",
            });
            break;
          }
          case "Table of Contents Page": {
            const tocData = await thesisAPI.getTableOfContents(thesisId);
            setTableOfContents(tocData || []);
            break;
          }
          case "Abstract Page": {
            const absData = await thesisAPI.getAbstract(thesisId);
            setAbstractText(absData?.abstract || "");
            break;
          }
          case "Dedication Page": {
            const dedData = await thesisAPI.getDedicationPage(thesisId);
            setDedicationText(dedData?.content || "");
            break;
          }
          case "List of Figures Page": {
            const figData = await thesisAPI.getListOfFigures(thesisId);
            setListOfFiguresText(figData?.content || "");
            break;
          }
          case "List of Tables Page": {
            const tablesData = await thesisAPI.getListOfTables(thesisId);
            setListOfTablesText(tablesData?.content || "");
            break;
          }
          case "Appendices Page": {
            const appData = await thesisAPI.getAppendices(thesisId);
            setAppendicesText(appData?.content || "");
            break;
          }
          case "References Page": {
            const refData = await thesisAPI.getReferences(thesisId);
            setReferencesText(refData?.content || "");
            break;
          }
          case "Other Info Page": {
            const otherData = await thesisAPI.getOtherInfo(thesisId);
            setOtherInfoText(otherData?.content || "");
            break;
          }
          case "Signature Page": {
            const sigData = await thesisAPI.getSignaturePage(thesisId);
            setSignatureText(sigData?.content || "");
            break;
          }
          case "Copyright Page": {
            const copyData = await thesisAPI.getCopyrightPage(thesisId);
            setCopyrightText(copyData?.content || "");
            break;
          }
          default:
            // If none of the above, load a "generic" text approach
            console.warn(`No specific load function for part: ${headerText}`);
            setGenericText("");
            break;
        }
      } catch (err) {
        console.error(`Failed to load data for ${headerText}:`, err);
        setError(`Failed to load data for ${headerText}`);
      } finally {
        setLoading(false);
      }
    })();
  }, [headerText, thesisId]);

  // ==============================
  // 2) DEBOUNCED UPDATE functions
  // ==============================
  // --- Cover Page ---
  const updateCoverPage = useCallback(
    debounce(async (field, value) => {
      try {
        await thesisAPI.updateCoverPage(thesisId, { [field]: value });
      } catch (error) {
        console.error("Error updating cover page:", error);
        setError("Failed to update cover page field.");
      }
    }, 500),
    [thesisId],
  );
  const handleCoverPageChange = (field, value) => {
    setCoverPage((prev) => ({ ...prev, [field]: value }));
    updateCoverPage(field, value);
  };

  // --- Table of Contents ---
  const updateTOC = useCallback(
    debounce(async (updatedTOC) => {
      try {
        await thesisAPI.updateTableOfContents(thesisId, updatedTOC);
        console.log("TOC updated successfully");
      } catch (error) {
        console.error("Error updating TOC:", error);
        setError("Failed to update Table of Contents.");
      }
    }, 500),
    [thesisId],
  );
  const handleTOCChange = (index, field, value) => {
    const newToc = [...tableOfContents];
    newToc[index][field] = value;
    setTableOfContents(newToc);
    updateTOC(newToc);
  };

  // --- Abstract ---
  const updateAbstract = useMemo(
    () =>
      debounce(async (newVal) => {
        try {
          await thesisAPI.updateAbstract(thesisId, { text: newVal });
          console.log("Abstract updated");
        } catch (error) {
          console.error("Error updating abstract:", error);
          setError("Failed to update abstract.");
        }
      }, 500),
    [thesisId],
  );
  const handleAbstractChange = (val) => {
    setAbstractText(val);
    updateAbstract(val);
  };

  // --- Dedication ---
  const updateDedication = useMemo(
    () =>
      debounce(async (newVal) => {
        try {
          await thesisAPI.updateDedicationPage(thesisId, { content: newVal });
        } catch (err) {
          console.error("Error updating Dedication Page:", err);
          setError("Failed to update Dedication Page.");
        }
      }, 500),
    [thesisId],
  );
  const handleDedicationChange = (val) => {
    setDedicationText(val);
    updateDedication(val);
  };

  // --- List of Figures ---
  const updateListOfFigures = useMemo(
    () =>
      debounce(async (newVal) => {
        try {
          await thesisAPI.updateListOfFigures(thesisId, { content: newVal });
        } catch (err) {
          console.error("Error updating List of Figures:", err);
          setError("Failed to update List of Figures.");
        }
      }, 500),
    [thesisId],
  );
  const handleListOfFiguresChange = (val) => {
    setListOfFiguresText(val);
    updateListOfFigures(val);
  };

  // --- List of Tables ---
  const updateListOfTables = useMemo(
    () =>
      debounce(async (newVal) => {
        try {
          await thesisAPI.updateListOfTables(thesisId, { content: newVal });
        } catch (err) {
          console.error("Error updating List of Tables:", err);
          setError("Failed to update List of Tables.");
        }
      }, 500),
    [thesisId],
  );
  const handleListOfTablesChange = (val) => {
    setListOfTablesText(val);
    updateListOfTables(val);
  };

  // --- Appendices ---
  const updateAppendices = useMemo(
    () =>
      debounce(async (newVal) => {
        try {
          await thesisAPI.updateAppendices(thesisId, { content: newVal });
        } catch (err) {
          console.error("Error updating Appendices:", err);
          setError("Failed to update Appendices.");
        }
      }, 500),
    [thesisId],
  );
  const handleAppendicesChange = (val) => {
    setAppendicesText(val);
    updateAppendices(val);
  };

  // --- References ---
  const updateReferences = useMemo(
    () =>
      debounce(async (newVal) => {
        try {
          await thesisAPI.updateReferences(thesisId, { content: newVal });
        } catch (err) {
          console.error("Error updating References:", err);
          setError("Failed to update References.");
        }
      }, 500),
    [thesisId],
  );
  const handleReferencesChange = (val) => {
    setReferencesText(val);
    updateReferences(val);
  };

  // --- Other Info ---
  const updateOtherInfo = useMemo(
    () =>
      debounce(async (newVal) => {
        try {
          await thesisAPI.updateOtherInfo(thesisId, { content: newVal });
        } catch (err) {
          console.error("Error updating Other Info:", err);
          setError("Failed to update Other Info.");
        }
      }, 500),
    [thesisId],
  );
  const handleOtherInfoChange = (val) => {
    setOtherInfoText(val);
    updateOtherInfo(val);
  };

  // --- Signature Page ---
  const updateSignaturePage = useMemo(
    () =>
      debounce(async (newVal) => {
        try {
          await thesisAPI.updateSignaturePage(thesisId, { content: newVal });
        } catch (err) {
          console.error("Error updating Signature Page:", err);
          setError("Failed to update Signature Page.");
        }
      }, 500),
    [thesisId],
  );
  const handleSignatureChange = (val) => {
    setSignatureText(val);
    updateSignaturePage(val);
  };

  // --- Copyright Page ---
  const updateCopyrightPage = useMemo(
    () =>
      debounce(async (newVal) => {
        try {
          await thesisAPI.updateCopyrightPage(thesisId, { content: newVal });
        } catch (err) {
          console.error("Error updating Copyright Page:", err);
          setError("Failed to update Copyright Page.");
        }
      }, 500),
    [thesisId],
  );
  const handleCopyrightChange = (val) => {
    setCopyrightText(val);
    copyrightText(val);
  };

  // --- Generic fallback update (if needed) ---
  const updateGenericPart = useMemo(
    () =>
      debounce(async (newVal) => {
        // You could store in some custom endpoint if you'd like,
        // or do nothing if the "default" part doesn't have an API route.
        console.warn("No specific API to update for generic part.");
      }, 500),
    [],
  );
  const handleGenericChange = (val) => {
    setGenericText(val);
    updateGenericPart(val);
  };

  // ==============================
  // 3) APA Preview generation
  // ==============================
  useEffect(() => {
    // We'll build a small snippet for each part, skipping body pages entirely.
    let previewHTML = "";

    // For consistency with ThesisDashboard, we could create an APA header:
    const uppercaseTitle = coverPage.title?.toUpperCase() || "[THESIS TITLE]";
    const heading = `<div class="apa-header">${uppercaseTitle}</div>`;

    switch (headerText) {
      case "Title Page":
        previewHTML = `
          <div class="apa-document">
            <div id="cover-page" class="apa-cover-page">
              <div class="apa-header">Running head: ${uppercaseTitle}</div>
              <h1 class="apa-title">${coverPage.title}</h1>
              <p class="apa-cover-author">${coverPage.author}</p>
              <p class="apa-cover-affiliation">${coverPage.affiliation}</p>
              <p class="apa-cover-course">${coverPage.course}</p>
              <p class="apa-cover-instructor">${coverPage.instructor}</p>
              <p class="apa-cover-date">${coverPage.due_date || ""}</p>
            </div>
          </div>
        `;
        break;

      case "Table of Contents Page":
        // Similar to ThesisDashboard, we’ll iterate tableOfContents array
        previewHTML = `
          <div class="apa-document">
            <div id="table-of-contents" class="apa-page">
              ${heading}
              <h2 class="apa-heading-1">Table of Contents</h2>
              <div class="apa-toc">
                ${tableOfContents
                  .map(
                    (entry) => `
                    <p class="apa-toc-entry">
                      <span class="apa-toc-title">${entry.section_title}</span>
                      <span class="apa-toc-dots">................................................................</span>
                      <span class="apa-toc-page">${entry.page_number || ""}</span>
                    </p>
                  `,
                  )
                  .join("")}
              </div>
            </div>
          </div>
        `;
        break;

      case "Abstract Page":
        previewHTML = `
          <div class="apa-document">
            <div id="abstract" class="apa-page">
              ${heading}
              <h2 class="apa-heading-1">Abstract</h2>
              <p class="apa-abstract">${abstractText}</p>
            </div>
          </div>
        `;
        break;

      case "Dedication Page":
        previewHTML = `
          <div class="apa-document">
            <div id="dedication" class="apa-page">
              ${heading}
              <h2 class="apa-heading-1">Dedication</h2>
              <div class="apa-paragraph">${dedicationText}</div>
            </div>
          </div>
        `;
        break;

      case "List of Figures Page":
        previewHTML = `
          <div class="apa-document">
            <div id="list-of-figures" class="apa-page">
              ${heading}
              <h2 class="apa-heading-1">List of Figures</h2>
              <div class="apa-paragraph">${listOfFiguresText}</div>
            </div>
          </div>
        `;
        break;

      case "List of Tables Page":
        previewHTML = `
          <div class="apa-document">
            <div id="list-of-tables" class="apa-page">
              ${heading}
              <h2 class="apa-heading-1">List of Tables</h2>
              <div class="apa-paragraph">${listOfTablesText}</div>
            </div>
          </div>
        `;
        break;

      case "Appendices Page":
        previewHTML = `
          <div class="apa-document">
            <div id="appendices" class="apa-page">
              ${heading}
              <h2 class="apa-heading-1">Appendices</h2>
              <div class="apa-paragraph">${appendicesText}</div>
            </div>
          </div>
        `;
        break;

      case "References Page":
        previewHTML = `
          <div class="apa-document">
            <div id="references" class="apa-page">
              ${heading}
              <h2 class="apa-heading-1">References</h2>
              <div class="apa-paragraph">${referencesText}</div>
            </div>
          </div>
        `;
        break;

      case "Other Info Page":
        previewHTML = `
          <div class="apa-document">
            <div id="other-info" class="apa-page">
              ${heading}
              <h2 class="apa-heading-1">Other Info</h2>
              <div class="apa-paragraph">${otherInfoText}</div>
            </div>
          </div>
        `;
        break;

      case "Signature Page":
        previewHTML = `
          <div class="apa-document">
            <div id="signature-page" class="apa-page">
              ${heading}
              <h2 class="apa-heading-1">Signature Page</h2>
              <div class="apa-paragraph">${signatureText}</div>
            </div>
          </div>
        `;
        break;

      case "Copyright Page":
        previewHTML = `
          <div class="apa-document">
            <div id="copyright-page" class="apa-copyright-page">
              <div class="apa-paragraph"><p>${copyrightText ? ("&copy" + copyrightText) : ("&copy" + "2025 John Smith")}</p></div>
            </div>
          </div>
        `;
        break;

      default:
        // If it's some leftover or unknown part, just show the generic text
        previewHTML = `
          <div class="apa-document">
            <div class="apa-page">
              ${heading}
              <h2 class="apa-heading-1">${headerText || "Content"}</h2>
              <div class="apa-paragraph">${genericText}</div>
            </div>
          </div>
        `;
        break;
    }

    // Finally, sanitize the HTML
    const sanitized = DOMPurify.sanitize(previewHTML);
    setFormattedContent(sanitized);
  }, [
    headerText,
    coverPage,
    tableOfContents,
    abstractText,
    dedicationText,
    listOfFiguresText,
    listOfTablesText,
    appendicesText,
    referencesText,
    otherInfoText,
    signatureText,
    copyrightText,
    genericText,
  ]);

  if (loading) {
    return <p>Loading {headerText} data...</p>;
  }

  return (
    <div className="container">
      {error && <p style={{ color: "red" }}>{error}</p>}

      <div className="col-md-12">
        <h3 className="flex text-center">{headerText}</h3>
        <p>
          Download APA sample paper{" "}
          <a
            href="https://apastyle.apa.org/style-grammar-guidelines/paper-format/professional-paper.docx"
            target="_blank"
            rel="noreferrer"
          >
            -- Link
          </a>
        </p>
        <p>
          Relevant APA{" "}
          <a
            href="https://apastyle.apa.org/style-grammar-guidelines"
            target="_blank"
            rel="noreferrer"
          >
            -- Link
          </a>
        </p>
        <div className="row">
          {/* ====================== LEFT COLUMN: Editor UI ====================== */}
          <div className="col-md-6 border" style={{ minHeight: "400px" }}>
            {/* Switch by part to display the correct editor controls */}
            {headerText === "Title Page" && (
              <div style={{ marginTop: "1rem" }}>
                <label>Title:</label>
                <input
                  type="text"
                  className="form-control"
                  value={coverPage.title}
                  onChange={(e) =>
                    handleCoverPageChange("title", e.target.value)
                  }
                />
                <label>Author:</label>
                <input
                  type="text"
                  className="form-control"
                  value={coverPage.author}
                  onChange={(e) =>
                    handleCoverPageChange("author", e.target.value)
                  }
                />
                <label>Affiliation:</label>
                <input
                  type="text"
                  className="form-control"
                  value={coverPage.affiliation}
                  onChange={(e) =>
                    handleCoverPageChange("affiliation", e.target.value)
                  }
                />
                <label>Course:</label>
                <input
                  type="text"
                  className="form-control"
                  value={coverPage.course}
                  onChange={(e) =>
                    handleCoverPageChange("course", e.target.value)
                  }
                />
                <label>Instructor:</label>
                <input
                  type="text"
                  className="form-control"
                  value={coverPage.instructor}
                  onChange={(e) =>
                    handleCoverPageChange("instructor", e.target.value)
                  }
                />
                <label>Due Date:</label>
                <input
                  type="date"
                  className="form-control"
                  value={coverPage.due_date}
                  onChange={(e) =>
                    handleCoverPageChange("due_date", e.target.value)
                  }
                />
              </div>
            )}

            {headerText === "Table of Contents Page" && (
              <div style={{ marginTop: "1rem" }}>
                <h5>Edit TOC Entries</h5>
                {tableOfContents.map((entry, index) => (
                  <div key={index} style={{ marginBottom: "10px" }}>
                    <input
                      type="text"
                      className="form-control"
                      placeholder="Section Title"
                      value={entry.section_title}
                      onChange={(e) =>
                        handleTOCChange(index, "section_title", e.target.value)
                      }
                    />
                    <input
                      type="number"
                      className="form-control"
                      placeholder="Page Number"
                      value={entry.page_number || ""}
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

            {headerText === "Abstract Page" && (
              <div style={{ marginTop: "1rem" }}>
                <ReactQuill
                  value={abstractText}
                  onChange={handleAbstractChange}
                  placeholder={textAreaPlaceholder}
                  modules={quillModules}
                />
              </div>
            )}

            {headerText === "Dedication Page" && (
              <div style={{ marginTop: "1rem" }}>
                <ReactQuill
                  value={dedicationText}
                  onChange={handleDedicationChange}
                  placeholder={textAreaPlaceholder}
                  modules={quillModules}
                />
              </div>
            )}

            {headerText === "List of Figures Page" && (
              <div style={{ marginTop: "1rem" }}>
                <ReactQuill
                  value={listOfFiguresText}
                  onChange={handleListOfFiguresChange}
                  placeholder={textAreaPlaceholder}
                  modules={quillModules}
                />
              </div>
            )}

            {headerText === "List of Tables Page" && (
              <div style={{ marginTop: "1rem" }}>
                <ReactQuill
                  value={listOfTablesText}
                  onChange={handleListOfTablesChange}
                  placeholder={textAreaPlaceholder}
                  modules={quillModules}
                />
              </div>
            )}

            {headerText === "Appendices Page" && (
              <div style={{ marginTop: "1rem" }}>
                <ReactQuill
                  value={appendicesText}
                  onChange={handleAppendicesChange}
                  placeholder={textAreaPlaceholder}
                  modules={quillModules}
                />
              </div>
            )}

            {headerText === "References Page" && (
              <div style={{ marginTop: "1rem" }}>
                <ReactQuill
                  value={referencesText}
                  onChange={handleReferencesChange}
                  placeholder={textAreaPlaceholder}
                  modules={quillModules}
                />
              </div>
            )}

            {headerText === "Other Info Page" && (
              <div style={{ marginTop: "1rem" }}>
                <ReactQuill
                  value={otherInfoText}
                  onChange={handleOtherInfoChange}
                  placeholder={textAreaPlaceholder}
                  modules={quillModules}
                />
              </div>
            )}

            {headerText === "Signature Page" && (
              <div style={{ marginTop: "1rem" }}>
                <ReactQuill
                  value={signatureText}
                  onChange={handleSignatureChange}
                  placeholder={textAreaPlaceholder}
                  modules={quillModules}
                />
              </div>
            )}

            {headerText === "Copyright Page" && (
              <div style={{ marginTop: "1rem" }}>
                <ReactQuill
                  value={copyrightText}
                  onChange={(val) => {
                    setCopyrightText(val);
                    // Debounce call:
                    try {
                      // We’ll fix the small bug in the snippet above
                      // (we wrote `copyrightText(val)` by mistake).
                      // Instead:d
                      debounceCopyright(val);
                    } catch (err) {
                      console.error(err);
                    }
                  }}
                  placeholder={textAreaPlaceholder}
                  modules={quillModules}
                />
              </div>
            )}

            {/* Default fallback for unknown parts */}
            {[
              "Title Page",
              "Table of Contents Page",
              "Abstract Page",
              "Dedication Page",
              "List of Figures Page",
              "List of Tables Page",
              "Appendices Page",
              "References Page",
              "Other Info Page",
              "Signature Page",
              "Copyright Page",
            ].indexOf(headerText) === -1 && (
              <div style={{ marginTop: "1rem" }}>
                <ReactQuill
                  value={genericText}
                  onChange={handleGenericChange}
                  placeholder={textAreaPlaceholder}
                  modules={quillModules}
                />
              </div>
            )}
          </div>

          {/* ====================== RIGHT COLUMN: APA Preview ====================== */}
          <div
            className="col-md-6 border"
            style={{ maxHeight: "80vh", overflowY: "auto" }}
          >
            <div dangerouslySetInnerHTML={{ __html: formattedContent }} />
          </div>
        </div>
      </div>

      {/* FOOTER / Buttons */}
      <div className="row" style={{ marginTop: "1rem" }}>
        <div className="col-md-2">
          <Link to="/app/manage-theses" className="btn btn-primary mb-3">
            Back to Dashboard
          </Link>
        </div>
      </div>
    </div>
  );
};

// Quill configuration
const quillModules = {
  toolbar: [
    [{ header: [1, 2, 3, false] }],
    ["bold", "italic", "underline"],
    [{ list: "ordered" }, { list: "bullet" }],
    ["blockquote", "code-block"],
    ["link", "image"],
    ["clean"],
  ],
};

// A separate debounced function for Copyright:
const debounceCopyright = debounce(async (val) => {
  try {
    await thesisAPI.updateCopyrightPage(/* thesisId, */ { content: val });
  } catch (err) {
    console.error("Failed to update copyright page:", err);
  }
}, 500);

export default Part;
