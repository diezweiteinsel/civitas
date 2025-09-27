import { useState, useEffect } from "react";
import "./../../style/AdminApplicantReporterPage.css";
import Navbar from "./../../components/Navbar";
import ApplicationContainer from "./../../components/ApplicationContainer";
import { Role } from "../../utils/const";

export default function ApplicantPage() {
  const [applications, setApplications] = useState([]);

  return (
    <>
      <Navbar role={Role.APPLICANT} />
      <ApplicationContainer applications={[]} title="Eigene Anträge:" />
    </>
  );
}
