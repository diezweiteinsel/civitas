import "./../../style/ApplicationEdit.css";
import React, { useState } from "react";
import "./../../style/ApplicationEdit.css";
import Navbar from "./../../components/Navbar";
import { useNavigate } from "react-router-dom";
import { Role } from "../../utils/const";

export default function ApplicationEdit() {
  const navigate = useNavigate();

  const [form, setForm] = useState({
    name: "",
    location: "",
    date: "",
    description: "",
    amount: "",
  });

  const handleChange = (e) => {
    const { name, value, type } = e.target;
    let newValue = value;

    if (type === "number") {
      newValue = value.replace(/[^0-9.]/g, "");
    }

    setForm((prev) => ({
      ...prev,
      [name]: newValue,
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    alert("Submitted: " + JSON.stringify(form, null, 2));
  };

  return (
    <>
      <Navbar role={Role.APPLICANT} />
      <div className="application-edit-container">
        <div className="application-edit-card">
          <h2 className="application-edit-title">Edit Application</h2>
          <form className="application-edit-form" onSubmit={handleSubmit}>
            {/* Later: Use one div as a template and let them be injected when routing to this page to get the right structure of the form. */}
            <div className="form-group">
              <label htmlFor="name">Name:</label>
              <input
                type="text"
                id="name"
                name="name"
                value={form.name}
                onChange={handleChange}
                required
              />
            </div>
            <div className="form-group">
              <label htmlFor="location">Location:</label>
              <input
                type="text"
                id="location"
                name="location"
                value={form.location}
                onChange={handleChange}
                required
              />
            </div>
            <div className="form-group">
              <label htmlFor="date">Date:</label>
              <input
                type="date"
                id="date"
                name="date"
                value={form.date}
                onChange={handleChange}
                required
              />
            </div>
            <div className="form-group">
              <label htmlFor="description">Description:</label>
              <textarea
                id="description"
                name="description"
                value={form.description}
                onChange={handleChange}
                required
              />
            </div>
            <div className="form-group">
              <label htmlFor="amount">Amount (Number):</label>
              <input
                type="number"
                id="amount"
                name="amount"
                value={form.amount}
                onChange={handleChange}
                required
              />
            </div>
            <div className="application-edit-buttons">
              <button
                className="application-edit-button"
                onClick={() => navigate("/applicant/submit")}
                type="button"
              >
                Cancel
              </button>
              <button className="application-edit-button" type="submit">
                Save
              </button>
            </div>
          </form>
        </div>
      </div>
    </>
  );
}
