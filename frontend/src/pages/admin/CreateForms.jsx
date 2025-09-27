// pflichtenheft-user-interface mockup under "Editing a from/Adding trigger-conditionals"
// Diese Seite soll "ViewForms.jsx" aufgerufen werden und soll die Möglichkeit bieten, ein neues Formular zu erstellen.

import React from "react";
import "./../../style/AdminApplicantReporterPage.css";

export default function Forms() {
    const [formFields, setFormFields] = usestate([
        {fieldOne: "", fieldTwo: ""},
    ])

    const handleFormChange = (event, index) => {
        let data = [...formFields]
        data[index][event.target.fieldOne] = event.target.value
        setFormFields(data)
    }

    const addFields = () => {
        let object = {
            fieldOne: "",
            fieldTwo: ""
        }

        setFormFields(...formFields, [object]) //ensures that previous object isn't overwritten 
    }

    const removeFields = (index) => {
        let data = [...formFields]
        data.splice[index,1]
        setFormFields(data)
    }
}