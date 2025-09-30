import { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { useMutation, useQuery } from "@tanstack/react-query";
import Navbar from "./../../components/Navbar";
import {
  updateApplication,
  getFormById,
  getApplicationById,
} from "../../utils/api";
import "./../../style/ApplicationEdit.css";

export default function ApplicationRevise() {
  const navigate = useNavigate();
  const { formId, applicationId } = useParams();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [formData, setFormData] = useState(null);
  const [applicationData, setApplicationData] = useState(null);
  const [formValues, setFormValues] = useState({});

  const numericFormId = Number.parseInt(formId, 10);
  const numericAppId = Number.parseInt(applicationId, 10);
  const areIdsValid =
    Number.isInteger(numericFormId) && Number.isInteger(numericAppId);

  // Fetch existing application data
  const {
    data: application,
    error: applicationError,
    isLoading: applicationLoading,
  } = useQuery({
    queryKey: ["application", numericFormId, numericAppId],
    queryFn: () => getApplicationById(numericFormId, numericAppId),
    enabled: areIdsValid,
    retry: 1,
  });

  const getFormByIdMutation = useMutation({
    mutationFn: getFormById,
    onSuccess: (data) => {
      setFormData(data);
      setLoading(false);

      // Pre-fill form values with existing application data
      if (data?.blocks && typeof data.blocks === "object" && applicationData) {
        const initialValues = {};
        Object.keys(data.blocks).forEach((key) => {
          // Get existing value from application payload
          const existingValue =
            applicationData.jsonPayload?.[key]?.value ||
            applicationData.payload?.[key]?.value ||
            "";
          initialValues[`block_${key}`] = existingValue;
        });
        setFormValues(initialValues);
      }
    },
    onError: (error) => {
      setError(error.message || "Fehler beim Laden des Formulars");
      setLoading(false);
    },
  });

  // Set application data and trigger form loading when application is fetched
  useEffect(() => {
    if (application) {
      setApplicationData(application);

      // Load form data after we have the application
      if (!formId || formId === "undefined") {
        setError("Keine Formular-ID gefunden");
        return;
      }

      if (!areIdsValid) {
        setError("Ungültige IDs");
        return;
      }

      setLoading(true);
      setError("");
      getFormByIdMutation.mutate(numericFormId);
    }
  }, [application, formId, areIdsValid]);

  // Handle application loading errors
  useEffect(() => {
    if (applicationError) {
      setError(applicationError.message || "Fehler beim Laden des Antrags");
    }
  }, [applicationError]);

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

    updateApplicationMutation.mutate({
      application_id: numericAppId,
      form_id: numericFormId,
      payload: jsonPayload,
    });
  };

  // Mutation to update application
  const updateApplicationMutation = useMutation({
    mutationFn: updateApplication,
    onSuccess: () => {
      alert("Antrag erfolgreich überarbeitet!");
      navigate(`/applications/${formId}/${applicationId}`);
    },
    onError: (error) => {
      setError(error.message || "Fehler beim Überarbeiten des Antrags");
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

  // Show loading state
  if (applicationLoading || loading) {
    return (
      <>
        <Navbar />
        <div className="application-edit-container">
          <div className="application-edit-card">
            <div className="loading-message">
              <p>Antrag und Formular werden geladen...</p>
            </div>
          </div>
        </div>
      </>
    );
  }

  // Show error state
  if (error || applicationError) {
    return (
      <>
        <Navbar />
        <div className="application-edit-container">
          <div className="application-edit-card">
            <div className="error-message">
              <p>{error || applicationError?.message}</p>
              <button
                onClick={() => navigate("/applicant")}
                className="application-edit-button"
              >
                Zurück
              </button>
            </div>
          </div>
        </div>
      </>
    );
  }

  // Show not found state
  if (!application) {
    return (
      <>
        <Navbar />
        <div className="application-edit-container">
          <div className="application-edit-card">
            <div className="error-message">
              <p>Antrag nicht gefunden</p>
              <button
                onClick={() => navigate("/applicant")}
                className="application-edit-button"
              >
                Zurück
              </button>
            </div>
          </div>
        </div>
      </>
    );
  }

  const applicationTitle =
    application?.title ||
    application?.form_name ||
    formData?.form_name ||
    `Antrag #${application?.id}`;

  return (
    <>
      <Navbar />
      <div className="application-edit-container">
        <div className="application-edit-card">
          <h2 className="application-edit-title">
            {`${applicationTitle} - Antrag überarbeiten`}
          </h2>

          {formData && (
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
                  disabled={updateApplicationMutation.isPending}
                >
                  {updateApplicationMutation.isPending
                    ? "Wird gespeichert..."
                    : "Überarbeitete Version einreichen"}
                </button>
                <button
                  className="application-edit-button"
                  onClick={() =>
                    navigate(`/applications/${formId}/${applicationId}`)
                  }
                  type="button"
                >
                  Zurück zur Ansicht
                </button>
                <button
                  className="application-edit-button"
                  onClick={() => navigate("/applicant")}
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
