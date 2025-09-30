import { useMemo } from "react";
import { useQuery } from "@tanstack/react-query";
import { useParams, useNavigate, useLocation } from "react-router-dom";
import { FaArrowLeft, FaHistory } from "react-icons/fa";

import "./../style/AdminApplicantReporterPage.css";
import "../style/ApplicationView.css";
import Navbar from "../components/Navbar";
import ApplicationContainer from "../components/ApplicationContainer";
import { getApplicationById } from "../utils/api";

const CONTEXT_FALLBACKS = {
  "admin-dashboard": "/admin",
  "applicant-dashboard": "/applicant",
  "reporter-applications": "/reporter",
  "public-applications": "/applicant/public",
};

export default function ApplicationRevision() {
  const navigate = useNavigate();
  const location = useLocation();
  const { formId, applicationId } = useParams();

  const numericFormId = Number.parseInt(formId, 10);
  const numericAppId = Number.parseInt(applicationId, 10);
  const areIdsValid =
    Number.isInteger(numericFormId) && Number.isInteger(numericAppId);

  const sourceContext = location.state?.fromPage || "unknown";

  const {
    data: application,
    error,
    isLoading,
    refetch,
  } = useQuery({
    queryKey: ["application", numericFormId, numericAppId],
    queryFn: () => getApplicationById(numericFormId, numericAppId),
    enabled: areIdsValid,
    retry: 1,
  });

  // TODO: Implement API call to fetch revision history from backend
  const revisionHistory = useMemo(() => {
    if (!application) return [];

    // TODO: Replace with actual API call to get application revision history
    // Example: getApplicationRevisions(numericFormId, numericAppId)
    // Should return array of revision objects with structure:
    // {
    //   id: string,
    //   revision_number: string,
    //   created_at: string,
    //   status: string,
    //   is_public: boolean,
    //   form_id: number,
    //   formName: string,
    //   title: string,
    //   user_id: number,
    //   jsonPayload: object,
    //   changes: string,
    //   change_type: string
    // }

    return [];
  }, [application]);

  const handleGoBack = () => {
    // Navigate back to the application view
    navigate(`/applications/${formId}/${applicationId}`);
  };

  if (isLoading) {
    return (
      <>
        <Navbar />
        <div className="application-view">
          <div className="loading">Antragshistorie wird geladen…</div>
        </div>
      </>
    );
  }

  if (error) {
    return (
      <>
        <Navbar />
        <div className="application-view">
          <div className="error">
            <h2>Fehler beim Laden</h2>
            <p>{error.message || "Unbekannter Fehler"}</p>
            <div
              className="button-group"
              style={{ justifyContent: "center", marginTop: "20px" }}
            >
              <button
                type="button"
                className="action-btn"
                onClick={handleGoBack}
              >
                Zurück
              </button>
              <button
                type="button"
                className="action-btn"
                onClick={() => refetch()}
              >
                Erneut versuchen
              </button>
            </div>
          </div>
        </div>
      </>
    );
  }

  if (!application) {
    return (
      <>
        <Navbar />
        <div className="application-view">
          <div className="error">
            <h2>Antrag nicht gefunden</h2>
            <p>Der angeforderte Antrag konnte nicht gefunden werden.</p>
            <button type="button" className="action-btn" onClick={handleGoBack}>
              Zurück
            </button>
          </div>
        </div>
      </>
    );
  }

  const applicationTitle =
    application.title || application.form_name || `Antrag #${application.id}`;

  return (
    <>
      <Navbar />
      <div className="application-view">
        <div className="view-container">
          <header className="view-header">
            <button type="button" className="back-btn" onClick={handleGoBack}>
              <FaArrowLeft /> Zurück zur Antragsansicht
            </button>
            <div className="header-info">
              <FaHistory className="icon-large" />
              <div className="header-text">
                <h1>Historie: {applicationTitle}</h1>
                <p style={{ margin: "8px 0 0 0" }}>
                  Antrag #{application.id} · Formular #
                  {application.form_id || application.formId}
                </p>
              </div>
            </div>
          </header>

          <section className="metadata-section">
            <h2>Revisionsübersicht</h2>
            <div className="metadata-text">
              <p>
                <strong>Antrag-ID:</strong> {application.id}
              </p>
              <p>
                <strong>Gesamte Revisionen:</strong> {revisionHistory.length || "TODO: Implementierung ausstehend"}
              </p>
              <p>
                <strong>Letzte Änderung:</strong>{" "}
                {new Date(
                  application.created_at || application.createdAt
                ).toLocaleString("de-DE")}
              </p>
            </div>
          </section>

          <ApplicationContainer
            applications={revisionHistory}
            title={`Revisionshistorie (${revisionHistory.length} Versionen)`}
            enableFetch={false}
            isLoadingOverride={false}
            errorOverride={null}
            showRevisionInfo={true}
          />
        </div>
      </div>
    </>
  );
}
