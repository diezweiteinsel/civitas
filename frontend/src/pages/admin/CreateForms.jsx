// pflichtenheft-user-interface mockup under "Editing a from/Adding trigger-conditionals"
// Diese Seite soll "ViewForms.jsx" aufgerufen werden und soll die Möglichkeit bieten, ein neues Formular zu erstellen.

import React, { useState } from "react";
import "./../../style/CreateForms.css";
import Navbar from "../../components/Navbar";
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
    // Create file input for XML import
    const fileInput = document.createElement("input");
    fileInput.type = "file";
    fileInput.accept = ".xml";
    fileInput.onchange = handleXMLFileImport;
    fileInput.click();
  };

  const handleXMLFileImport = (event) => {
    const file = event.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (e) => {
      try {
        const xmlContent = e.target.result;
        const parsedForm = parseXMLToForm(xmlContent);

        if (parsedForm) {
          setFormTitle(parsedForm.name);
          setFormFields(parsedForm.fields);
          setError("");
          alert("XML-Formular wurde erfolgreich importiert!");
        }
      } catch (error) {
        console.error("XML Import Error:", error);
        setError("Fehler beim Importieren der XML-Datei: " + error.message);
      }
    };
    reader.readAsText(file);
  };

  const parseXMLToForm = (xmlContent) => {
    // Parse XML according to backend structure:
    // <xNameExport><formDefinition name="..."><attributes><attribute name="..." type="..." required="..."/></attributes></formDefinition></xNameExport>

    const parser = new DOMParser();
    const xmlDoc = parser.parseFromString(xmlContent, "text/xml");

    // Check for parsing errors
    const parserError = xmlDoc.getElementsByTagName("parsererror");
    if (parserError.length > 0) {
      throw new Error("Ungültiges XML-Format");
    }

    // Extract form name from formDefinition
    const formDefinition = xmlDoc.getElementsByTagName("formDefinition")[0];
    if (!formDefinition) {
      throw new Error("Keine formDefinition im XML gefunden");
    }

    const formName =
      formDefinition.getAttribute("name") || "Importiertes Formular";

    // Extract all attribute elements (form fields)
    const attributes = xmlDoc.getElementsByTagName("attribute");
    const fields = [];

    for (let i = 0; i < attributes.length; i++) {
      const attr = attributes[i];
      const fieldName = attr.getAttribute("name");
      const fieldType = attr.getAttribute("type");
      const isRequired = attr.getAttribute("required") === "true";

      if (fieldName && fieldType) {
        // Map backend types to frontend dropdown options
        const mappedType = mapBackendTypeToFrontend(fieldType);

        fields.push({
          id: getNextId(),
          name: fieldName,
          type: mappedType,
          required: isRequired, // Store required info (though not used in current UI)
        });
      }
    }

    if (fields.length === 0) {
      throw new Error("Keine gültigen Felder in der XML-Datei gefunden");
    }

    return {
      name: formName,
      fields: fields,
    };
  };

  const mapBackendTypeToFrontend = (backendType) => {
    // Map backend BBType enum values to frontend dataTypes
    const typeMapping = {
      STRING: "String",
      TEXT: "String",
      EMAIL: "String",
      INTEGER: "Number",
      NUMBER: "Number",
      DATE: "Date",
      FLOAT: "Float",
      LONG: "Number",
      BOOLEAN: "Boolean",
      // Handle lowercase variants too
      string: "String",
      text: "String",
      email: "String",
      integer: "Number",
      number: "Number",
      date: "Date",
      float: "Float",
      long: "Number",
      boolean: "Boolean",
    };

    return typeMapping[backendType] || "String"; // Default to String if unknown type
  };

  const generateXMLFromCurrentForm = () => {
    const formNameSafe = formTitle.trim().replace(/[^a-zA-Z0-9]/g, "");
    let xml = `<x${formNameSafe}Export xmlns="urn:xoev:x${formNameSafe}:1.0" version="1.0">
	<!-- Formular-Definition -->
	<formDefinition name="${formTitle.trim()}">
		<attributes>`;

    formFields.forEach((field) => {
      const typeUpper = field.type.toUpperCase();
      xml += `\n			<attribute name="${field.name}" type="${typeUpper}" required="false"/>`;
    });

    xml += `
		</attributes>
	</formDefinition>
</x${formNameSafe}Export>`;

    return xml;
  };

  const handleExport = () => {
    const xmlContent = generateXMLFromCurrentForm();

    // Create and download the XML file
    const blob = new Blob([xmlContent], { type: "application/xml" });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = `${formTitle.trim() || "Civitas_formular"}.xml`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.URL.revokeObjectURL(url);

    alert("XML-Datei wurde erfolgreich heruntergeladen!");
  };

  return (
    <div>
      <Navbar />
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
            XML-Datei Importieren
          </button>
          <button className="export-button" onClick={handleExport}>
            XML-Datei Exportieren
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
