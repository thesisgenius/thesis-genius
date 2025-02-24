import { useState, useEffect } from "react";
import { Link, useParams } from "react-router-dom";
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap/dist/js/bootstrap.bundle.min.js";
import ReactQuill from "react-quill";
import "react-quill/dist/quill.snow.css"; // Import Quill's CSS
import FadingBanner from "../components/FadingBanner";
import thesisAPI from "../services/thesisEndpoint";

const PREDEFINED_SECTIONS = [
  "Chapter I: Introduction",
  "Chapter II: Literature Review",
  "Chapter III: Methods",
  "Chapter IV: Results",
  "Chapter V: Discussion",
];

const ThesisBody = () => {
  const { thesisId } = useParams();

  const [selectedSection, setSelectedSection] = useState(
    PREDEFINED_SECTIONS[0],
  );

  const [sectionContent, setSectionContent] = useState(
    PREDEFINED_SECTIONS.reduce((content, section) => {
      content[section] = `Placeholder for ${section.toLowerCase()}...`;
      return content;
    }, {}),
  );

  const [chapterIds, setChapterIds] = useState({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    const loadChapters = async () => {
      setLoading(true);
      try {
        console.log("Starting to fetch chapters for thesisId:", thesisId);

        // Ensure we get the chapters array from the response object
        const response = await thesisAPI.getChapters(thesisId);
        const dbChapters = response || []; // Safely access the chapters array
        console.log("Fetched chapters from API:", dbChapters);

        const sectionUpdates = await Promise.all(
          PREDEFINED_SECTIONS.map(async (sectionName) => {
            const found = dbChapters.find(
              (chapter) => chapter.name === sectionName,
            );
            console.log(`Processing section: ${sectionName}`);
            if (found) {
              console.log(`Found section in DB: ${sectionName}`, found);
              return {
                name: sectionName,
                content: found.content || "",
                id: found.id,
              };
            } else {
              console.log(
                `Section not found in DB: ${sectionName}, creating new one.`,
              );
              const newChapter = await thesisAPI.addChapter(thesisId, {
                name: sectionName,
                content: sectionContent[sectionName] || "",
              });
              console.log(
                `Created new chapter in DB: ${sectionName}`,
                newChapter,
              );
              return {
                name: sectionName,
                content: newChapter.content || "",
                id: newChapter.id,
              };
            }
          }),
        );

        const newSectionContent = {};
        const newChapterIds = {};
        sectionUpdates.forEach(({ name, content, id }) => {
          newSectionContent[name] = content;
          newChapterIds[name] = id;
        });

        console.log("Final sectionContent:", newSectionContent);
        console.log("Final chapterIds:", newChapterIds);

        setSectionContent(newSectionContent);
        setChapterIds(newChapterIds);
      } catch (err) {
        console.error("Failed to fetch or create chapters:", err);
        setError("Error loading chapters. Please try again.");
      } finally {
        setLoading(false);
      }
    };

    if (thesisId) {
      loadChapters();
    } else {
      setError("Invalid Thesis ID.");
    }
  }, [thesisId]);

  const handleSectionChange = (section) => {
    setSelectedSection(section);
  };

  const handleContentChange = async (newValue) => {
    setSectionContent({
      ...sectionContent,
      [selectedSection]: newValue,
    });

    try {
      const chapterId = chapterIds[selectedSection];
      if (chapterId) {
        await thesisAPI.updateChapter(thesisId, chapterId, {
          content: newValue,
        });
      }
    } catch (err) {
      console.error("Failed to update chapter content:", err);
      setError("Error updating chapter content. Please try again.");
    }
  };

  if (loading) {
    return <div className="container">Loading chapters...</div>;
  }
  if (error) {
    return <div className="container text-danger">{error}</div>;
  }

  return (
    <div className="container">
      <div className="col-md-12">
        <h3 className="flex">{selectedSection}</h3>
        <div className="row">
          {/* Sidebar Navigation */}
          <div className="col-md-2">
            <ul className="list-group">
              {PREDEFINED_SECTIONS.map((section) => (
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
        <Link to="/app/manage-theses" className="btn btn-primary mb-3">
          Back to Dashboard
        </Link>
      </div>
    </div>
  );
};

export default ThesisBody;
