import React, { useState } from "react";
import "./../../style/CreateEditForms.css";
import "./../../style/AdminApplicantReporterPage.css"

// Mock data types to match your mockup dropdowns
const dataTypes = ["String", "Date", "Float", "Boolean", "Number"];

export default function Forms() {
    const [formFields, setFormFields] = useState([
        { id: '1', name: "Feld eins", type: "String", value: "" }, 
    ]);

    // Generates a unique ID for new fields
    const getNextId = () => (Date.now() + Math.random()).toString();

    // 1. Handles changes to the name and type of a field
    const handleFieldDefinitionChange = (event, index) => {
        const { name, value } = event.target;
        let data = [...formFields];
        // The event target name will be 'name' (for the field name) or 'type' (for the data type)
        data[index][name] = value;
        setFormFields(data);
    };

    // 2. Adds a new field ("Add Buildingblock" in the mockup)
    const addFields = () => {
        let newField = {
            id: getNextId(),
            name: `Neues Feld ${formFields.length + 1}`, // Default name
            type: "String", // Default type
            value: ""
        };
        // Add the new field object to the array
        setFormFields([...formFields, newField]);
    };

    // 3. Removes a field ("Remove Buildingblock" in the mockup)
    const removeFields = (id) => {
        // Filter the array to keep all fields whose id does NOT match the id to be removed
        const data = formFields.filter(field => field.id !== id);
        setFormFields(data);
    };

    // 4. Placeholder for "Meldeform Importieren"
    const handleImport = () => {
        alert("Meldeform Importieren clicked! (Functionality not yet implemented)");
        // Logic to open a file picker or modal for JSON/schema import would go here.
    };
    
    // 5. Placeholder for "Open Trigger List"
    const openTriggerList = (fieldName) => {
        alert(`Open Trigger List for: ${fieldName}`);
        // Logic to open a modal/drawer for conditional logic (triggers) would go here.
    };


    return (
        <div className="admin-page-container">
            <h1 className="main-title">Formular bearbeiten</h1>
            
            {/* Top-level buttons from your original code */}
            <div className="top-buttons-container">
                <button 
                    className="create-button"
                    onClick={addFields} // Correctly calls the addFields function
                >
                    Neues Feld Hinzufügen 
                </button>
                <button 
                    className="import-button"
                    onClick={handleImport}
                >
                    Meldeform Importieren 
                </button>
            </div>
            
            {/* Field Definitions Table/List */}
            <div className="form-builder-list">
                <h2>Formular Felder</h2>
                
                {formFields.map((field, index) => (
                    // This section visually represents one "building block" row from your mockup
                    <div key={field.id} className="field-row">
                        
                        {/* 1. Field Name Input */}
                        <input 
                            name="name"
                            placeholder="Feldname"
                            value={field.name}
                            onChange={(e) => handleFieldDefinitionChange(e, index)}
                            className="field-name-input"
                        />

                        {/* 2. Data Type Dropdown */}
                        <select
                            name="type"
                            value={field.type}
                            onChange={(e) => handleFieldDefinitionChange(e, index)}
                            className="field-type-select"
                        >
                            {dataTypes.map((type) => (
                                <option key={type} value={type}>{type}</option>
                            ))}
                        </select>
                        
                        {/* 3. Open Trigger List Button */}
                        <button 
                            className="trigger-button"
                            onClick={() => openTriggerList(field.name)}
                        >
                            Trigger-Liste Öffnen 
                        </button>
                        
                        {/* 4. Remove Buildingblock Button */}
                        <button 
                            className="remove-button"
                            onClick={() => removeFields(field.id)} // Uses the removeFields function
                        >
                            Entfernen 
                        </button>
                    </div>
                ))}
                
            </div>
        </div>
    );
}

