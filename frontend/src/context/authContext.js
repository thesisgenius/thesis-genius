// frontend/src/context/authContext.js
import { createContext, useContext } from "react";

/**
 * The AuthContext object used to share auth state.
 * Typically paired with AuthProvider (see AuthProvider.jsx).
 */
export const AuthContext = createContext(null);

/**
 * A custom hook to access the AuthContext value.
 */
export function useAuth() {
  return useContext(AuthContext);
}
