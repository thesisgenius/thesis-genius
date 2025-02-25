import React from "react";
import { useAuth } from "@/context/authContext";

const ProtectedRoute = ({ children }) => {
  const { loading } = useAuth();

  // Prevent rendering until loading is complete
  if (loading) return <p>Loading...</p>;

  // Render children if authenticated
  return children;
};

export default ProtectedRoute;
