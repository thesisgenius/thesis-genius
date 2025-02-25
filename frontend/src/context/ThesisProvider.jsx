import React, { useState, useEffect, useMemo, useCallback } from "react";
import { ThesisContext } from "./thesisContext";
import thesisAPI from "../services/thesisEndpoint";

export default function ThesisProvider({ children }) {
  const [activeThesisId, setActiveThesisId] = useState(null);
  const [activeThesis, setActiveThesis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // Centralized function for fetching thesis data
  const fetchThesis = useCallback(async () => {
    if (!activeThesisId) {
      setActiveThesis(null);
      setError("");
      return;
    }
    setLoading(true);
    setError("");
    try {
      const data = await thesisAPI.getThesis(activeThesisId);
      setActiveThesis(data);
    } catch (err) {
      console.error("Error fetching thesis:", err);
      setError("Failed to fetch thesis data");
      setActiveThesis(null);
    } finally {
      setLoading(false);
    }
  }, [activeThesisId]);

  // Fetch thesis whenever the activeThesisId changes
  useEffect(() => {
    const performFetch = async () => {
      await fetchThesis(); // Await the Promise to handle async properly
    };
    performFetch()
  }, [activeThesisId, fetchThesis]);

  // Manual refresh of thesis
  const refreshThesis = fetchThesis;

  // Memoized context value to prevent unnecessary re-renders
  const value = useMemo(
      () => ({
        activeThesisId,
        setActiveThesisId,
        activeThesis,
        loading,
        error,
        refreshThesis,
      }),
      [activeThesisId, activeThesis, loading, error, refreshThesis]
  );

  return (
      <ThesisContext.Provider value={value}>
        {children}
      </ThesisContext.Provider>
  );
}