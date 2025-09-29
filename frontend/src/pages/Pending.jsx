import { useState, useEffect } from "react";
import "./../style/AdminApplicantReporterPage.css";
import Navbar from "../components/Navbar";
import ApplicationContainer from "../components/ApplicationContainer";
import { useSearchParams } from "react-router-dom";
import { Role } from "../utils/const";
import { getApplicationsByStatus } from "../utils/data";

export default function PendingApplication() {
  const [searchParams] = useSearchParams();
  const sourceRole = searchParams.get("from");

  const currentRole =
    sourceRole === "reporter"
      ? Role.REPORTER
      : Role.EMPTY;

  const [applications, setApplications] = useState([]);

  useEffect(() => {
    const pendingApplication = getApplicationsByStatus("pending");
    setApplications(pendingApplication);
  }, []);



  return (
    <>
      <Navbar role={currentRole} />
      <ApplicationContainer applications={applications} title="Ausstehende Anträge:" />
    </>
  );
}