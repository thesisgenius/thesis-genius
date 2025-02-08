import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
    faUser,
    faSignOutAlt,
    faSignInAlt,
    faDashboard,
    faComments,
    faBars,
    faTimes,
} from "@fortawesome/free-solid-svg-icons";
import "../styles/Header.css";

const LOGO_PATH = "/owl.png";
const LOGO_ALT = "ThesisGenius";
const NAV_LINKS = [
    { to: "/dashboard", label: "Dashboard", icon: faDashboard },
    { to: "/forum", label: "Forum", icon: faComments },
    { to: "/signup", label: "Sign Up", icon: faUser },
];

const ExpandableMenu = () => {
    const { user, signOut, refreshUser } = useAuth(); // Include refreshUser
    const navigate = useNavigate();
    const [isMenuOpen, setIsMenuOpen] = useState(false);

    // Handle Logout
    const handleLogout = () => {
        signOut(); // Log the user out
        navigate("/"); // Redirect to home after logout
    };

    // Handle Menu Toggle with Optional User Refresh
    const toggleMenu = async () => {
        if (!isMenuOpen) {
            await refreshUser(); // Optionally refresh user when menu is opened
        }
        setIsMenuOpen((prev) => !prev);
    };

    // Manual User Refresh Button
    const handleRefresh = async () => {
        await refreshUser(); // Explicit action for the user to refresh their auth state/profile
    };

    // Render Navigation Links
    const renderNavLinks = () =>
        NAV_LINKS.map(({ to, label, icon }) => (
            <li key={to}>
                <Link to={to}>
                    <FontAwesomeIcon icon={icon} /> {label}
                </Link>
            </li>
        ));

    // Render Authentication Section
    const renderAuthSection = user ? (
        <>
            <li>
                <button onClick={handleRefresh} className="refresh-button">
                    <FontAwesomeIcon icon={faUser} /> Refresh Profile
                </button>
            </li>
            <li>
                <button onClick={handleLogout} className="logout-button">
                    <FontAwesomeIcon icon={faSignOutAlt} /> Logout
                </button>
            </li>
        </>
    ) : (
        <li>
            <Link to="/signin">
                <FontAwesomeIcon icon={faSignInAlt} /> Sign In
            </Link>
        </li>
    );

    // Render Component
    return (
        <div className="header">
            {/* Logo Section */}
            <div className="logo" onClick={() => navigate("/")}>
                <img src={LOGO_PATH} alt={LOGO_ALT} />
                <Link to="/">ThesisGenius</Link>
                <sub>write smart, stress less</sub>
            </div>

            {/* Menu Toggle Button */}
            <div className="menu-toggle" onClick={toggleMenu}>
                <FontAwesomeIcon icon={isMenuOpen ? faTimes : faBars} size="lg" />
            </div>

            {/* Expandable Menu */}
            {isMenuOpen && (
                <nav className={`menu ${isMenuOpen ? "open" : ""}`}>
                    <ul>
                        {renderNavLinks()}
                        {renderAuthSection}
                    </ul>
                </nav>
            )}
        </div>
    );
  return (
    <header className="header">
      <div className="logo">
        <img
          src="/owl.png"
          alt="Logo"
          className="img img-responsive logo-class"
        />
        <Link to="/">Thesis Genius</Link>
      </div>
      <nav className="nav">
        <Link to="/dash">Dashboard</Link>
        <Link to="/about">About</Link>
        <a href="https://resources.nu.edu/Chatpage" target="_blank">
          Forum
        </a>
        {user ? (
          <button onClick={handleLogout} className="btn btn-danger">
            Logoff
          </button>
        ) : (
          <Link to="/signin">Sign in</Link>
        )}
      </nav>
    </header>
  );
};

export default ExpandableMenu;