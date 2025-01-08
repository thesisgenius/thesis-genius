import React from "react";
import { Link } from "react-router-dom";
import "./../styles/NotFound.css";

const NotFound = () => {
    return (
        <div className="notfound-container">
            <h1>404 - Page Not Found</h1>
            <p>Sorry, the page you are looking for does not exist.</p>
            <Link to="/dashboard" className="back-link">
                Go Back to Dashboard
            </Link>
        </div>
    );
};

export default NotFound;