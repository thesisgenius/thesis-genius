import React from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import "../styles/Header.css";

const Header = () => {
  const { user, signOut } = useAuth();
  const navigate = useNavigate();

  const temp = "temp";

  const handleLogout = () => {
    signOut();
    navigate("/signin");
  };

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

export default Header;
