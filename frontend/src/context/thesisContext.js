// frontend/src/context/thesisContext.js
import { createContext, useContext } from "react";

/**
 * Just the ThesisContext and a custom useThesis hook.
 */
export const ThesisContext = createContext(null);

export function useThesis() {
  return useContext(ThesisContext);
}
