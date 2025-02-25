import { useEffect } from "react";
import { useNavigate } from "react-router-dom";

/**
 * Custom hook to redirect authenticated users to the dashboard.
 */
const useRedirectIfAuthenticated = () => {
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (token) {
      navigate("/app/manage-thesis"); // Redirect if a token exists
    }
  }, [navigate]);
};

export default useRedirectIfAuthenticated;
