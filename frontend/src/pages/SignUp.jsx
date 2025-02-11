// SignUp.jsx

import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import authAPI from "../services/authEndpoint"; // Use authAPI for authentication-related actions
import useRedirectIfAuthenticated from "../hooks/useRedirectIfAuthenticated";
import "../styles/SignUp.css";

const SignUp = () => {
    useRedirectIfAuthenticated(); // Redirect if already authenticated

    const [formData, setFormData] = useState({
        first_name: "",
        last_name: "",
        email: "",
        password: "",
        confirmPassword: "",
        institution: "",
    });
    const [loading, setLoading] = useState(false);
    const [formErrors, setFormErrors] = useState({});
    const navigate = useNavigate();

    // Handle input changes for the form
    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData({ ...formData, [name]: value });
    };

    // Password Validation Logic
    const validatePassword = (password) => {
        // Ensure password has at least 8 characters, one uppercase, one number, and one special character
        const regex = /^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
        return regex.test(password);
    };

    // Handle form submission
    const handleSignup = async (e) => {
        e.preventDefault();
        const errors = {};

        // Validate inputs
        if (!formData.first_name) errors.first_name = "First name is required.";
        if (!formData.last_name) errors.last_name = "Last name is required.";
        if (!formData.email) errors.email = "Email is required.";
        if (!formData.password) {
            errors.password = "Password is required.";
        } else if (!validatePassword(formData.password)) {
            errors.password =
                "Password must contain at least 8 characters, one uppercase letter, one number, and one special character.";
        }
        if (formData.password !== formData.confirmPassword) {
            errors.confirmPassword = "Passwords do not match.";
        }
        if (!formData.institution) errors.institution = "Institution is required.";

        // If errors exist, set them and stop form submission
        if (Object.keys(errors).length > 0) {
            setFormErrors(errors);
            return;
        }

        setLoading(true);
        try {
            // Register the user through authAPI.register
            const response = await authAPI.register(formData);
            if (response.success) {
                // Automatically sign in the user after registration using authAPI.signIn
                const signInResponse = await authAPI.signIn({
                    email: formData.email,
                    password: formData.password,
                });

                const { token } = signInResponse;
                localStorage.setItem("token", token); // Save the token
                alert("Signup successful! Redirecting to dashboard...");
                navigate("/dashboard"); // Redirect to the dashboard
            } else {
                alert(response.message || "Signup failed. Please try again.");
            }
        } catch (error) {
            console.error("Signup failed:", error);
            alert("An error occurred. Please try again later.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="signup-background">
            <div className="signup-container">
                <header className="signup-header">
                    <h1>Create an Account</h1>
                    <p>Join us and start your journey today!</p>
                </header>
                <form onSubmit={handleSignup} className="signup-form">
                    <label htmlFor="email">Email</label>
                    <input
                        type="email"
                        name="email"
                        id="email"
                        autoComplete="email"
                        className={formErrors.email ? "input-error" : ""}
                        value={formData.email}
                        onChange={handleInputChange}
                        placeholder="Enter your email"
                        required
                    />
                    <span className="error">{formErrors.email}</span>

                    <label htmlFor="first_name">First Name</label>
                    <input
                        type="text"
                        name="first_name"
                        id="first_name"
                        autoComplete="given-name"
                        className={formErrors.first_name ? "input-error" : ""}
                        value={formData.first_name}
                        onChange={handleInputChange}
                        placeholder="Enter your first name"
                        required
                    />
                    <span className="error">{formErrors.first_name}</span>

                    <label htmlFor="last_name">Last Name</label>
                    <input
                        type="text"
                        name="last_name"
                        id="last_name"
                        autoComplete="family-name"
                        className={formErrors.last_name ? "input-error" : ""}
                        value={formData.last_name}
                        onChange={handleInputChange}
                        placeholder="Enter your last name"
                        required
                    />
                    <span className="error">{formErrors.last_name}</span>

                    <label htmlFor="password">Password</label>
                    <input
                        type="password"
                        name="password"
                        id="password"
                        autoComplete="new-password"
                        className={formErrors.password ? "input-error" : ""}
                        value={formData.password}
                        onChange={handleInputChange}
                        placeholder="Enter your password"
                        required
                    />
                    <span className="error">{formErrors.password}</span>

                    <label htmlFor="confirmPassword">Confirm Password</label>
                    <input
                        type="password"
                        name="confirmPassword"
                        id="confirmPassword"
                        autoComplete="new-password"
                        className={formErrors.confirmPassword ? "input-error" : ""}
                        value={formData.confirmPassword}
                        onChange={handleInputChange}
                        placeholder="Re-enter your password"
                        required
                    />
                    <span className="error">{formErrors.confirmPassword}</span>

                    <label htmlFor="institution">Institution</label>
                    <input
                        type="text"
                        name="institution"
                        id="institution"
                        autoComplete="organization"
                        className={formErrors.institution ? "input-error" : ""}
                        value={formData.institution}
                        onChange={handleInputChange}
                        placeholder="Enter your school or institution"
                        required
                    />
                    <span className="error">{formErrors.institution}</span>

                    <div className="signup-button-container">
                        <button type="submit" disabled={loading} className="signup-button">
                            {loading ? "Signing Up..." : "Sign Up"}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
};

export default SignUp;
