import { useState, useEffect } from "react";
import "./../../style/AdminApplicantReporterPage.css";
import Navbar from "./../../components/Navbar";
import { FaDog, FaFire, FaInfoCircle } from "react-icons/fa";
import { Role } from "../../utils/const";
import ApplicationContainer from "./../../components/ApplicationContainer";
import { getAllApplications, getApplicationsByStatus } from "../../utils/data";

export default function AdminPage() {
  const [pendingApplications, setPendingApplications] = useState([]);
  const [approvedApplications, setApprovedApplications] = useState([]);

  useEffect(() => {
    const pending = getApplicationsByStatus("pending");
    const approved = getApplicationsByStatus("approved");

    setPendingApplications(pending);
    setApprovedApplications(approved);
  }, []);

  return (
    <>
      <Navbar role={Role.ADMIN} />
      <div className="page-container">
        <ApplicationContainer
          applications={pendingApplications}
          title="Pending Applications:"
        />
        <div className="page-space"> </div>
        <ApplicationContainer
          applications={approvedApplications}
          title="Approved Applications:"
        />
      </div>
    </>
  );
}
