import React from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import "../styles/Header.css";

const Header = () => {
    const { user, signOut } = useAuth();
    const navigate = useNavigate();

    const handleLogout = () => {
        signOut();
        navigate("/signin");
    };

    return (
        <header className="header">
            <div className="logo">
                <Link to="/">Thesis Genius</Link>
            </div>
            <nav className="nav">
                <Link to="/dashboard">Dashboard</Link>
                <Link to="/forum">Forum</Link>
                {user ? (
                    <button onClick={handleLogout} className="logout-button">
                        Logout
                    </button>
                ) : (
                    <Link to="/signin">Sign In</Link>
                )}
            </nav>
        </header>
    );
};

export default Header;