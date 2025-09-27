// pflichtenheft-user-interface mockup above "Admins can view approved or published applications via the "Admin Homepage" and "Public Applications" page."
// This side shows the details of a specific application. Must have the option to look at revision when admin is looking at it or we have a "ApplicationView.jsx" inside of admin and applicant which are fundamentally the same but with different buttons.
// Can be routed to from anywhere where you can press on a application to view it in detail. Also needs ability to have multiple button for the different cases in admin for example "Approve/reject" afterwards maybe "publish".

import { useState } from "react";
import { useParams, useNavigate, useLocation } from "react-router-dom";
import "./../style/AdminApplicantReporterPage.css";
import "./../style/ApplicationView.css";
import Navbar from "../components/Navbar";
import {
  FaDog,
  FaFire,
  FaInfoCircle,
  FaArrowLeft,
  FaHistory,
} from "react-icons/fa";
import { Role } from "../utils/const";

export default function ApplicationView() {
  const { id } = useParams();
  const navigate = useNavigate();
  const location = useLocation();
  const [application, setApplication] = useState(null);
  const [loading, setLoading] = useState(true);

  const getUserRole = () => {
    const currentPath = location.pathname;
    const referrer = location.state?.from || document.referrer;

    if (referrer) {
      if (referrer.includes("/admin")) return Role.ADMIN;
      if (referrer.includes("/applicant")) return Role.APPLICANT;
    }

    return Role.EMPTY;
  };

  const currentRole = getUserRole();
  const sourceContext = getSourceContext();

  const getIconByFormId = (formId) => {
    const iconMap = {
      1: <FaDog />,
      2: <FaFire />,
      3: <FaInfoCircle />,
    };
    return iconMap[formId] || <FaInfoCircle />;
  };

  const getFormTypeByFormId = (formId) => {
    const typeMap = {
      1: "Hundelizenzantrag",
      2: "Biike-Feuerantrag",
      3: "Informationsanfrage",
    };
    return typeMap[formId] || "Unbekannter Antrag";
  };

  const handleStatusUpdate = (newStatus) => {
    if (application) {
      alert(`Antrag ${newStatus} erfolgreich!`);
    }
  };

  const handleGoBack = () => {
    if (currentRole === Role.ADMIN) {
      navigate("/admin");
    } else if (currentRole === Role.APPLICANT) {
      navigate("/applicant");
    } else {
      navigate(-1);
    }
  };

  const renderPageContext = () => {
    if (currentRole !== Role.ADMIN) return null;

    const contextMap = {
      "admin-dashboard": "Anzeigen über die Admin-Startseite",
      "public-applications": "Anzeigen über die öffentlichen Anwendungen",
      "applicant-dashboard": "Anzeigen über das Bewerber-Dashboard",
      unknown: "Direkter Zugriff",
    };

    return (
      <div className="context-info">
        <small>
          <FaHistory /> {contextMap[sourceContext] || "Unbekannter Kontext"}
        </small>
      </div>
    );
  };

  const renderActionButtons = () => {
    if (currentRole !== Role.ADMIN) return null;

    const { status } = application;

    return (
      <div className="action-buttons">
        <h3>Admin-Aktionen:</h3>
        {renderPageContext()}

        <div className="button-group">
          {/* Pending Applications - From Admin Dashboard */}
          {status === "pending" && (
            <>
              <button
                className="action-btn approve-btn"
                onClick={() => handleStatusUpdate("approved")}
              >
                Antrag genehmigen
              </button>
              <button
                className="action-btn reject-btn"
                onClick={() => handleStatusUpdate("rejected")}
              >
                Antrag ablehnen
              </button>
            </>
          )}

          {/* Approved Applications - Can be Published */}
          {status === "approved" && (
            <>
              <button
                className="action-btn publish-btn"
                onClick={() => handleStatusUpdate("published")}
              >
                Antrag veröffentlichen
              </button>
            </>
          )}
        </div>
      </div>
    );
  };

  const renderApplicantActions = () => {
    if (currentRole !== Role.APPLICANT) return null;

    return (
      <div className="applicant-actions">
        <h3>Antragsoptionen:</h3>
        <div className="button-group">
          {application.status === "pending" && (
            <button
              className="action-btn edit-btn"
              onClick={() => navigate(`/applicant/edit/${application.id}`)}
            >
              Antrag bearbeiten
            </button>
          )}

          <button
            className="action-btn info-btn"
            onClick={() => {
              const statusMessages = {
                pending:
                  "Ihr Antrag wird derzeit von unserem Verwaltungsteam geprüft.",
                approved: "Herzlichen Glückwunsch! Ihr Antrag wurde genehmigt.",
                rejected:
                  "Leider wurde Ihr Antrag nicht genehmigt. Bitte kontaktieren Sie die Verwaltung für weitere Informationen.",
                published:
                  "Ihr Antrag wurde genehmigt und ist jetzt öffentlich sichtbar.",
              };
              alert(
                statusMessages[application.status] || "Antragsstatus unbekannt."
              );
            }}
          >
            Status-Informationen
          </button>
        </div>
      </div>
    );
  };

  if (loading) {
    return (
      <>
        <Navbar role={currentRole} />
        <div className="application-view">
          <div className="loading">Loading application...</div>
        </div>
      </>
    );
  }

  if (!application) {
    return (
      <>
        <Navbar role={currentRole} />
        <div className="application-view">
          <div className="error">Application not found</div>
          <button className="action-btn" onClick={handleGoBack}>
            Go Back
          </button>
        </div>
      </>
    );
  }

  return (
    <>
      <Navbar role={currentRole} />
      <div className="application-view">
        <div className="view-container">
          {/* Header */}
          <div className="view-header">
            <button className="back-btn" onClick={handleGoBack}>
              <FaArrowLeft /> Back to Dashboard
            </button>
            <div className="header-info">
              <div className="icon-large">
                {getIconByFormId(application.formId)}
              </div>
              <div className="header-text">
                <h1>{getFormTypeByFormId(application.formId)}</h1>
                <div
                  className={`status-badge ${application.status.toLowerCase()}`}
                >
                  {application.status.charAt(0).toUpperCase() +
                    application.status.slice(1)}
                </div>
              </div>
            </div>
          </div>

          {/* Application Metadata */}
          <div className="metadata-section">
            <h2>Application Information</h2>
            <div className="metadata-text">
              <p>Application ID: {application.id}</p>
              <p>Form ID: {application.formId}</p>
              <p>Applicant ID: {application.applicantId}</p>
              {/* Maybe useful when we want to know which admin approved*/}
              <p>Admin ID: {application.adminId}</p>{" "}
              <p>Submitted: {application.createdAt?.toLocaleString()}</p>
              <p>Current Snapshot ID: {application.currentSnapshotId}</p>
              {application.previousSnapshotId && (
                <p>Previous Snapshot ID: {application.previousSnapshotId}</p>
              )}
            </div>
          </div>

          {/* Form Data */}
          <div className="form-data-section">
            <h2>Application Details</h2>
            <div className="form-data-content">
              {Object.entries(application.jsonPayload || {}).map(
                ([key, value]) => (
                  <div key={key} className="form-field">
                    <label>
                      {key.charAt(0).toUpperCase() +
                        key.slice(1).replace(/([A-Z])/g, " $1")}
                      :
                    </label>
                    <span>
                      {typeof value === "object"
                        ? JSON.stringify(value, null, 2)
                        : String(value)}
                    </span>
                  </div>
                )
              )}
            </div>
          </div>

          {/* Role-based Action Buttons */}
          {renderActionButtons()}
          {renderApplicantActions()}

          {/* Revision History for Admins */}
          {currentRole === Role.ADMIN && (
            <div className="revision-section">
              <h2>Revision History</h2>
              <div className="revision-info">
                <p>
                  <strong>Current Snapshot ID:</strong>{" "}
                  {application.currentSnapshotId}
                </p>
                {application.previousSnapshotId && (
                  <p>
                    <strong>Previous Snapshot ID:</strong>{" "}
                    {application.previousSnapshotId}
                  </p>
                )}
                <button
                  className="action-btn info-btn"
                  onClick={() =>
                    alert("Revision comparison feature coming soon!")
                  }
                >
                  View Revision History
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </>
  );
}
