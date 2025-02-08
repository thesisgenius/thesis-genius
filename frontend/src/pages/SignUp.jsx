import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import apiClient from "../services/apiClient";
import useRedirectIfAuthenticated from "../hooks/useRedirectIfAuthenticated";
import "./../styles/SignUp.css";

const Signup = () => {
    useRedirectIfAuthenticated(); // Redirect if already authenticated

    const [formData, setFormData] = useState({ first_name: "", last_name: "", email: "", password: "", institution: "" });
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
                <label htmlFor="first_name">First Name</label>
                <input
                    type="text"
                    name="first_name" // Corrected name attribute
                    id="first_name"
                    value={formData.first_name}
                    onChange={handleInputChange}
                    placeholder="Enter your first name"
                    required
                />

                <label htmlFor="last_name">Last Name</label>
                <input
                    type="text"
                    name="last_name" // Corrected name attribute
                    id="last_name"
                    value={formData.last_name}
                    onChange={handleInputChange}
                    placeholder="Enter your last name"
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

                <label htmlFor="institution">Institution</label>
                <input
                    type="text"
                    name="institution"
                    id="institution"
                    value={formData.institution}
                    onChange={handleInputChange}
                    placeholder="Enter your school or institution"
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
