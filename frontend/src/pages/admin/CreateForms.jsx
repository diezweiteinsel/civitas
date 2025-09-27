// pflichtenheft-user-interface mockup under "Editing a from/Adding trigger-conditionals"
// Diese Seite soll "ViewForms.jsx" aufgerufen werden und soll die Möglichkeit bieten, ein neues Formular zu erstellen.

import React, { useState } from "react";
import "./../../style/CreateEditForms.css";
import "./../../style/AdminApplicantReporterPage.css"

export default function Forms() {
    const [formFields, setFormFields] = useState([
        { id: '1', name: "Feld eins", type: "Text", value: "" }, // needs to be implemnted as a dict instead? i dont know 
    ])

    const handleFormChange = (event, index) => {
        let data = [...formFields]
        data[index][event.target.name] = event.target.value
        setFormFields(data)
    }

    const addFields = () => {
        let object = {
            fieldOne: "",
            //fieldTwo: ""
        }
        setFormFields([...formFields, object]) //ensures that previous object doesn't get overwritten
    }

    const removeFields = (index) => {
        let data = [...formFields]
        data.splice(index,1)
        setFormFields(data)
    }

    const handleExport = () => {

    }

    return (
        <>
        <Navbar />
        <div>
            <button 
            className="create-button"
            onClick={() => addFields()}
            >Neue Meldeform Erstellen
            </button>
            <button 
            className="import-button"
            onClick={() => handleExport()}
            >Meldeform Importieren
            </button>
        </div>
        </>
    )
}