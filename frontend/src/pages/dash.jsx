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
          <Link to="/copyright">2. Copyright Page</Link>
        </p>
        <p className="textbox">
          <Link to="/signature">3. Signature Page</Link>
        </p>
        <p className="textbox">
          <Link to="/abstract">4. Abstract Page</Link>
        </p>
        <p className="textbox">
          <Link to="/dedication">5. Dedication Page</Link>
        </p>
        <p className="textbox">
          <Link to="/acknowledgements">6. Acknowledgements Page</Link>
        </p>
        <p className="textbox">
          <Link to="/table-of-contents">7. Table of Contents</Link>
        </p>
        <p className="textbox">
          <Link to="/list-of-figures">8. List of Figures (if any)</Link>
        </p>
        <p className="textbox">
          <Link to="/list-of-tables">9. List of Tables (if any)</Link>
        </p>
        <Accordion.Item eventKey="5">
          <Accordion.Header>
            <Link to="/body">10. Body (4-6 sections)</Link>{" "}
          </Accordion.Header>
          <Accordion.Body>
            <ol>
              <li>Chapter I: Introduction</li>
              <li>Chapter II: Literature Review</li>
              <li>Chapter III: Methods</li>
              <li>Chapter IV: Results</li>
              <li>Chapter V: Discussion</li>
            </ol>
          </Accordion.Body>
        </Accordion.Item>
        <p className="textbox">
          <Link to="/references">11. References</Link>
        </p>
        <p className="textbox">
          <Link to="/appendices">12. Appendices</Link>
        </p>

        <p className="textbox">
          <Link to="/other-info">13. Other Info</Link>
        </p>
      </Accordion>
    </div>
  );
};

export default Dash;
