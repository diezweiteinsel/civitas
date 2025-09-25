import { useState } from "react";
import "./../../style/AdminApplicantReporterPage.css";
import Navbar from "../../components/Navbar";
import { FaDog, FaFire, FaInfoCircle } from "react-icons/fa";
import { useNavigate } from "react-router-dom";
import { Role } from "../../utils/const";

export default function SubmitApplications() {
  const formTypes = [
    { type: "Form type: Dog", icon: <FaDog /> },
    { type: "Form type: Fire", icon: <FaFire /> },
    { type: "Form type: Info", icon: <FaInfoCircle /> },
  ];
  const navigate = useNavigate();

  // Create one container for each type: Dog, Fire, Info
  const [containers, setContainers] = useState(
    formTypes.map((form, i) => ({
      id: i + 1,
      formType: form.type,
      icon: form.icon,
      description: `This is more detailed information about the ${form.type}.`,
    }))
  );
  const [expandedIds, setExpandedIds] = useState([]);

  return (
    <>
      <Navbar role={Role.APPLICANT} />
      <div className="page-container">
        <div className="containers-card">
          <h2 className="card-title">Submit Applications</h2>

          <div className="container-list">
            {containers.map((container) => (
              <div key={container.id} className="container-item">
                <div className="container-header">
                  <div className="icon">{container.icon}</div>
                  <div className="info">
                    <div className="form-type">{container.formType}</div>
                  </div>
                  <button
                    className="toggle-btn"
                    onClick={() => navigate("/applicant/application-edit")}
                  >
                    {expandedIds.includes(container.id) ? "Hide" : "Fill out"}
                  </button>
                </div>
                {expandedIds.includes(container.id) && (
                  <div className="container-details">
                    {container.description}
                  </div>
                )}
              </div>
            ))}
          </div>
          <div className="page-space"></div>
        </div>
      </div>
    </>
  );
}
