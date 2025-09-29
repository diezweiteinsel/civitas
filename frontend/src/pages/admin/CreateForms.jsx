// pflichtenheft-user-interface mockup under "Editing a from/Adding trigger-conditionals"
// Diese Seite soll "ViewForms.jsx" aufgerufen werden und soll die Möglichkeit bieten, ein neues Formular zu erstellen.

import React, { useState } from "react";
import "./../../style/CreateForms.css";
import Navbar from "../../components/Navbar";
import { Role } from "../../utils/const";
import { useMutation } from "@tanstack/react-query";
import { createForm } from "../../utils/api";
import { useNavigate } from "react-router-dom";

const dataTypes = ["String", "Date", "Float", "Boolean", "Number"];

export default function CreateForms() {
  const [formTitle, setFormTitle] = useState("");
  const [formFields, setFormFields] = useState([
    { id: "1", name: "Neues Feld 1", type: "Text" },
  ]);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const getNextId = () => (Date.now() + Math.random()).toString();

  const handleForm = (event, index) => {
    const { name, value } = event.target;
    let data = [...formFields];
    data[index][name] = value;
    setFormFields(data);
  };

  const addFields = () => {
    let newField = {
      id: getNextId(),
      name: `Neues Feld ${formFields.length + 1}`,
      type: "String",
    };
    setFormFields([...formFields, newField]);
  };

  const removeFields = (id) => {
    const data = formFields.filter((field) => field.id !== id);
    setFormFields(data);
  };

  // Mutation for creating a form
  const createFormMutation = useMutation({
    mutationFn: createForm,
    onSuccess: (data) => {
      setError("");
      alert("Meldeform wurde erflogreich erstellt!");
      navigate("/admin");
    },
    onError: (error) => {
      setError(error.message || "Form creation failed. Please try again.");
      console.error("Form creation error:", error);
    },
  });

  // Handle form save
  const handleSave = () => {
    if (!formTitle.trim()) {
      setError("Bitte geben Sie einen Titel für das Formular ein.");
      return;
    }

    if (formFields.length === 0) {
      setError("Bitte fügen Sie mindestens ein Feld hinzu.");
      return;
    }

    const formData = {
      form_name: formTitle.trim(),
      blocks: formFields.reduce((acc, field, index) => {
        acc[(index + 1).toString()] = {
          label: field.name,
          data_type: field.type.toUpperCase(),
        };
        return acc;
      }, {}),
    };

    // Call the API to create the form
    createFormMutation.mutate(formData);
  };

  const handleImport = () => {
    alert("Meldeform wurde erflogreich importiert TODO"); //TODO:
  };

  return (
    <div>
      <Navbar role={Role.ADMIN} />
      <div className="form-creation-container">
        <div className="form-creation-header">
          <h2>Neues Meldeform erstellen</h2>
        </div>

        <div className="form-title-section">
          <label htmlFor="form-title">Formular Titel:</label>
          <input
            id="form-title"
            type="text"
            placeholder="Geben Sie den Titel des Formulars ein..."
            value={formTitle}
            onChange={(e) => setFormTitle(e.target.value)}
            className="form-title-input"
          />
        </div>

        <div className="form-actions">
          <button className="create-button" onClick={addFields}>
            Neues Feld Hinzufügen
          </button>
          <button className="import-button" onClick={handleImport}>
            Meldeform Importieren
          </button>
        </div>

        <div className="fields-container">
          {formFields.map((field, index) => (
            <div key={field.id} className="field-row">
              <input
                name="name"
                placeholder="Feldname eingeben..."
                value={field.name}
                onChange={(e) => handleForm(e, index)}
              />

              <select
                name="type"
                value={field.type}
                onChange={(e) => handleForm(e, index)}
              >
                {dataTypes.map((type) => (
                  <option key={type} value={type}>
                    {type}
                  </option>
                ))}
              </select>

              <button
                className="remove-button"
                onClick={() => removeFields(field.id)}
                title="Feld entfernen"
              >
                Entfernen
              </button>
            </div>
          ))}
        </div>

        {error && <div className="error-message">{error}</div>}

        <button
          className="save-button"
          onClick={handleSave}
          disabled={createFormMutation.isPending}
        >
          {createFormMutation.isPending
            ? "Speichert..."
            : "Meldeform Speichern"}
        </button>
      </div>
    </div>
  );
}
