import React, { useState } from "react";
import "../styles/ContactUs.css";

const ContactPage = () => {
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    phone: "",
    contactType: "other",
    comments: "",
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    // Construct email subject and body
    const subject = `Contact Request from ${formData.name}`;
    const body = `
Name: ${formData.name}
Phone: ${formData.phone}
Email: ${formData.email}
Preferred Contact Method: ${formData.contactType}

Comments:
${formData.comments}
    `;

    // Encode and open the mailto link
    const mailtoLink = `mailto:Thesis-Genius@theses.dev?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
    window.location.href = mailtoLink;
  };

  return (
    <div className="contact-container">
      <header className="contact-hero">
        <h1>Contact Us</h1>
        <p>We're here to assist you! Fill out the form and we'll get back to you.</p>
      </header>

      <section className="contact-form-section">
        <form className="contact-form" onSubmit={handleSubmit}>
          <label>
            Name:
            <input
              type="text"
              name="name"
              placeholder="Your Name"
              value={formData.name}
              onChange={handleChange}
              required
            />
          </label>

          <label>
            Email:
            <input
              type="email"
              name="email"
              placeholder="Your Email"
              value={formData.email}
              onChange={handleChange}
              required
            />
          </label>

          <label>
            Phone:
            <input
              type="tel"
              name="phone"
              placeholder="Your Phone Number"
              value={formData.phone}
              onChange={handleChange}
            />
          </label>

          <label>
            Preferred Contact Method:
            <select name="contactType" value={formData.contactType} onChange={handleChange}>
              <option value="email">Email</option>
              <option value="phone">Phone</option>
              <option value="other">Other</option>
              <option value="no-contact">No Contact</option>
            </select>
          </label>

          <label>
            Comments:
            <textarea
              name="comments"
              placeholder="Enter your comments here..."
              rows="10"
              value={formData.comments}
              onChange={handleChange}
            />
          </label>

          <button type="submit" className="submit-button">Submit</button>
        </form>
      </section>
    </div>
  );
};

export default ContactPage;