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

const LOGO_PATH = "/tg-white.png";
const LOGO_ALT = "ThesisGenius";
const NAV_LINKS = [
    { to: "/dashboard", label: "Dashboard", icon: faDashboard },
    { to: "/forum", label: "Forum", icon: faComments },
    { to: "/signup", label: "Sign Up", icon: faUser },
];

const ExpandableMenu = () => {
    const { user, signOut } = useAuth();
    const navigate = useNavigate();
    const [isMenuOpen, setIsMenuOpen] = useState(false); // State to control menu expand/collapse

    const handleLogout = () => {
        signOut();
        navigate("/");
    };

    const toggleMenu = () => {
        setIsMenuOpen((prev) => !prev); // Toggle menu state
    };

    const renderNavLinks = () =>
        NAV_LINKS.map(({ to, label, icon }) => (
            <li key={to}>
                <Link to={to}>
                    <FontAwesomeIcon icon={icon} /> {label}
                </Link>
            </li>
        ));

    const renderAuthSection = user ? (
        <li>
            <button onClick={handleLogout} className="logout-button">
                <FontAwesomeIcon icon={faSignOutAlt} /> Logout
            </button>
        </li>
    ) : (
        <li>
            <Link to="/signin">
                <FontAwesomeIcon icon={faSignInAlt} /> Sign In
            </Link>
        </li>
    );

    return (
        <div className="header">
            {/* Logo Section on the Left */}
            <div className="logo">
                <img src={LOGO_PATH} alt={LOGO_ALT} onClick={() => "/"}/>
                <Link to="/">ThesisGenius</Link>
                <sub>write smart, stress less</sub>
            </div>

            {/* Hamburger Menu on the Right */}
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