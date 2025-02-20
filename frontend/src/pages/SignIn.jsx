// src/pages/SignIn.jsx
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import apiClient from "../services/apiClient";
import { useAuth } from "../context/AuthContext";
import useRedirectIfAuthenticated from "../hooks/useRedirectIfAuthenticated";

import "../styles/SignIn.css";

const SignIn = () => {
  useRedirectIfAuthenticated();
  const { setUser } = useAuth();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleSignIn = async (e) => {
    e.preventDefault();
    try {
      const response = await apiClient.post("/auth/signin", { email, password });
      const { token } = response.data;

            localStorage.setItem("token", token); // Save the token
            alert("Sign-in successful! Redirecting to dashboard...");
            navigate("/dashboard"); // Redirect to the dashboard
            window.location.reload();                  // 🔄 Refresh after sign-in

    } catch (error) {
      console.error("Sign-in failed:", error);
      alert("Invalid email or password.");
      window.location.reload();                  // 🔄 Refresh after sign-in

    }
  };

  return (
    <div className="signin-container">
      <h1>Sign In</h1>
      <form onSubmit={handleSignIn}>
        <label>Email:</label>
                <input
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                />
                <br />
        <label>Password:</label>
                <input
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                />
                <br />
        <button type="submit">Sign In</button>
      </form>
    </div>
  );
};

export default SignIn;
