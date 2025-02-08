import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
    faUser,
    faUserCircle,
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
    { to: "https://resources.nu.edu/Chatpage", label: "Forum", icon: faComments },
    { to: "/about", label: "About", icon: faUserCircle},
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
                <img src={LOGO_PATH} alt={LOGO_ALT} style={{ width: "50px" }}/>
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
};

export default ExpandableMenu;