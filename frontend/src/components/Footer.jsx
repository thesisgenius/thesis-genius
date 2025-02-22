// src/components/Footer.jsx

import React from "react";
import { Link } from "react-router-dom";
import "../styles/Footer.css";

const Footer = () => {
  return (
    <footer className="footer bg-dark text-white py-4">
      <div className="container">
        <div className="row">
          {/* Quick Links */}
          <div className="col-md-6">
            <h2>Quick Links</h2>
            <ul className="list-unstyled">
              <li>
                <Link to="/about" className="footer-link">About Us</Link>
              </li>
              <li>
                <a
                  href="https://apastyle.apa.org/style-grammar-guidelines"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="footer-link"
                >
                  APA Guidelines
                </a>
                (opens a new tab)
              </li>
              <li>
                <a
                  href="https://resources.nu.edu/Chatpage"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="footer-link"
                >
                  Forum
                </a>
                (opens a new tab)
              </li>
            </ul>
          </div>

          {/* Contact Info */}
          <div className="col-md-6">
            <h2>Contact Info</h2>
            <p>
              Email:{" "}
              <a href="mailto:thesis-genius@theses.dev" className="footer-link">
                thesis-genius@theses.dev
              </a>
            </p>
            <p>Phone: +1 (123) 456-7890</p>
          </div>
        </div>

        {/* Divider Line */}
        <hr className="footer-divider" />

        <div className="footer-bottom text-center mt-3">
          <p>&copy; {new Date().getFullYear()} Thesis Genius. All Rights Reserved.</p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
