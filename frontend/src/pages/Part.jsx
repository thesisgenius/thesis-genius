import React from "react";
import { Link } from "react-router-dom";
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap/dist/js/bootstrap.bundle.min.js";
import FadingBanner from "../components/FadingBanner";

const Part = ({ headerText, textAreaPlaceholder }) => {
  return (
    <div className="container">
      <div className="col-md-12">
        <h3 className="flex text-center">{headerText}</h3>
        <p>
          An attached example <a href="#">example linked</a>
        </p>
        <p>
          Relevant AP <a href="">Rules Linked</a>
        </p>
        <div className="row">
          <div className="col-md-6 border">
            <textarea
              className="form-control"
              style={{ height: "200px" }}
              placeholder={textAreaPlaceholder}
            ></textarea>
          </div>

          <div className="col-md-6 border display-screen">
            <h4>{headerText}</h4>
            <p></p>
          </div>
        </div>
      </div>

      <div className="row">
        <FadingBanner />
      </div>
      <div className="col-md-2">
        <Link to="/dash" className="btn btn-primary mb-3">
          Back to Dashboard
        </Link>
      </div>
    </div>
  );
};

export default Part;
