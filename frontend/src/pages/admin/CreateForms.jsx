// pflichtenheft-user-interface mockup under "Editing a from/Adding trigger-conditionals"
// Diese Seite soll "ViewForms.jsx" aufgerufen werden und soll die Möglichkeit bieten, ein neues Formular zu erstellen.

import React, { useState } from "react";
import "./../../style/CreateEditForms.css";
import "./../../style/AdminApplicantReporterPage.css"

const dataTypes = ["String", "Date", "Float", "Boolean", "Number"];

export default function Forms() {
    const [formFields, setFormFields] = useState([
        { id: '1', name: "Feld eins", type: "Text", value: "" }, // needs to be implemnted as a dict instead? i dont know 
    ])

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
            value: ""
        };
        setFormFields([...formFields, newField]);
    };

    const removeFields = (id) => {
        const data = formFields.filter(field => field.id !== id);
        setFormFields(data);
    };

    const handleImport = () => {
        alert("Meldeform wurde erflogreich importiert") //TODO:
    }

    return (
        <div>
            
            <div>
                <button 
                    className="create-button"
                    onClick={addFields}
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
            
            <div>
                
                {formFields.map((field, index) => (
                    <div key={field.id} className="field-row">

                        <input 
                            name="name"
                            placeholder="Feldname"
                            value={field.name}
                            onChange={(e) => handleForm(e, index)}
                        />

                        <select
                            name="type"
                            value={field.type}
                            onChange={(e) => handleForm(e, index)}
                        >
                            {dataTypes.map((type) => (
                                <option key={type} value={type}>{type}</option>
                            ))}
                        </select>
                        
                        <button 
                            className="remove-button"
                            onClick={() => removeFields(field.id)} 
                        >
                            Entfernen 
                        </button>
                    </div>
                ))}
                
            </div>
        </div>
    );
}