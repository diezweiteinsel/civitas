import { useState, useEffect } from "react";
import "./../style/AdminApplicantReporterPage.css";
import Navbar from "../components/Navbar";
import ApplicationContainer from "../components/ApplicationContainer";
import { useSearchParams } from "react-router-dom";
import { Role } from "../utils/const";
import { getApplicationsByStatus } from "../utils/data";

export default function RejectedApplication() {
  const [searchParams] = useSearchParams();
  const sourceRole = searchParams.get("from");

  const currentRole =
    sourceRole === "reporter"
      ? Role.REPORTER
      : Role.EMPTY;

  const [applications, setApplications] = useState([]);

  useEffect(() => {
    const rejectedApplication = getApplicationsByStatus("rejected");
    setApplications(rejectedApplication);
  }, []);



  return (
    <>
      <Navbar role={currentRole} />
      <ApplicationContainer applications={applications} title="Abgelehnte Anträge" />
    </>
  );
}