import React from "react";
import "../styles/Footer.css";

const Footer = () => {
  return (
    <footer className="bg-dark text-white py-4">
      <div className="container">
        <div className="row">
          <div className="col-md-6">
            <h2>Quick Links</h2>
            <ul className="list-unstyled">
              <li>
                <a href="/home" className="text-white">
                  Home
                </a>
              </li>
              <li>
                <a
                  href="https://www.nu.edu/contact-list/"
                  className="text-white"
                  target="_blank"
                >
                  Contact US
                </a>
              </li>
              <li>
                <a
                  href="https://ncu.libanswers.com/asc"
                  target="_blank"
                  className="text-white"
                >
                  FAQs
                </a>
              </li>
              <li>
                <a
                  href="https://resources.nu.edu/editing"
                  className="text-white"
                >
                  AI Assistance
                </a>
              </li>
              <li>
                <a
                  href="https://apastyle.apa.org/style-grammar-guidelines"
                  className="text-white"
                  target="_blank"
                >
                  APA Guidelines
                </a>
              </li>
            </ul>
          </div>
          <div className="col-md-6">
            <h2>Contact Us</h2>
            <p>Email: support@thesisdomain.com</p>
            <p>Phone: +123 456 7890</p>
          </div>
        </div>
        <div className="footer-bottom text-center mt-3">
          <p>
            &copy; {new Date().getFullYear()} Thesis Genius. All Rights
            Reserved.
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
