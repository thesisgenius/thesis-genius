import React from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap/dist/js/bootstrap.bundle.min.js";
import FadingBanner from "../components/FadingBanner";

const About = () => {
  return (
    <div className="container py-5">
      {/* FadingBanner at the top */}
      <div className="mb-5">
        <FadingBanner />
      </div>

      <div className="row justify-content-center">
        <div className="col-lg-10 text-center">
          {/* Main Title */}
          <h2 className="display-4 fw-bold mb-4">About Thesis Genius</h2>
          <p className="lead text-muted">
            Thesis Genius is a comprehensive service designed to help students
            and researchers manage their thesis projects efficiently. Our
            platform offers a range of tools and resources to streamline the
            thesis writing process, from organizing research materials to
            tracking progress and deadlines.
          </p>
          <hr className="my-5" />

          {/* Mission Section */}
          <section className="mb-5">
            <h3 className="fw-semibold text-primary">Our Mission</h3>
            <p className="mt-3 text-muted">
              We aim to empower scholars worldwide by simplifying the thesis
              journey, fostering academic excellence, and encouraging impactful
              research.
            </p>
          </section>

          {/* Core Values Section */}
          <section className="mb-5">
            <h3 className="fw-semibold text-primary">Core Values</h3>
            <ul className="list-unstyled mt-3 text-muted">
              <li className="my-2">
                <strong>Integrity:</strong> Upholding the highest standards of
                academic honesty.
              </li>
              <li className="my-2">
                <strong>Innovation:</strong> Continuously refining our tools to
                meet evolving research needs.
              </li>
              <li className="my-2">
                <strong>Collaboration:</strong> Partnering with educational
                institutions and experts to enhance support.
              </li>
              <li className="my-2">
                <strong>Excellence:</strong> Striving to deliver user-friendly
                experiences and reliable, high-quality service.
              </li>
            </ul>
          </section>

          {/* Team or Leadership Section (Optional) */}
          <section className="mb-5">
            <h3 className="fw-semibold text-primary">Meet the Team</h3>
            <p className="mt-3 text-muted">
              Our dedicated group of educators, researchers, and developers is
              committed to guiding you through every step of your thesis
              process.
            </p>
            {/* Optionally include headshots or team bios here */}
          </section>

          {/* Achievements (Optional) */}
          <section className="mb-5">
            <h3 className="fw-semibold text-primary">Key Achievements</h3>
            <ul className="list-unstyled mt-3 text-muted">
              <li className="my-2">
                <strong>10,000+</strong> successful thesis submissions managed
              </li>
              <li className="my-2">
                Recognized by <em>Academic Weekly</em> (2024)
              </li>
              <li className="my-2">
                Partnered with leading universities to streamline thesis
                requirements
              </li>
            </ul>
          </section>

          {/* Call To Action / Contact */}
          <section>
            <h3 className="fw-semibold text-primary">Ready to Get Started?</h3>
            <p className="mt-3 text-muted">
              Let Thesis Genius handle the administrative side of your thesis so
              you can focus on delivering remarkable research.
            </p>
            <a href="/signup" className="btn btn-primary btn-lg mt-3">
              Join Today
            </a>
            <div className="mt-4">
              <p className="text-muted">
                Have any questions? Reach us at{" "}
                <a href="mailto:info@thesisgenius.com">
                  support@thesisgenius.com
                </a>
              </p>
            </div>
          </section>
        </div>
      </div>
    </div>
  );
};

export default About;
