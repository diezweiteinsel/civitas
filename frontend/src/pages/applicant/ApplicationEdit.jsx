import "./../../style/ApplicationEdit.css";
import React, { useState } from "react";
import "./../../style/ApplicationEdit.css";
import Navbar from "./../../components/Navbar";
import { useNavigate } from "react-router-dom";
import { Role } from "../../utils/const";
import { useMutation } from "@tanstack/react-query";
import { createApplication } from "../../utils/api";

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
    const applicationData = {
      user_id: 1,
      form_id: 1,
      jsonPayload: {
        0: {
          label: "Name",
          value: form.name,
        },
        1: {
          label: "Standort",
          value: form.location,
        },
        2: {
          label: "Datum",
          value: form.date,
        },
        3: {
          label: "Beschreibung",
          value: form.description,
        },
        4: {
          label: "Betrag",
          value: form.amount,
        },
      },
    };
    createApplicationMutation.mutate(applicationData);
    e.preventDefault();
    console.log("Versuch Antrag zu stellen:", applicationData);
  };

  const createApplicationMutation = useMutation({
    mutationFn: createApplication,
    onSuccess: (data) => {
      setError("");
      alert("Antrag erfolgreich erstellt!");
      setSuccess("Antrag erfolgreich erstellt! Weiterleitung...");
      console.log("Antrag erfolgreich erstellt:", data);

      navigate("/");
    },
    onError: (error) => {
      setSuccess("");
      setError(
        error.message ||
          "Antragserstellung fehlgeschlagen. Bitte versuchen Sie es erneut."
      );
      console.error("Fehler bei Antragserstellung:", error);
    },
  });

  return (
    <>
      <Navbar role={Role.APPLICANT} />
      <div className="application-edit-container">
        <div className="application-edit-card">
          <h2 className="application-edit-title">Antrag bearbeiten</h2>
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
              <label htmlFor="location">Standort:</label>
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
              <label htmlFor="date">Datum:</label>
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
              <label htmlFor="description">Beschreibung:</label>
              <textarea
                id="description"
                name="description"
                value={form.description}
                onChange={handleChange}
                required
              />
            </div>
            <div className="form-group">
              <label htmlFor="amount">Betrag (Zahl):</label>
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
              <button className="application-edit-button" type="submit">
                Speichern
              </button>
              <button
                className="application-edit-button"
                onClick={() => navigate("/applicant/submit")}
                type="button"
              >
                Abbrechen
              </button>
            </div>
          </form>
        </div>
      </div>
    </>
  );
}
