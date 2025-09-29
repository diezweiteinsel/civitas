// pflichtenheft-user-interface mockup under "Role-Reporter"
// The "Dashboard" page provides reporters with an overview of all applications.

import { useState, useEffect } from "react";
import "./../../style/AdminApplicantReporterPage.css";
import Navbar from "./../../components/Navbar";
import ApplicationContainer from "./../../components/ApplicationContainer";
import { Role } from "../../utils/const";

export default function ReporterPage() {
  const [applications, setApplications] = useState([]);

  useEffect(() => {
    const persistentApplications = getAllApplications();
    setApplications(persistentApplications);
  }, []);


  return (
    <>
      <Navbar role={Role.REPORTER} />
      <ApplicationContainer applications={[]} title="Applications:" />
      <div style={{ textAlign: "center", marginTop: "20px" }}>
        <button
          onClick={handleExport}
          style={{
            backgroundColor: "#dc3545",
            color: "white",
            padding: "10px 20px",
            border: "none",
            borderRadius: "5px",
            cursor: "pointer",
          }}
        >
          Exportieren
        </button>
      </div>
    </>
  );
}
