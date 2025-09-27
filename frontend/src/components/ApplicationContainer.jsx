import { useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import "./../style/AdminApplicantReporterPage.css";
import { FaDog, FaFire, FaInfoCircle } from "react-icons/fa";

export default function ApplicationContainer({
  applications,
  title = "Applications",
}) {
  const [expandedIds, setExpandedIds] = useState([]);
  const navigate = useNavigate();
  const location = useLocation();

  // Helper function to get icon based on formId
  const getIconByFormId = (formId) => {
    const iconMap = {
      1: <FaDog />,
      2: <FaFire />,
      3: <FaInfoCircle />,
    };
    return iconMap[formId] || <FaInfoCircle />;
  };

  // Helper function to get form type name based on formId
  const getFormTypeByFormId = (formId) => {
    const typeMap = {
      1: "Dog License Application",
      2: "Fire Permit Application",
      3: "Information Request",
    };
    return typeMap[formId] || "Unknown Application";
  };

  const handleViewApplication = (applicationId) => {
    // Determine the source page context
    const currentPath = location.pathname;
    let fromPage = "unknown";

    if (currentPath.includes("/admin")) {
      fromPage = "admin-dashboard";
    } else if (currentPath.includes("/applicant")) {
      fromPage = "applicant-dashboard";
    } else if (currentPath.includes("/public")) {
      fromPage = "public-applications";
    }

    // Navigate with state to provide context to ApplicationView
    navigate(`/application/${applicationId}`, {
      state: {
        fromPage: fromPage,
        from: currentPath,
      },
    });
  };

  const toggleExpand = (id) => {
    setExpandedIds((prev) =>
      prev.includes(id) ? prev.filter((eid) => eid !== id) : [...prev, id]
    );
  };

  return (
    <div className="page-container">
      <div className="containers-card">
        <h2 className="card-title">{title}</h2>

        <div className="container-list">
          {applications.length === 0 ? (
            <div className="no-applications">
              <p>Keine Anträge gefunden.</p>
            </div>
          ) : (
            applications.map((application) => (
              <div key={application.id} className="container-item">
                <div className="container-header">
                  <div className="icon">
                    {getIconByFormId(application.formId)}
                  </div>
                  <div className="info">
                    <div className="form-type">
                      {getFormTypeByFormId(application.formId)}
                    </div>
                    <div
                      className={`status ${application.status.toLowerCase()}`}
                    >
                      {application.status.charAt(0).toUpperCase() +
                        application.status.slice(1)}
                    </div>
                  </div>
                  <button
                    className="toggle-btn"
                    onClick={() => handleViewApplication(application.id)}
                  >
                    Zeige Details
                  </button>
                </div>
                {expandedIds.includes(application.id) && (
                  <div className="container-details">
                    <div>
                      <strong>Vorschau:</strong>
                    </div>
                    <div>Antrags-ID: {application.id}</div>
                    <div>
                      Erstellt: {application.createdAt?.toLocaleDateString()}
                    </div>
                    <div>Status: {application.status}</div>
                    <button
                      className="toggle-btn"
                      style={{ marginTop: "10px" }}
                      onClick={() => handleViewApplication(application.id)}
                    >
                      Zeige vollständige Details
                    </button>
                  </div>
                )}
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}
