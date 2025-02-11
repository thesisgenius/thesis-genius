// Required installations for this file:
// Run the following command in your project root:
// npm install react-slick slick-carousel
// This installs the necessary dependencies for the carousels.

import React from "react";
import { Link } from "react-router-dom";
import Slider from "react-slick";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";
import "../styles/Home.css";

const Home = () => {
    const whyNeedIt = [
        { title: "Know All the Stuff", description: "You've done the research, gathered the data, and have all the content ready." },
        { title: "Did All the Work", description: "Hours of effort went into compiling your thesis. Now it's time to structure it properly." },
        { title: "Ready to Write it Down", description: "Ready to put it on paper or in a document,\nbut formatting and finalization can be tricky." },
        { title: "Thesis Genius Merges It", description: "Our platform helps you seamlessly bring everything together in a polished format." }
    ];

    const steps = [
	{ title: "Create a Profile", description: "Keep track of all your work in one place.\nYour profile will store your thesis projects,\ndrafts, and approvals." },
        { title: "Create a Thesis", description: "Start a new thesis project and outline the\nkey sections before diving into the details." },
        { title: "Break it Down into Parts", description: "Structure your thesis into manageable sections\nlike introduction, literature review,\nmethodology, and conclusion." },
	{ title: "Manage Your Thesis", description: "Easily create, edit, and track the progress of your academic work at any stage\nEdit and refine your work as you progress." },
        { title: "Engage in Forums", description: "Join discussions with peers and experts in your field." },     
        { title: "Submit for Approval", description: "Send your thesis for review and get feedback\nfrom your professor or advisor." },
        { title: "Finalize & Export", description: "Once approved, format your thesis and export\nit to PDF, DOC, or other formats for submission." }
    ];

    const helpInfo = [
        { title: "Manage Your Thesis", description: "Easily create, edit, and track the progress of your academic work." },
        { title: "Engage in Forums", description: "Join discussions with peers and experts in your field." },
        { title: "Stay Organized", description: "Keep all your research and conversations in one place." },
        { title: "Get the Help You Need", description: "Find guidance and resources to complete your thesis efficiently." },
        { title: "Knowledge & Assistance", description: "We provide informational links and structured guidance to help you succeed." },
        { title: "We're With You All the Way", description: "Our support extends from planning to final submission." },
        { title: "Students Helping Students", description: "Collaborate and learn from peers who have gone through the same journey." }

    ];

    // Settings for the carousels, including autoplay and transition effects.
const settings = {
        dots: true,
        infinite: true,
        speed: 500,
        slidesToShow: 1,
        slidesToScroll: 1,
        autoplay: true,
        autoplaySpeed: 3000,
        fade: true
    };

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
                <h2>How It Works</h2>
                <div className="info-box-container" style={{ display: "flex", justifyContent: "center", gap: "20px", marginTop: "20px" }}>
                    <div className="carousel-box" style={{ backgroundColor: "#e0f7fa", padding: "30px", borderRadius: "10px", border: "2px solid #007BFF", boxShadow: "-10px 10px 20px rgba(0, 0, 0, 0.2)", maxWidth: "450px", textAlign: "center" }}>
<Slider {...settings} autoplaySpeed={6000} pauseOnHover={false} fade={true}>
                            {whyNeedIt.map((item, index) => (
                                <div key={index} className="carousel-slide" style={{ padding: "15px" }}>
                                    <h3>{item.title}</h3>
                                    <p>{item.description}</p>
                                </div>
                            ))}
                        </Slider>
                    </div>
                    <div className="carousel-box" style={{ backgroundColor: "#e0f7fa", padding: "30px", borderRadius: "10px", border: "2px solid #007BFF", boxShadow: "-10px 10px 20px rgba(0, 0, 0, 0.2)", maxWidth: "450px", textAlign: "center" }}>
<Slider {...settings} autoplaySpeed={9000} pauseOnHover={false} fade={true}>
                            {steps.map((step, index) => (
                                <div key={index} className="carousel-slide" style={{ padding: "15px" }}>
                                    <h3>{step.title}</h3>
                                    <p style={{ whiteSpace: "pre-line" }}>{step.description}</p>
                                </div>
                            ))}
                        </Slider>
                    </div>
                    <div className="carousel-box" style={{ backgroundColor: "#e0f7fa", padding: "30px", borderRadius: "10px", border: "2px solid #007BFF", boxShadow: "-10px 10px 20px rgba(0, 0, 0, 0.2)", maxWidth: "450px", textAlign: "center" }}>
<Slider {...settings} autoplaySpeed={12000} pauseOnHover={false} fade={true}>
                            {helpInfo.map((item, index) => (
                                <div key={index} className="carousel-slide" style={{ padding: "15px" }}>
                                    <h3>{item.title}</h3>
                                    <p>{item.description}</p>
                                </div>
                            ))}
                        </Slider>
                    </div>
                </div>
            </section>
            <footer className="cta-section">
                <h2>Ready to Get Started?</h2>
                <div style={{ marginTop: "30px" }}>
                    <Link to="/signup" className="button primary">Create an Account</Link>
                </div>
            </footer>
        </div>
    );
};

export default Home;
