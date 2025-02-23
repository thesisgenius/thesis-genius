import React, { useState } from "react";
import { Link } from "react-router-dom";
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap/dist/js/bootstrap.bundle.min.js";
import FadingBanner from "../components/FadingBanner";

const Part = ({ headerText, textAreaPlaceholder }) => {
  const [text, setText] = useState("");

  const handleTextChange = (event) => {
    setText(event.target.value);
  };

  return (
    <div className="container">
      <div className="col-md-12">
        <h3 className="flex text-center">{headerText}</h3>
        <p>
          An attached example{" "}
          <a
            href="https://apastyle.apa.org/instructional-aids/abstract-keywords-guide.pdf"
            target="_blank"
          >
            example linked
          </a>
        </p>
        <p>
          Relevant APA{" "}
          <a
            href="https://apastyle.apa.org/style-grammar-guidelines"
            target="_blank"
          >
            Rules Linked
          </a>
        </p>
        <div className="row">
          <div className="col-md-6 border">
            <textarea
              className="form-control"
              style={{ height: "200px" }}
              placeholder={textAreaPlaceholder}
              value={text}
              onChange={handleTextChange}
            ></textarea>
          </div>

          <div className="col-md-6 border display-screen">
            <h4>{headerText}</h4>
            <p id="display_area">{text}</p>
          </div>
        </div>
      </div>

      <div className="row">
        <FadingBanner />
      </div>
      <div className="col-md-2">
        <Link to="/dashboard" className="btn btn-primary mb-3">
          Back to Dashboard
        </Link>
      </div>
    </div>
  );
};

export default Part;
