import { useState, useEffect, useMemo } from "react";
import { debounce } from "lodash";
import DOMPurify from "dompurify";
import thesisAPI from "../services/thesisEndpoint";

export function useThesisBody(thesisId, predefinedSections = []) {
    // We store chapters as an array: [{id, name, content, order}, ...]
    const [chapters, setChapters] = useState([]);
    const [selectedChapterId, setSelectedChapterId] = useState(null);

    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");
    const [formattedContent, setFormattedContent] = useState("");

    // We ensure we only run "loadChapters" once per thesis
    const [didLoadChapters, setDidLoadChapters] = useState(false);

    // Debounce updates so we don't spam the server
    const debouncedUpdateChapter = useMemo(
        () =>
            debounce(async (cid, fields) => {
                try {
                    await thesisAPI.updateChapter(thesisId, cid, fields);
                } catch (err) {
                    console.error("Failed to update chapter:", err);
                    setError("Could not update chapter. Please try again.");
                }
            }, 500),
        [thesisId]
    );

    // 1) Load or create chapters once
    useEffect(() => {
        if (!thesisId || didLoadChapters) return;

        const loadChapters = async () => {
            setLoading(true);
            try {
                // fetch chapters from the server
                let dbChapters = await thesisAPI.getChapters(thesisId);
                // sort by order ascending
                dbChapters.sort((a, b) => (a.order || 0) - (b.order || 0));

                // If you want to auto-create your "predefinedSections" only if
                // there are NO chapters in DB, do:
                if (dbChapters.length === 0 && predefinedSections.length > 0) {
                    let newChapters = [];
                    for (let i = 0; i < predefinedSections.length; i++) {
                        const name = predefinedSections[i];
                        const newOne = await thesisAPI.addChapter(thesisId, {
                            name,
                            content: `Placeholder for ${name}`,
                            order: i + 1,
                        });
                        newChapters.push(newOne);
                    }
                    dbChapters = newChapters;
                }

                // store them
                setChapters(dbChapters);
                // select the first
                if (dbChapters.length > 0) {
                    setSelectedChapterId(dbChapters[0].id);
                }
                setDidLoadChapters(true);
            } catch (err) {
                console.error("Error loading chapters:", err);
                setError("Failed to load chapters.");
            } finally {
                setLoading(false);
            }
        };

        loadChapters();
    }, [thesisId, didLoadChapters]); // no more deps for "predefinedSections"

    // 2) Reordering
    const moveChapterUp = (chapterId) => {
        const idx = chapters.findIndex((c) => c.id === chapterId);
        if (idx <= 0) return;
        const above = chapters[idx - 1];
        const current = chapters[idx];

        const newOrder = above.order;
        const oldOrder = current.order;

        const updated = [...chapters];
        updated[idx - 1] = { ...above, order: oldOrder };
        updated[idx] = { ...current, order: newOrder };
        updated.sort((a, b) => (a.order || 0) - (b.order || 0));
        setChapters(updated);

        // Save changes
        debouncedUpdateChapter(current.id, { order: newOrder });
        debouncedUpdateChapter(above.id, { order: oldOrder });
    };

    const moveChapterDown = (chapterId) => {
        const idx = chapters.findIndex((c) => c.id === chapterId);
        if (idx < 0 || idx >= chapters.length - 1) return;
        const below = chapters[idx + 1];
        const current = chapters[idx];

        const newOrder = below.order;
        const oldOrder = current.order;

        const updated = [...chapters];
        updated[idx + 1] = { ...below, order: oldOrder };
        updated[idx] = { ...current, order: newOrder };
        updated.sort((a, b) => (a.order || 0) - (b.order || 0));
        setChapters(updated);

        debouncedUpdateChapter(current.id, { order: newOrder });
        debouncedUpdateChapter(below.id, { order: oldOrder });
    };

    // 3) Editing content
    const updateChapterContent = (chapterId, newContent) => {
        setChapters((prev) =>
            prev.map((ch) => (ch.id === chapterId ? { ...ch, content: newContent } : ch))
        );
        debouncedUpdateChapter(chapterId, { content: newContent });
    };

    // 4) Add a new chapter
    const addNewChapter = async (chapterName) => {
        try {
            let maxOrder = chapters.length > 0 ? Math.max(...chapters.map((c) => c.order || 0)) : 0;
            const newChap = await thesisAPI.addChapter(thesisId, {
                name: chapterName,
                content: "",
                order: maxOrder + 1,
            });
            const updated = [...chapters, newChap];
            updated.sort((a, b) => (a.order || 0) - (b.order || 0));
            setChapters(updated);
            setSelectedChapterId(newChap.id);
        } catch (err) {
            console.error("Failed to add new chapter:", err);
            setError("Could not add chapter. Please try again.");
        }
    };

    // 5) Delete
    const deleteChapter = async (chapterId) => {
        try {
            await thesisAPI.deleteChapter(thesisId, chapterId);
            let updated = chapters.filter((c) => c.id !== chapterId);
            setChapters(updated);
            if (selectedChapterId === chapterId) {
                if (updated.length > 0) setSelectedChapterId(updated[0].id);
                else setSelectedChapterId(null);
            }
        } catch (err) {
            console.error("Failed to delete chapter:", err);
            setError("Could not delete chapter. Please try again.");
        }
    };

    // 6) Build APA preview
    useEffect(() => {
        const pagesHTML = chapters
            .map(
                (ch) => `
          <div class="apa-page">
            <h4>${ch.name}</h4>
            <div class="apa-paragraph">${ch.content || ""}</div>
          </div>
        `
            )
            .join("");
        const docHTML = `<div class="apa-document">${pagesHTML}</div>`;
        setFormattedContent(DOMPurify.sanitize(docHTML));
    }, [chapters]);

    const selectedChapter = chapters.find((ch) => ch.id === selectedChapterId);

    return {
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
    };
}
