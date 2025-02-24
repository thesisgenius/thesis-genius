// useThesisBody.js

import { useState, useEffect, useMemo } from "react";
import { debounce } from "lodash";
import DOMPurify from "dompurify";
import thesisAPI from "../services/thesisEndpoint";

export function useThesisBody(thesisId) {
    // We'll store chapters in an array: [ {id, name, content, order}, ... ]
    const [chapters, setChapters] = useState([]);
    const [selectedChapterId, setSelectedChapterId] = useState(null);

    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");
    const [formattedContent, setFormattedContent] = useState("");
    const [didLoadChapters, setDidLoadChapters] = useState(false);

    // Debounced update function
    const debouncedUpdateChapter = useMemo(
        () =>
            debounce(async (chapterId, fields) => {
                try {
                    await thesisAPI.updateChapter(thesisId, chapterId, fields);
                } catch (err) {
                    console.error("Failed to update chapter:", err);
                    setError("Could not update chapter. Please try again.");
                }
            }, 500),
        [thesisId]
    );

    // Load chapters once
    useEffect(() => {
        if (!thesisId || didLoadChapters) return;

        const loadChapters = async () => {
            setLoading(true);
            try {
                let dbChapters = await thesisAPI.getChapters(thesisId);
                // Sort them by order ascending
                dbChapters.sort((a, b) => (a.order || 0) - (b.order || 0));

                setChapters(dbChapters);
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
    }, [thesisId, didLoadChapters]);

    // Reorder chapters
    const moveChapterUp = (chapterId) => {
        const idx = chapters.findIndex((c) => c.id === chapterId);
        if (idx <= 0) return; // already at top or not found
        const above = chapters[idx - 1];
        const current = chapters[idx];

        // Swap their 'order'
        const newOrder = above.order;
        const oldOrder = current.order;

        const updated = [...chapters];
        updated[idx - 1] = { ...above, order: oldOrder };
        updated[idx] = { ...current, order: newOrder };
        updated.sort((a, b) => (a.order || 0) - (b.order || 0));
        setChapters(updated);

        // Debounced calls to update both chapters
        debouncedUpdateChapter(current.id, { order: newOrder });
        debouncedUpdateChapter(above.id, { order: oldOrder });
    };

    const moveChapterDown = (chapterId) => {
        const idx = chapters.findIndex((c) => c.id === chapterId);
        if (idx < 0 || idx >= chapters.length - 1) return; // already at bottom
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

    // Called when user types in Quill
    const updateChapterContent = (chapterId, newContent) => {
        // local
        setChapters((prev) =>
            prev.map((ch) => (ch.id === chapterId ? { ...ch, content: newContent } : ch))
        );
        // debounced server update
        debouncedUpdateChapter(chapterId, { content: newContent });
    };

    // Add a new chapter
    const addNewChapter = async (chapterName) => {
        try {
            // find max order
            let maxOrder = 0;
            if (chapters.length > 0) {
                maxOrder = Math.max(...chapters.map((c) => c.order || 0));
            }
            const newChapter = await thesisAPI.addChapter(thesisId, {
                name: chapterName,
                content: "",
                order: maxOrder + 1,
            });
            const updated = [...chapters, newChapter];
            updated.sort((a, b) => (a.order || 0) - (b.order || 0));
            setChapters(updated);
            setSelectedChapterId(newChapter.id);
        } catch (err) {
            console.error("Failed to add new chapter:", err);
            setError("Could not add chapter. Please try again.");
        }
    };

    // Remove a chapter
    const deleteChapter = async (chapterId) => {
        try {
            await thesisAPI.deleteChapter(thesisId, chapterId);
            let updated = chapters.filter((ch) => ch.id !== chapterId);
            setChapters(updated);

            // If the removed chapter was selected, pick another
            if (selectedChapterId === chapterId) {
                if (updated.length > 0) {
                    setSelectedChapterId(updated[0].id);
                } else {
                    setSelectedChapterId(null);
                }
            }
        } catch (err) {
            console.error("Failed to delete chapter:", err);
            setError("Could not delete chapter. Please try again.");
        }
    };
    // Generate APA preview
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
        setSelectedChapterId,
    };
}
