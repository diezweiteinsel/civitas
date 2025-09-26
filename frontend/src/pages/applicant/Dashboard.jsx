import { useState, useEffect } from "react";
import "./../../style/AdminApplicantReporterPage.css";
import Navbar from "./../../components/Navbar";
import ApplicationContainer from "./../../components/ApplicationContainer";
import { Role } from "../../utils/const";
import { getAllApplications, addApplication } from "../../utils/data";
import applicationDB from "../../utils/data";

export default function ApplicantPage() {
  const [applications, setApplications] = useState([]);

  useEffect(() => {
    const persistentApplications = getAllApplications();
    setApplications(persistentApplications);
  }, []);

  const handleAddApplication = () => {
    const newApplication = addApplication();

    const updatedApplications = getAllApplications();
    setApplications(updatedApplications);
  };

  const handleResetDatabase = () => {
    if (
      window.confirm(
        "Are you sure you want to reset the database? This will delete all applications and create new random ones."
      )
    ) {
      applicationDB.resetDatabase();
      const refreshedApplications = getAllApplications();
      setApplications(refreshedApplications);
    }
  };

  return (
    <>
      <Navbar role={Role.APPLICANT} />
      <ApplicationContainer
        applications={applications}
        title="Your Applications:"
      />
      <div style={{ textAlign: "center", marginTop: "20px" }}>
        <button
          onClick={handleAddApplication}
          style={{
            backgroundColor: "#007bff",
            color: "white",
            padding: "10px 20px",
            border: "none",
            borderRadius: "5px",
            marginRight: "10px",
            cursor: "pointer",
          }}
        >
          Add New Application
        </button>
        <button
          onClick={handleResetDatabase}
          style={{
            backgroundColor: "#dc3545",
            color: "white",
            padding: "10px 20px",
            border: "none",
            borderRadius: "5px",
            cursor: "pointer",
          }}
        >
          Reset Database
        </button>
      </div>
    </>
  );
}
