import { useState, useEffect } from "react";
import { useParams, useNavigate, useLocation } from "react-router-dom";
import { useMutation } from "@tanstack/react-query";
import {
  FaDog,
  FaFire,
  FaInfoCircle,
  FaArrowLeft,
  FaHistory,
} from "react-icons/fa";

import "./../style/AdminApplicantReporterPage.css";
import "./../style/ApplicationView.css";
import Navbar from "../components/Navbar";
import { Role } from "../utils/const";
import { getApplicationById } from "../utils/api";

export default function ApplicationView() {
  const { id } = useParams();
  const navigate = useNavigate();
  const location = useLocation();
  const [application, setApplication] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  // Simplified helper functions
  const currentRole = (() => {
    const referrer = location.state?.from || document.referrer;
    if (referrer?.includes("/admin")) return Role.ADMIN;
    if (referrer?.includes("/applicant")) return Role.APPLICANT;
    return Role.EMPTY;
  })();

  const sourceContext = location.state?.fromPage || "unknown";

  // Fetch application data
  const getApplicationByIdMutation = useMutation({
    mutationFn: getApplicationById,
    onSuccess: (data) => {
      setError("");
      setApplication(data);
      setLoading(false);
    },
    onError: (error) => {
      setError(error.message || "Failed to fetch application.");
      setLoading(false);
    },
  });

  useEffect(() => {
    if (id && id !== "undefined") {
      setLoading(true);
      setError("");
      const numericId = parseInt(id, 10);
      if (isNaN(numericId)) {
        setError("Invalid application ID");
        setLoading(false);
        return;
      }
      getApplicationByIdMutation.mutate(numericId);
    } else {
      setError("No application ID provided");
      setLoading(false);
    }
  }, [id]);

  // Form configuration
  const FORM_CONFIG = {
    1: { icon: <FaDog />, type: "Hundelizenzantrag" },
    2: { icon: <FaFire />, type: "Biike-Feuerantrag" },
    3: { icon: <FaInfoCircle />, type: "Informationsanfrage" },
  };

  // Status translation
  const getGermanStatus = (status) => {
    const statusMap = {
      PENDING: "Ausstehend",
      APPROVED: "Genehmigt",
      REJECTED: "Abgelehnt",
      PUBLISHED: "Veröffentlicht",
    };
    return statusMap[status] || status;
  };

  const getIconByFormId = (formId) =>
    FORM_CONFIG[formId]?.icon || <FaInfoCircle />;
  const getFormTypeByFormId = (formId) =>
    FORM_CONFIG[formId]?.type || "Unbekannter Antrag";

  // Helper to get application properties with fallbacks
  const getAppProperty = (primary, secondary) =>
    application?.[primary] || application?.[secondary];

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
          {status?.toLowerCase() === "pending" && (
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

          {status?.toLowerCase() === "approved" && (
            <button
              className="action-btn publish-btn"
              onClick={() => handleStatusUpdate("published")}
            >
              Antrag veröffentlichen
            </button>
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
          {application.status?.toLowerCase() === "pending" && (
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
          <div className="loading">Antrag wird geladen...</div>
        </div>
      </>
    );
  }

  if (error) {
    return (
      <>
        <Navbar role={currentRole} />
        <div className="application-view">
          <div className="error">
            <h2>Fehler</h2>
            <p>{error}</p>
            <button className="action-btn" onClick={handleGoBack}>
              Zurück
            </button>
            <button
              className="action-btn"
              onClick={() => {
                const numericId = parseInt(id, 10);
                if (!isNaN(numericId)) {
                  setLoading(true);
                  setError("");
                  getApplicationByIdMutation.mutate(numericId);
                }
              }}
              style={{ marginLeft: "10px" }}
            >
              Erneut versuchen
            </button>
          </div>
        </div>
      </>
    );
  }

  if (!application) {
    return (
      <>
        <Navbar role={currentRole} />
        <div className="application-view">
          <div className="error">Antrag nicht gefunden</div>
          <button className="action-btn" onClick={handleGoBack}>
            Zurück
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
              <FaArrowLeft /> Zurück zum Dashboard
            </button>
            <div className="header-info">
              <div className="icon-large">
                {getIconByFormId(getAppProperty("formID", "formId"))}
              </div>
              <div className="header-text">
                <h1>
                  {getFormTypeByFormId(getAppProperty("formID", "formId"))}
                </h1>
                <div
                  className={`status-badge ${(
                    application.status || "pending"
                  ).toLowerCase()}`}
                >
                  {getGermanStatus(application.status || "PENDING")}
                </div>
              </div>
            </div>
          </div>

          {/* Application Metadata */}
          <div className="metadata-section">
            <h2>Antragsinformationen</h2>
            <div className="metadata-text">
              <p>Antrags-ID: {getAppProperty("applicationID", "id")}</p>
              <p>Formular-ID: {getAppProperty("formID", "formId")}</p>
              <p>Benutzer-ID: {getAppProperty("userID", "applicantId")}</p>
              {application.adminId && <p>Admin-ID: {application.adminId}</p>}
              <p>Status: {getGermanStatus(application.status)}</p>
              <p>
                Erstellt:{" "}
                {application.createdAt
                  ? new Date(application.createdAt).toLocaleString("de-DE")
                  : "Nicht verfügbar"}
              </p>
              {getAppProperty("currentSnapshotID", "currentSnapshotId") && (
                <p>
                  Aktuelle Snapshot-ID:{" "}
                  {getAppProperty("currentSnapshotID", "currentSnapshotId")}
                </p>
              )}
              {getAppProperty("previousSnapshotID", "previousSnapshotId") && (
                <p>
                  Vorherige Snapshot-ID:{" "}
                  {getAppProperty("previousSnapshotID", "previousSnapshotId")}
                </p>
              )}
            </div>
          </div>

          {/* Form Data */}
          <div className="form-data-section">
            <h2>Antragsdetails</h2>
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
              <h2>Revisionsgeschichte</h2>
              <div className="revision-info">
                <p>
                  <strong>Aktuelle Snapshot-ID:</strong>{" "}
                  {getAppProperty("currentSnapshotID", "currentSnapshotId") ||
                    "N/A"}
                </p>
                {getAppProperty("previousSnapshotID", "previousSnapshotId") && (
                  <p>
                    <strong>Vorherige Snapshot-ID:</strong>{" "}
                    {getAppProperty("previousSnapshotID", "previousSnapshotId")}
                  </p>
                )}
              </div>
            </div>
          )}
        </div>
      </div>
    </>
  );
}
