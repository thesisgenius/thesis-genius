// ThesisBody.jsx
import React, { useState } from "react";
import { Link, useParams } from "react-router-dom";
import ReactQuill from "react-quill";
import "react-quill/dist/quill.snow.css";
import "../styles/apaStyle.css";
import FadingBanner from "../components/FadingBanner";
import { useThesisBody } from "../hooks/useThesisBody";

export default function ThesisBody() {
  const { thesisId } = useParams();
  const {
    chapters,
    selectedChapter,
    loading,
    error,
    formattedContent,
    moveChapterUp,
    moveChapterDown,
    updateChapterContent,
    addNewChapter,
    deleteChapter,
    setSelectedChapterId,
  } = useThesisBody(thesisId, [
    // if you only want to auto-create these if no chapters exist
    "Chapter I: Introduction",
    "Chapter II: Literature Review",
    "Chapter III: Methods",
    "Chapter IV: Results",
    "Chapter V: Discussion",
  ]);

  const [newChapterName, setNewChapterName] = useState("");

  if (loading) return <div className="container">Loading chapters...</div>;
  if (error) return <div className="container text-danger">{error}</div>;

  return (
      <div className="container">
        <div className="col-md-12">
          <h3 className="flex">Thesis Body (Add/Remove & Reorder, No Duplicates)</h3>

          <div className="row">
            {/* Sidebar */}
            <div className="col-md-2">
              {/* Add Chapter */}
              <div style={{ marginBottom: "10px" }}>
                <input
                    type="text"
                    className="form-control"
                    placeholder="New Chapter Name"
                    value={newChapterName}
                    onChange={(e) => setNewChapterName(e.target.value)}
                />
                <button
                    className="btn btn-sm btn-primary mt-2"
                    onClick={() => {
                      if (newChapterName.trim()) {
                        addNewChapter(newChapterName.trim());
                        setNewChapterName("");
                      }
                    }}
                >
                  + Add Chapter
                </button>
              </div>

              {/* Chapters list */}
              <ul className="list-group">
                {chapters.map((ch, idx) => (
                    <li
                        key={ch.id}
                        className="list-group-item"
                        style={{
                          cursor: "pointer",
                          backgroundColor:
                              selectedChapter?.id === ch.id ? "#e9ecef" : "white",
                        }}
                    >
                      <div onClick={() => setSelectedChapterId(ch.id)}>
                        {ch.name}
                      </div>

                      <div style={{ marginTop: "5px" }}>
                        <button
                            className="btn btn-sm btn-outline-secondary"
                            onClick={() => moveChapterUp(ch.id)}
                            disabled={idx === 0}
                        >
                          ↑
                        </button>
                        <button
                            className="btn btn-sm btn-outline-secondary"
                            style={{ marginLeft: "5px" }}
                            onClick={() => moveChapterDown(ch.id)}
                            disabled={idx === chapters.length - 1}
                        >
                          ↓
                        </button>
                        <button
                            className="btn btn-sm btn-danger"
                            style={{ marginLeft: "5px" }}
                            onClick={() => deleteChapter(ch.id)}
                        >
                          Delete
                        </button>
                      </div>
                    </li>
                ))}
              </ul>
            </div>

            {/* Middle: Quill */}
            <div className="col-md-5 border">
              {selectedChapter ? (
                  <ReactQuill
                      theme="snow"
                      value={selectedChapter.content || ""}
                      onChange={(val) => updateChapterContent(selectedChapter.id, val)}
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
              ) : (
                  <p>Select or create a chapter to start editing.</p>
              )}
            </div>

            {/* Right: APA Preview */}
            <div className="col-md-5 border display-screen">
              <div dangerouslySetInnerHTML={{ __html: formattedContent }} />
            </div>
          </div>
        </div>

        <div className="row">
          <FadingBanner />
        </div>
        <div className="col-md-2">
          <Link to="/app/manage-theses" className="btn btn-primary mb-3">
            Back to Dashboard
          </Link>
        </div>
      </div>
  );
}
