import React from "react";
import { Link } from "react-router-dom";
import "../styles/Home.css";

const Home = () => {
    return (
        <div className="home-container">
            <header className="hero-section">
                <div className="hero-content">
                    <h1>Welcome to Thesis Genius</h1>
                    <p>Your platform for managing theses and engaging in academic discussions.</p>
                    <div className="hero-buttons">
                        <Link to="/signin" className="button primary">Sign In</Link>
                        <Link to="/signup" className="button secondary">Sign Up</Link>
                    </div>
                </div>
            </header>
            <section className="features-section">
                <h2>Why Choose Thesis Genius?</h2>
                <div className="features-grid">
                    <div className="feature">
                        <h3>Manage Your Thesis</h3>
                        <p>Easily create, edit, and track the progress of your academic work.</p>
                    </div>
                    <div className="feature">
                        <h3>Engage in Forums</h3>
                        <p>Join discussions with peers and experts in your field.</p>
                    </div>
                    <div className="feature">
                        <h3>Stay Organized</h3>
                        <p>Keep all your research and conversations in one place.</p>
                    </div>
                </div>
            </section>
            <footer className="cta-section">
                <h2>Ready to Get Started?</h2>
                <Link to="/signup" className="button primary">Create an Account</Link>
            </footer>
        </div>
    );
};

export default Home;
