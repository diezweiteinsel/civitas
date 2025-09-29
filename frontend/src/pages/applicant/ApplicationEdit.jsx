import "./../../style/ApplicationEdit.css";
import React, { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import Navbar from "./../../components/Navbar";
import { Role } from "../../utils/const";
import { useMutation } from "@tanstack/react-query";
import { createApplication, getFormById } from "../../utils/api";

export default function ApplicationEdit() {
  const navigate = useNavigate();
  const { id: formId } = useParams(); // The route parameter is 'id', but we'll use it as formId

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [formData, setFormData] = useState(null);
  const [formValues, setFormValues] = useState({});

  const getFormByIdMutation = useMutation({
    mutationFn: getFormById,
    onSuccess: (data) => {
      console.log("Form data received:", data); // Debug log
      setFormData(data);
      setLoading(false);
      // Initialize form values based on form blocks (dictionary/object)
      if (data && data.blocks && typeof data.blocks === "object") {
        const initialValues = {};
        Object.keys(data.blocks).forEach((key) => {
          initialValues[`block_${key}`] = "";
        });
        setFormValues(initialValues);
      } else {
        console.warn("Form blocks not found or not an object:", data.blocks);
        setFormValues({});
      }
    },
    onError: (error) => {
      setError(error.message || "Failed to fetch form");
      setLoading(false);
    },
  });

  useEffect(() => {
    if (formId && formId !== "undefined") {
      setLoading(true);
      setError("");
      const numericId = parseInt(formId, 10);
      if (isNaN(numericId)) {
        setError("Invalid form ID");
        setLoading(false);
        return;
      }
      getFormByIdMutation.mutate(numericId);
    } else {
      setError("No form ID provided");
      setLoading(false);
    }
  }, [formId]);

  const handleChange = (e) => {
    const { name, value, type } = e.target;
    let newValue = value;

    if (type === "number") {
      newValue = value.replace(/[^0-9.]/g, "");
    }

    setFormValues((prev) => ({
      ...prev,
      [name]: newValue,
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    // Build payload from form values and blocks (dictionary/object)
    const jsonPayload = {};
    if (formData && formData.blocks && typeof formData.blocks === "object") {
      Object.keys(formData.blocks).forEach((key) => {
        const block = formData.blocks[key];
        jsonPayload[key] = {
          label: block.label || `Field ${key}`,
          value: formValues[`block_${key}`] || "",
          data_type: block.data_type,
        };
      });
    }

    const applicationData = {
      form_id: parseInt(formId, 10),
      payload: jsonPayload,
    };

    console.log("Submitting application:", applicationData);
    createApplicationMutation.mutate(applicationData);
  };

  const createApplicationMutation = useMutation({
    mutationFn: createApplication,
    onSuccess: (data) => {
      setError("");
      alert("Antrag erfolgreich erstellt!");
      setSuccess("Antrag erfolgreich erstellt! Weiterleitung...");
      console.log("Antrag erfolgreich erstellt:", data);

      navigate("/applicant");
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

  const renderFormField = (block, key) => {
    const fieldName = `block_${key}`;
    const fieldValue = formValues[fieldName] || "";
    const label = block.label || `Field ${key}`;

    switch (block.data_type) {
      case "TEXT":
        return (
          <div key={key} className="form-group">
            <label htmlFor={fieldName}>{label}:</label>
            <input
              type="text"
              id={fieldName}
              name={fieldName}
              value={fieldValue}
              onChange={handleChange}
              required={block.required || false}
            />
          </div>
        );

      case "FLOAT":
      case "INTEGER":
      case "NUMBER":
        return (
          <div key={key} className="form-group">
            <label htmlFor={fieldName}>{label}:</label>
            <input
              type="number"
              step={block.data_type === "FLOAT" ? "0.01" : "1"}
              id={fieldName}
              name={fieldName}
              value={fieldValue}
              onChange={handleChange}
              required={block.required || false}
            />
          </div>
        );

      case "DATE":
        return (
          <div key={key} className="form-group">
            <label htmlFor={fieldName}>{label}:</label>
            <input
              type="date"
              id={fieldName}
              name={fieldName}
              value={fieldValue}
              onChange={handleChange}
              required={block.required || false}
            />
          </div>
        );

      case "EMAIL":
        return (
          <div key={key} className="form-group">
            <label htmlFor={fieldName}>{label}:</label>
            <input
              type="email"
              id={fieldName}
              name={fieldName}
              value={fieldValue}
              onChange={handleChange}
              required={block.required || false}
            />
          </div>
        );

      case "TEXTAREA":
      case "LONG_TEXT":
        return (
          <div key={key} className="form-group">
            <label htmlFor={fieldName}>{label}:</label>
            <textarea
              id={fieldName}
              name={fieldName}
              value={fieldValue}
              onChange={handleChange}
              required={block.required || false}
            />
          </div>
        );

      default:
        return (
          <div key={key} className="form-group">
            <label htmlFor={fieldName}>{label}:</label>
            <input
              type="text"
              id={fieldName}
              name={fieldName}
              value={fieldValue}
              onChange={handleChange}
              required={block.required || false}
            />
          </div>
        );
    }
  };

  return (
    <>
      <Navbar role={Role.APPLICANT} />
      <div className="application-edit-container">
        <div className="application-edit-card">
          <h2 className="application-edit-title">
            {formData
              ? `${formData.form_name} - Antrag bearbeiten`
              : "Antrag bearbeiten"}
          </h2>

          {loading && (
            <div className="loading-message">
              <p>Formular wird geladen...</p>
            </div>
          )}

          {error && (
            <div className="error-message">
              <p>Fehler: {error}</p>
              <button
                onClick={() => navigate("/applicant/submit")}
                className="application-edit-button"
              >
                Zurück
              </button>
            </div>
          )}

          {success && (
            <div className="success-message">
              <p>{success}</p>
            </div>
          )}

          {formData && !loading && (
            <form className="application-edit-form" onSubmit={handleSubmit}>
              {formData.blocks &&
              typeof formData.blocks === "object" &&
              Object.keys(formData.blocks).length > 0 ? (
                Object.keys(formData.blocks).map((key) =>
                  renderFormField(formData.blocks[key], key)
                )
              ) : (
                <div className="no-fields-message">
                  <p>Dieses Formular hat keine konfigurierten Felder.</p>
                </div>
              )}

              <div className="application-edit-buttons">
                <button
                  className="application-edit-button"
                  type="submit"
                  disabled={createApplicationMutation.isPending}
                >
                  {createApplicationMutation.isPending
                    ? "Wird gespeichert..."
                    : "Speichern"}
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
          )}
        </div>
      </div>
    </>
  );
}
