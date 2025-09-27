import { useEffect, useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import "./../style/AdminApplicantReporterPage.css";
import { FaDog, FaFire, FaInfoCircle } from "react-icons/fa";
import { getAllApplications } from "../utils/api";

export default function ApplicationContainer({
  applications: propsApplications = [],
  title = "Applications",
}) {
  const [expandedIds, setExpandedIds] = useState([]);
  const navigate = useNavigate();
  const location = useLocation();

  const {
    data: fetchedApplications,
    isLoading: applicationsLoading,
    error: applicationsError,
    refetch: refetchApplications,
  } = useQuery({
    queryKey: ["AllApplications"],
    queryFn: getAllApplications,
    enabled: true, // Enable automatic fetching
    retry: 1,
  });

  // Use fetched applications if available, otherwise use props
  const applications = fetchedApplications || propsApplications;

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
      1: "Dog License Application",
      2: "Fire Permit Application",
      3: "Information Request",
    };
    return typeMap[formId] || "Unknown Application";
  };

  const handleViewApplication = (applicationId) => {
    console.log(
      "ApplicationContainer - Navigating to application ID:",
      applicationId
    );

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

  return (
    <div className="page-container">
      <div className="containers-card">
        <h2 className="card-title">{title}</h2>

        {applicationsLoading && (
          <div style={{ textAlign: "center", padding: "20px" }}>
            <p>Loading applications...</p>
          </div>
        )}

        {applicationsError && (
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
            <p>Error loading applications: {applicationsError.message}</p>
            <button
              onClick={() => refetchApplications()}
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
          {!applicationsLoading && applications && applications.length === 0 ? (
            <div className="no-applications">
              <p>No applications found.</p>
            </div>
          ) : (
            applications &&
            applications.map((application) => (
              <div
                key={application.applicationID || application.id}
                className="container-item"
              >
                <div className="container-header">
                  <div className="icon">
                    {getIconByFormId(application.formID || application.formId)}
                  </div>
                  <div className="info">
                    <div className="form-type">
                      {getFormTypeByFormId(
                        application.formID || application.formId
                      )}
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
                    onClick={() =>
                      handleViewApplication(
                        application.applicationID || application.id
                      )
                    }
                    style={{ marginLeft: "10px" }}
                  >
                    Zeige Details
                  </button>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}
