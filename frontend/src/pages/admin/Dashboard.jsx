import { useState, useEffect } from "react";
import "./../../style/AdminApplicantReporterPage.css";
import Navbar from "./../../components/Navbar";
import { FaDog, FaFire, FaInfoCircle } from "react-icons/fa";
import { Role } from "../../utils/const";
import ApplicationContainer from "./../../components/ApplicationContainer";

export default function AdminPage() {
  const [pendingApplications, setPendingApplications] = useState([]);
  const [approvedApplications, setApprovedApplications] = useState([]);

  return (
    <>
      <Navbar role={Role.ADMIN} />
      <div className="page-container">
        <ApplicationContainer applications={[]} title="Pending Applications:" />
        <div className="page-space"> </div>
        <ApplicationContainer
          applications={[]}
          title="Approved Applications:"
        />
      </div>
    </>
  );
}
