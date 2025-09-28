// pflichtenheft-user-interface mockup under "Editing a from/Adding trigger-conditionals"
// Diese Seite soll "ViewForms.jsx" aufgerufen werden und soll die Möglichkeit bieten, ein neues Formular zu erstellen.

import React, { useState } from "react";
import "./../../style/CreateEditForms.css";
import Navbar from "../../components/Navbar";
import { Role } from "../../utils/const";
import { useMutation } from "@tanstack/react-query";
import { createForm } from "../../utils/api";
import { useNavigate } from "react-router-dom";

const dataTypes = ["String", "Date", "Float", "Boolean", "Number"];

export default function CreateForms() {
  const [formFields, setFormFields] = useState([
    { id: "1", name: "Neues Feld 1", type: "Text", value: "" }, // needs to be implemnted as a dict instead? i dont know
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
      value: "",
    };
    setFormFields([...formFields, newField]);
  };

  const removeFields = (id) => {
    const data = formFields.filter((field) => field.id !== id);
    setFormFields(data);
  };

  const createFormMutation = useMutation({
    mutationFn: createForm,
    onSuccess: (data) => {
      setError("");
      console.log("Form creation successful:", data);
      navigate("/admin");
    },
    onError: (error) => {
      setError(error.message || "Form creation failed. Please try again.");
      console.error("Form creation error:", error);
    },
  });

  const handleSave = () => {
    if (formFields.length === 0) {
      setError("Bitte fügen Sie mindestens ein Feld hinzu.");
      return;
    }

    // Convert frontend fields to backend format
    const formData = {
      code: `form_${Date.now()}`,
      title: `Neues Formular ${new Date().toLocaleDateString()}`,
      isActive: true,
      sections: [
        {
          sectionID: 1,
          title: "Hauptabschnitt",
          buildingBlocks: formFields.map((field, index) => ({
            buildingBlockID: index + 1,
            label: field.name,
            type: field.type.toUpperCase(),
            value: field.value || "",
            isRequired: true,
          })),
        },
      ],
    };

    // Call the API to create the form
    createFormMutation.mutate(formData);
    console.log("Form data to be saved:", formData);
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
