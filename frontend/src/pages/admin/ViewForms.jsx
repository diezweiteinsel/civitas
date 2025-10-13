// plichtenheft-user-interface mockup above "The "Form" page allows admins to create new forms, edit existing ones, or import them."
// Soll die Seite sein die vom Admin dashboard aus erreichbar ist und alle current Formulare anzeigt und die Möglichkeit bietet, neue Formulare zu erstellen und zu importieren.
// Soll durch "create form" button oder so zu "CreateFroms.jsx" navigieren

import React, { useState, useEffect } from "react";
import "../../style/ViewForms.css";
import Navbar from "../../components/Navbar";
import { getAllForms } from "../../utils/api";
import { useNavigate } from "react-router-dom";
import { FaDownload } from "react-icons/fa";
import { CiEdit } from "react-icons/ci";

export default function ViewForms() {
  const [forms, setForms] = useState([]);
  const [loading, setLoading] = useState(true);

  const [error, setError] = useState("");
  const navigate = useNavigate();

  const goToCreateForms = () => {
    navigate("/admin/create-forms");
  };

  const exportFormAsXml = (id) => {
    const form = forms.find((f) => f.id == id);
    const formNameSafe = form.form_name.trim().replace(/[^a-zA-Z0-9]/g, "");
    let xml = `<x${formNameSafe}Export xmlns="urn:xoev:x${formNameSafe}:1.0" version="1.0">
	<!-- Formular-Definition -->
	<formDefinition name="${form.form_name.trim()}">
		<attributes>`;
    //console.log("form", JSON.stringify(form, null, 2));

    const blocksArray = Object.values(form.blocks);
    blocksArray.forEach((block) => {
      const typeUpper = block.data_type.toUpperCase();
      xml += `\n			<attribute name="${block.label}" type="${typeUpper}" required="false"/>`;
    });

    xml += `
		</attributes>
	</formDefinition>
</x${formNameSafe}Export>`;

    const blob = new Blob([xml], { type: "application/xml" });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = `${form.form_name.trim() || "Civitas_formular"}.xml`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.URL.revokeObjectURL(url);
  };

  //const allForms = getAllForms();
  useEffect(() => {
    // call your function when component mounts
    getAllForms()
      .then((data) => {
        setForms(data);
        setLoading(false);
      })
      .catch((error) => {
        setError("Error loading forms:", error);
        setLoading(false);
      });
  }, []);

  if (loading)
    return (
      <div>
        <Navbar />
        <div className="form-view-container">
          <div className="form-view-header">
            <h2>Alle Meldeformulare</h2>
          </div>
          ...
          {error && <div className="error-message">{error}</div>}
        </div>
      </div>
    );

  return (
    <div>
      <Navbar />
      <div className="form-view-container">
        <div className="form-view-header">
          <h2>Alle Meldeformulare</h2>
        </div>

        {error && <div className="error-message">{error}</div>}

        <div className="forms-container">
          {forms.map((form) => (
            <div key={form.id} className="forms-row">
              <div>{form.id}</div>
              <div>{form.version}</div>
              <div>{form.form_name}</div>
              <div>{form.is_active}</div>
              <button
                className="export-form-button"
                onClick={() => exportFormAsXml(form.id)}
                title="Antrag exportieren"
              >
                <FaDownload />
              </button>
            </div>
          ))}
        </div>
        <button className="create-new-form-button" onClick={goToCreateForms}>
          Neues Meldeformular Erstellen
        </button>
      </div>
    </div>
  );
}
