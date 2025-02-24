// frontend/src/context/ThesisProvider.jsx
import React, { useState, useEffect, useMemo } from "react";
import { ThesisContext } from "./thesisContext";
import thesisAPI from "../services/thesisEndpoint";

/**
 * ThesisProvider now fetches the thesis data whenever `activeThesisId` changes.
 */
export default function ThesisProvider({ children }) {
  const [activeThesisId, setActiveThesisId] = useState(null);
  const [activeThesis, setActiveThesis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // Whenever activeThesisId changes, fetch the latest data
  useEffect(() => {
    if (!activeThesisId) {
      // If none selected, reset state
      setActiveThesis(null);
      setError("");
      return;
    }

    async function loadThesis() {
      setLoading(true);
      setError("");
      try {
        const data = await thesisAPI.getThesis(activeThesisId);
        setActiveThesis(data);
      } catch (err) {
        console.error("Failed to load thesis:", err);
        setError("Failed to load thesis data");
        setActiveThesis(null);
      } finally {
        setLoading(false);
      }
    }

    loadThesis();
  }, [activeThesisId]);

  // Optional: function to force a re-fetch
  async function refreshThesis() {
    if (!activeThesisId) return;
    setLoading(true);
    setError("");
    try {
      const data = await thesisAPI.getThesis(activeThesisId);
      setActiveThesis(data);
    } catch (err) {
      console.error("Failed to refresh thesis:", err);
      setError("Failed to refresh thesis");
    } finally {
      setLoading(false);
    }
  }

  const value = useMemo(
    () => ({
      // controlling which thesis is “active”
      activeThesisId,
      setActiveThesisId,

      // store full thesis data from server
      activeThesis,

      // loading & error states
      loading,
      error,

      // function to manually re-fetch
      refreshThesis,
    }),
    [activeThesisId, activeThesis, loading, error],
  );

  return (
    <ThesisContext.Provider value={value}>{children}</ThesisContext.Provider>
  );
}
