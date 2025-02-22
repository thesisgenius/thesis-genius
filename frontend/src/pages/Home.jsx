import React from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import Slider from "react-slick";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";
import "../styles/Home.css";

const Home = () => {
  const { user, signOut } = useAuth();
  const navigate = useNavigate();

  const handleLogout = async () => {
    await signOut();
    window.location.reload(); // 🔄 Refresh page after logout
  };

  const whyNeedIt = [
    { title: "Know All the Stuff", description: "You've done the research, gathered the data, and have all the content ready." },
    { title: "Did the Work", description: "Hours of effort went into compiling your thesis. Now it's time to structure it properly." },
    { title: "Ready to Put It in Print", description: "Ready to put it on paper or in a document, but formatting and finalization can be tricky." },
    { title: "Thesis Genius Merges it", description: "Our platform helps you seamlessly bring everything together in a polished format." }
  ];

  const steps = [
    { title: "Create a Profile", description: "Keep track and manage all your work in one place. Come back later to finish" },
    { title: "Create a Thesis", description: "Start a new thesis project and outline the key sections before diving into the details." },
    { title: "Break It Down into Parts", description: "Structure your thesis into manageable sections." },
    { title: "Manage Your Thesis", description: "Easily create, edit, and track the progress of your academic work at any stage." },
    { title: "Engage in Forums", description: "Join discussions with peers and experts in your field." },
    { title: "Submit for Approval", description: "Send your thesis for review and get feedback from your professor or advisor." },
    { title: "Finalize & Export", description: "Once approved, format your thesis and export it to a PDF, or DOC." }
  ];

  const helpInfo = [
    { title: "Manage Your Thesis", description: "Easily create, edit, and track the progress of your academic work." },
    { title: "Engage in Forums", description: "Join discussions with peers and experts in your field." },
    { title: "Stay Organized", description: "Keep all your research and conversations in one place." },
    { title: "Get the Help You Need", description: "Find guidance and resources to complete your thesis efficiently." },
    { title: "Knowledge & Assistance", description: "We provide informational links and structured guidance to help you succeed." },
    { title: "Help at Every Stage", description: "Our support extends from planning to final submission." },
  ];

  const settings = {
    dots: false,
    infinite: true,
    speed: 500,
    slidesToShow: 1,
    slidesToScroll: 1,
    autoplay: true,
    autoplaySpeed: 1000,
    fade: true
  };

  return (
    <div className="home-container">
      <header className="hero-section">
        <div className="hero-content">
          <h1>Welcome to Thesis Genius</h1>
          <p>Your platform for managing theses and engaging in academic discussions.</p>
          <div className="hero-buttons">
            {user ? (
              <>
                <Link to="/dashboard" className="button primary">Dashboard</Link>
                <button onClick={handleLogout} className="button secondary">Logout</button>
              </>
            ) : (
              <>
                <Link to="/signin" className="button primary">Sign In</Link>
                <Link to="/signup" className="button secondary">Sign Up</Link>
              </>
            )}
          </div>
        </div>
      </header>

      <section className="features-section" style={{ marginTop: "15px" }}>
        <h2 style={{ textAlign: "center", marginTop: "-45px" }}>How It Works</h2>
        <div
          className="info-box-container"
          style={{
            display: "flex",
            justifyContent: "center",
            gap: "20px",
            flexWrap: "nowrap",
            alignItems: "flex-start",
          }}
        >
          {[whyNeedIt, steps, helpInfo].map((data, i) => (
            <div
              key={i}
              className="carousel-box"
              style={{
                backgroundColor: "#e0f7fa",
                padding: "30px",
                marginTop: "15px",
                borderRadius: "10px",
                border: "2px solid #007BFF",
                boxShadow: "-10px 10px 20px rgba(0, 0, 0, 0.2)",
                maxWidth: "450px",
                width: "450px",
                height: "150px",
                textAlign: "center",
                overflow: "hidden",
                display: "flex",
                flexDirection: "column",
                justifyContent: "center",
              }}
            >
              <Slider {...settings} autoplaySpeed={(i + 1) * 2000 + 2000} pauseOnHover={false} fade={true}>
                {data.map((item, index) => (
                  <div key={index} className="carousel-slide" style={{ padding: "15px" }}>
                    <h3>{item.title}</h3>
                    <p style={{ whiteSpace: "pre-line" }}>{item.description}</p>
                  </div>
                ))}
              </Slider>
            </div>
          ))}
        </div>
      </section>

      {!user && (
        <footer className="cta-section">
          <h2>Ready to Get Started?</h2>
          <div style={{ marginTop: "20px" }}>
            <Link to="/signup" className="button primary">Create an Account</Link>
          </div>
        </footer>
      )}
    </div>
  );
};

export default Home;
