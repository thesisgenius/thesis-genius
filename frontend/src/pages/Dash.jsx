import React from "react";
import { Accordion } from "react-bootstrap";
import "bootstrap/dist/css/bootstrap.min.css";
import { Link } from "react-router-dom";

const Dash = () => {
  return (
    <div className="container">
      <div className="row">
        <h3 className="text-center">Dashboard</h3>
      </div>
      <h5>Take these steps in order: </h5>
      <Accordion defaultActiveKey="0">
        <p className="textbox">
          <Link to="/title">1. Title Page</Link>
        </p>
        <p className="textbox">
          <Link to="/abstract">2. Abstract</Link>
        </p>
        <p className="textbox">
          <Link to="/table-of-contents">3. Table of Contents</Link>
        </p>
        <p className="textbox">
          <Link to="/list-of-figures">4. List of Figures</Link>
        </p>
        <p className="textbox">
          <Link to="/list-of-tables">5. List of Tables</Link>
        </p>
        <Accordion.Item eventKey="5">
          <Accordion.Header>
            <Link to="/body">6. Body (4-6 sections)</Link>{" "}
          </Accordion.Header>
          <Accordion.Body>
            <ul>
              <li>Literature Review</li>
              <li>Methodology</li>
              <li>Results</li>
              <li>Discussion</li>
              <li>Conclusion</li>
            </ul>
          </Accordion.Body>
        </Accordion.Item>
        <p className="textbox">
          <Link to="/appendices">7. Appendices</Link>
        </p>
        <p className="textbox">
          <Link to="/references">8. References</Link>
        </p>
        <p className="textbox">
          <Link to="/other-info">9. Other Info</Link>
        </p>
      </Accordion>
    </div>
  );
};

export default Dash;
