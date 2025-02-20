// src/components/Header.jsx

import React, { useState, useEffect } from "react";
import { Link, useNavigate, useLocation } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faSignOutAlt,
  faSignInAlt,
  faUserPlus,
  faHome,
  faComments,
  faBars,
  faTimes,
  faCog,
  faEnvelope,
} from "@fortawesome/free-solid-svg-icons";
import "../styles/Header.css";

const LOGO_PATH = "/owl.png";
const LOGO_ALT = "ThesisGenius";

const NAV_LINKS_PUBLIC = [
  { to: "/", label: "Home", icon: faHome },
  { to: "/chat", label: "Chat With AI", icon: faComments },
  { to: "/contact", label: "Contact Us", icon: faEnvelope }, // ✅ Contact Us added under Chat With AI
];

const ExpandableMenu = () => {
  const { user, signOut } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  useEffect(() => {
    setIsMenuOpen(false); // Close menu when route changes
  }, [location]);

  const handleLogout = () => {
    signOut();
    navigate("/"); // Redirect to Home after logout
  };

  const toggleMenu = () => setIsMenuOpen((prev) => !prev);

  const renderNavLinks = () => (
    <>
      {NAV_LINKS_PUBLIC.map(({ to, label, icon }) => (
        <li key={to}>
          <Link to={to} className="menu-link">
            <FontAwesomeIcon icon={icon} /> {label}
          </Link>
        </li>
      ))}

      {user && (
        <>
          <li>
            <button className="menu-link" onClick={() => navigate("/dashboard")}>
              <FontAwesomeIcon icon={faComments} /> Dashboard
            </button>
          </li>
          <li>
            <button className="menu-link" onClick={() => navigate("/settings")}>
              <FontAwesomeIcon icon={faCog} /> Account Settings
            </button>
          </li>
        </>
      )}
    </>
  );

  return (
    <div className="header">
      {/* Logo */}
      <div className="logo" onClick={() => navigate("/")}>
        <img src={LOGO_PATH} alt={LOGO_ALT} style={{ width: "50px" }} />
        <Link to="/">ThesisGenius</Link>
        <sub>write smart, stress less</sub>
      </div>

      {/* Hamburger Menu */}
      <div className="menu-toggle" onClick={toggleMenu}>
        <FontAwesomeIcon icon={isMenuOpen ? faTimes : faBars} size="lg" />
      </div>

      {/* Expandable Menu */}
      {isMenuOpen && (
        <nav className="menu open">
          <ul>
            {renderNavLinks()}
            {user ? (
              <li>
                <button onClick={handleLogout} className="logout-button">
                  <FontAwesomeIcon icon={faSignOutAlt} /> Logout
                </button>
              </li>
            ) : (
              <>
                <li>
                  <Link to="/signin" onClick={() => setIsMenuOpen(false)}>
                    <FontAwesomeIcon icon={faSignInAlt} /> Sign In
                  </Link>
                </li>
                <li>
                  <Link to="/signup" onClick={() => setIsMenuOpen(false)}>
                    <FontAwesomeIcon icon={faUserPlus} /> Sign Up
                  </Link>
                </li>
              </>
            )}
          </ul>
        </nav>
      )}
    </div>
  );
};

export default ExpandableMenu;
