import { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { useMutation } from "@tanstack/react-query";
import Navbar from "./../../components/Navbar";
import { Role } from "../../utils/const";
import { createApplication, getFormById } from "../../utils/api";
import "./../../style/ApplicationEdit.css";

export default function ApplicationEdit() {
  const navigate = useNavigate();
  const { id: formId } = useParams();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [formData, setFormData] = useState(null);
  const [formValues, setFormValues] = useState({});

  const getFormByIdMutation = useMutation({
    mutationFn: getFormById,
    onSuccess: (data) => {
      setFormData(data);
      setLoading(false);

      if (data?.blocks && typeof data.blocks === "object") {
        const initialValues = {};
        Object.keys(data.blocks).forEach((key) => {
          initialValues[`block_${key}`] = "";
        });
        setFormValues(initialValues);
      }
    },
    onError: (error) => {
      setError(error.message || "Fehler beim Laden des Formulars");
      setLoading(false);
    },
  });

  // Fetch form data when component mounts or formId changes
  useEffect(() => {
    if (!formId || formId === "undefined") {
      setError("Keine Formular-ID gefunden");
      return;
    }

    const numericId = parseInt(formId, 10);
    if (isNaN(numericId)) {
      setError("Ungültige Formular-ID");
      return;
    }

    setLoading(true);
    setError("");
    getFormByIdMutation.mutate(numericId);
  }, [formId]);

  // Handle input changes
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormValues((prev) => ({ ...prev, [name]: value }));
  };

  // Handle form submission
  const handleSubmit = (e) => {
    e.preventDefault();

    const jsonPayload = {};
    Object.keys(formData.blocks || {}).forEach((key) => {
      const block = formData.blocks[key];
      jsonPayload[key] = {
        label: block.label,
        value: formValues[`block_${key}`] || "",
        data_type: block.data_type,
      };
    });

    createApplicationMutation.mutate({
      form_id: parseInt(formId, 10),
      payload: jsonPayload,
    });
  };

  // Mutation to create application
  const createApplicationMutation = useMutation({
    mutationFn: createApplication,
    onSuccess: () => {
      alert("Antrag erfolgreich erstellt!");
      navigate("/applicant");
    },
    onError: (error) => {
      setError(error.message || "Fehler beim Erstellen des Antrags");
    },
  });

  // Render form fields based on formData.blocks
  const renderFormField = (block, key) => {
    const fieldName = `block_${key}`;
    const fieldValue = formValues[fieldName] || "";
    const { label, data_type, required } = block;

    const fieldProps = {
      id: fieldName,
      name: fieldName,
      value: fieldValue,
      onChange: handleChange,
      required: required || false,
    };

    const renderInput = () => {
      switch (data_type) {
        case "FLOAT":
          return <input type="number" step="0.01" {...fieldProps} />;
        case "INTEGER":
        case "NUMBER":
          return <input type="number" step="1" {...fieldProps} />;
        case "DATE":
          return <input type="date" {...fieldProps} />;
        case "EMAIL":
          return <input type="email" {...fieldProps} />;
        case "TEXTAREA":
        case "LONG_TEXT":
          return <textarea {...fieldProps} />;
        default:
          return <input type="text" {...fieldProps} />;
      }
    };

    return (
      <div key={key} className="form-group">
        <label htmlFor={fieldName}>{label}:</label>
        {renderInput()}
      </div>
    );
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
              <p>{error}</p>
              <button
                onClick={() => navigate("/applicant/submit")}
                className="application-edit-button"
              >
                Zurück
              </button>
            </div>
          )}

          {formData && !loading && (
            <form className="application-edit-form" onSubmit={handleSubmit}>
              {Object.keys(formData.blocks || {}).length > 0 ? (
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
