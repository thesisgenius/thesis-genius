import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import apiClient from "../services/apiClient";
import useRedirectIfAuthenticated from "../hooks/useRedirectIfAuthenticated";
import "./../styles/Signup.css";

const Signup = () => {
    useRedirectIfAuthenticated(); // Redirect if already authenticated

    const [formData, setFormData] = useState({ name: "", email: "", password: "" });
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    // Handle input changes for the form
    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData({ ...formData, [name]: value });
    };

    // Handle form submission
    const handleSignup = async (e) => {
        e.preventDefault();
        setLoading(true);
        try {
            const response = await apiClient.post("/auth/register", formData);
            if (response.data.success) {
                // Automatically sign in the user after registration
                const signInResponse = await apiClient.post("/auth/signin", {
                    email: formData.email,
                    password: formData.password,
                });

                const { token } = signInResponse.data;
                localStorage.setItem("token", token); // Save the token
                alert("Signup successful! Redirecting to dashboard...");
                navigate("/dashboard"); // Redirect to the dashboard
            } else {
                alert(response.data.message || "Signup failed. Please try again.");
            }
        } catch (error) {
            console.error("Signup failed:", error);
            alert("An error occurred. Please try again later.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="signup-container">
            <h1>Create an Account</h1>
            <form onSubmit={handleSignup}>
                <label htmlFor="name">Name</label>
                <input
                    type="text"
                    name="name"
                    id="name"
                    value={formData.name}
                    onChange={handleInputChange}
                    placeholder="Enter your name"
                    required
                />

                <label htmlFor="email">Email</label>
                <input
                    type="email"
                    name="email"
                    id="email"
                    value={formData.email}
                    onChange={handleInputChange}
                    placeholder="Enter your email"
                    required
                />

                <label htmlFor="password">Password</label>
                <input
                    type="password"
                    name="password"
                    id="password"
                    value={formData.password}
                    onChange={handleInputChange}
                    placeholder="Enter your password"
                    required
                />

                <button type="submit" disabled={loading}>
                    {loading ? "Signing Up..." : "Sign Up"}
                </button>
            </form>
        </div>
    );
};

export default Signup;
