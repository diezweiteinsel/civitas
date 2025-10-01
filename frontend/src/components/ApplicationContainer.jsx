import "./../style/AdminApplicantReporterPage.css";
import { useNavigate, useLocation } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { BiWorld } from "react-icons/bi";
import { FaEye } from "react-icons/fa";
import {
  getAllApplications,
  getApplicationsByStatus,
  getPublicApplications,
  getPublicApplicationsByStatus,
} from "../utils/api";

export default function ApplicationContainer({
  applications: providedApplications = [],
  statuses = [],
  isPublic = false,
  title = "Applications",
  enableFetch = true,
  isLoadingOverride = false,
  errorOverride = null,
  onRetry = () => {},
}) {
  const navigate = useNavigate();
  const location = useLocation();

  // Fetch applications based on isPublic prop
  const normalizedStatuses = Array.isArray(statuses)
    ? statuses.filter(Boolean)
    : [];

  const queryKey = [
    "applications",
    isPublic ? "public" : "private",
    normalizedStatuses.length ? normalizedStatuses.join(",") : "all",
  ];

  const queryFn = () => {
    if (isPublic) {
      if (normalizedStatuses.length) {
        return getPublicApplicationsByStatus(normalizedStatuses);
      }
      return getPublicApplications();
    }

    if (normalizedStatuses.length) {
      return getApplicationsByStatus(normalizedStatuses);
    }

    return getAllApplications();
  };

  const {
    data: fetchedApplications,
    isLoading: applicationsLoading,
    error: applicationsError,
    refetch: refetchApplications,
  } = useQuery({
    queryKey,
    queryFn,
    enabled: enableFetch,
    retry: 1,
  });

  const applications = enableFetch ? fetchedApplications : providedApplications;
  const isLoading = enableFetch ? applicationsLoading : isLoadingOverride;
  const error = enableFetch ? applicationsError : errorOverride;
  const retryFn = enableFetch ? refetchApplications : onRetry;

  const safeApplications = Array.isArray(applications) ? applications : [];

  // Function to route to ApplicationView and to give the redirection context
  const handleViewApplication = (formId, applicationId) => {
    if (!formId || !applicationId) {
      return;
    }

    // Determine the source page context
    const currentPath = location.pathname;
    let fromPage = "unknown";

    if (currentPath.includes("/admin")) {
      fromPage = "admin-dashboard";
    } else if (currentPath.includes("/applicant")) {
      fromPage = "applicant-dashboard";
    } else if (currentPath.includes("/public")) {
      fromPage = "public-applications";
    } else if (currentPath.includes("/reporter")) {
      fromPage = "reporter-applications";
    }

    // Navigate with state to provide context to ApplicationView
    navigate(`/applications/${formId}/${applicationId}`, {
      state: {
        fromPage: fromPage,
        from: currentPath,
      },
    });
  };

  const translateStatus = (status) => {
    if (!status) return "Unbekannt";
    const statusUpper = status.toString().toUpperCase();
    if (statusUpper === "PENDING") return "Ausstehend";
    if (statusUpper === "APPROVED") return "Genehmigt";
    if (statusUpper === "REJECTED") return "Abgelehnt";
    return status;
  };

  return (
    <div className="page-container">
      <div className="containers-card">
        <h2 data-testid="card-title" className="card-title">
          {title}
        </h2>

        {isLoading && (
          <div style={{ textAlign: "center", padding: "20px" }}>
            <p>Loading applications...</p>
          </div>
        )}
        {error && (
          <div
            style={{
              textAlign: "center",
              color: "red",
              padding: "20px",
              backgroundColor: "#fee",
              borderRadius: "5px",
              margin: "10px 0",
            }}
          >
            <p>Error loading applications: {error.message || String(error)}</p>
            <button
              onClick={() => retryFn && retryFn()}
              style={{
                marginTop: "10px",
                padding: "5px 10px",
                backgroundColor: "#007bff",
                color: "white",
                border: "none",
                borderRadius: "3px",
                cursor: "pointer",
              }}
            >
              Retry
            </button>
          </div>
        )}
        <div className="container-list">
          {!isLoading && safeApplications && safeApplications.length === 0 ? (
            <div className="no-applications">
              <p>No applications found.</p>
            </div>
          ) : (
            safeApplications.map((application) => {
              const applicationId = application.applicationID || application.id;
              const formId =
                application.formId || application.formID || application.form_id;
              const formName = application.title;
              const createdRaw =
                application.createdAt || application.created_at;
              let createdLabel = "—";
              if (createdRaw) {
                const createdDate = new Date(createdRaw);
                if (!Number.isNaN(createdDate.getTime())) {
                  createdLabel = createdDate.toLocaleString("de-DE");
                }
              }
              const rawStatus = (application.status || "").toString();
              const statusClass = rawStatus.toLowerCase();
              const statusDisplay = rawStatus
                ? translateStatus(rawStatus)
                : "Unbekannt";

              return (
                <div key={applicationId} className="container-item">
                  <div className="container-header">
                    <div className="info">
                      <div className="form-type">{formName}</div>
                      <div className="container-meta">
                        <span>Erstellt: {createdLabel}</span>
                      </div>
                      <div className="status-row">
                        <div className={`status ${statusClass}`}>
                          {statusDisplay}
                        </div>
                        {application.is_public && (
                          <div
                            className="public-indicator"
                            title="Öffentlich sichtbar"
                          >
                            <BiWorld className="world-icon" />
                            <FaEye className="eye-icon" />
                          </div>
                        )}
                      </div>
                    </div>
                    <button
                      className="toggle-btn"
                      onClick={() =>
                        handleViewApplication(formId, applicationId)
                      }
                      style={{ marginLeft: "10px" }}
                    >
                      Zeige Details
                    </button>
                  </div>
                </div>
              );
            })
          )}
        </div>
      </div>
    </div>
  );
}
