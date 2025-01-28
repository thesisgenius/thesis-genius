import React from "react";
import "../styles/Footer.css";

const Footer = () => {
    return (
        <footer className="footer">
            <p>&copy; {new Date().getFullYear()} Thesis Genius. All Rights Reserved.</p>
        </footer>
    );
};

export default Footer;