import { Fragment, useMemo } from "react";
import { useQuery } from "@tanstack/react-query";
import { useParams, useNavigate, useLocation } from "react-router-dom";
import {
  FaCheckCircle,
  FaTimesCircle,
  FaClock,
  FaArrowLeft,
  FaHistory,
} from "react-icons/fa";

import { BiWorld } from "react-icons/bi";
import { FaEye } from "react-icons/fa";

import "./../style/AdminApplicantReporterPage.css";
import "./../style/ApplicationView.css";
import Navbar from "../components/Navbar";
import { Role } from "../utils/const";
import { getApplicationById } from "../utils/api";
import { getUserRoles } from "../utils/data";

const STATUS_LABELS = {
  PENDING: "Ausstehend",
  APPROVED: "Genehmigt",
  REJECTED: "Abgelehnt",
  REVISION: "Revision",
  PUBLISHED: "Öffentlich",
  DRAFT: "Entwurf",
};

const CONTEXT_FALLBACKS = {
  "admin-dashboard": "/admin",
  "applicant-dashboard": "/applicant",
  "reporter-applications": "/reporter",
  "public-applications": "/applicant/public",
};

export default function ApplicationView() {
  const navigate = useNavigate();
  const location = useLocation();
  const { formId, applicationId } = useParams();

  const numericFormId = Number.parseInt(formId, 10);
  const numericAppId = Number.parseInt(applicationId, 10);
  const areIdsValid =
    Number.isInteger(numericFormId) && Number.isInteger(numericAppId);

  const roles = getUserRoles();
  const currentRole = roles && roles.length > 0 ? roles[0] : navigate("/login");

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

  const handleStatusChange = (newStatus) => {
    // TODO: Implement status change logic
  };

  const statusKey = (application?.status || application?.Status || "")
    .toString()
    .toUpperCase();

  const statusLabel = STATUS_LABELS[statusKey] || statusKey || "Unbekannt";
  const statusClass = statusKey.toLowerCase();

  const createdAtLabel = useMemo(() => {
    const rawCreated = application?.created_at || application?.createdAt;
    if (!rawCreated) return "—";
    const createdDate = new Date(rawCreated);
    if (Number.isNaN(createdDate.getTime())) return String(rawCreated);
    return createdDate.toLocaleString("de-DE");
  }, [application?.created_at, application?.createdAt]);

  const payloadEntries = useMemo(() => {
    const rawPayload = application?.jsonPayload || application?.payload || {};
    if (!rawPayload || typeof rawPayload !== "object") {
      return [];
    }
    return Object.entries(rawPayload);
  }, [application?.jsonPayload, application?.payload]);

  const handleGoBack = () => {
    const fromPath = location.state?.from;
    if (fromPath) {
      navigate(fromPath, { replace: false });
      return;
    }

    if (window.history.length > 1) {
      navigate(-1);
      return;
    }

    const fallbackPath = CONTEXT_FALLBACKS[sourceContext];
    if (fallbackPath) {
      navigate(fallbackPath, { replace: false });
      return;
    }

    navigate("/");
  };

  const renderWorkflow = () => {
    const steps = ["Eingereicht", "In Prüfung", "Entscheidung"];

    const currentIndex =
      statusKey === "APPROVED"
        ? 2
        : statusKey === "REJECTED"
        ? 2
        : statusKey === "PENDING"
        ? 1
        : 0;

    return (
      <div className="status-flow-info">
        <h4>Bearbeitungsstatus</h4>
        <div className="workflow-steps">
          {steps.map((step, index) => {
            const isCurrent = index === currentIndex;
            const isCompleted = index < currentIndex;
            let stepClass = "workflow-step";
            if (isCurrent) stepClass += " current";
            if (isCompleted) stepClass += " completed";
            if (statusKey === "APPROVED" && index === 2) {
              stepClass += " completed";
            }

            if (statusKey === "REJECTED" && index === currentIndex) {
              stepClass += " rejected";
            }
            return (
              <Fragment key={`workflow-${index}`}>
                <div className={stepClass}>{step}</div>
                {index < steps.length - 1 && (
                  <div className="workflow-arrow">→</div>
                )}
              </Fragment>
            );
          })}
        </div>
        {statusKey === "APPROVED" && (
          <div className="workflow-step completed">Antrag wurde genehmigt</div>
        )}
        {statusKey === "REJECTED" && (
          <div className="workflow-step rejected">Antrag wurde abgelehnt</div>
        )}
      </div>
    );
  };

  const renderRoleSpecificActions = () => {
    const isApproved = statusKey === "APPROVED";
    const isRejected = statusKey === "REJECTED";
    const isPublished = application?.is_public;

    if (currentRole === Role.ADMIN) {
      return (
        <div className="button-group">
          {!isApproved && (
            <button
              type="button"
              className="action-btn approve-btn"
              onClick={() => handleStatusChange("APPROVED")}
            >
              Genehmigen
            </button>
          )}
          {!isRejected && (
            <button
              type="button"
              className="action-btn reject-btn"
              onClick={() => handleStatusChange("REJECTED")}
            >
              Ablehnen
            </button>
          )}
          {!isPublished && isApproved && (
            <button
              type="button"
              className="action-btn publish-btn"
              onClick={() => handleStatusChange("PUBLISHED")}
            >
              Veröffentlichen
            </button>
          )}
        </div>
      );
    }

    if (currentRole === Role.APPLICANT) {
      return (
        <div className="button-group">
          {!(isPublished || isApproved || isRejected) && (
            <button
              type="button"
              className="action-btn edit-btn"
              onClick={() =>
                navigate(
                  `/applicant/application-revise/${formId}/${applicationId}`
                )
              }
            >
              Antrag bearbeiten
            </button>
          )}
          <button type="button" className="action-btn info-btn" disabled>
            Rückfragen stellen
          </button>
        </div>
      );
    }

    if (currentRole === Role.REPORTER) {
      return (
        <div className="button-group">
          <button type="button" className="action-btn info-btn" disabled>
            Verlauf exportieren
          </button>
        </div>
      );
    }

    return (
      <div className="button-group">
        <button type="button" className="action-btn info-btn" disabled>
          Keine Aktionen verfügbar
        </button>
      </div>
    );
  };

  if (isLoading) {
    return (
      <>
        <Navbar />
        <div className="application-view">
          <div className="loading">Antrag wird geladen…</div>
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
  const iconForStatus =
    statusKey === "APPROVED"
      ? FaCheckCircle
      : statusKey === "REJECTED"
      ? FaTimesCircle
      : FaClock;

  const IconComponent = iconForStatus;

  return (
    <>
      <Navbar />
      <div className="application-view">
        <div className="view-container">
          <header className="view-header">
            <button type="button" className="back-btn" onClick={handleGoBack}>
              <FaArrowLeft /> Zurück
            </button>
            <div className="header-info">
              <IconComponent className="icon-large" />
              <div className="header-text">
                <h1>{applicationTitle}</h1>
                <div className={`status-badge ${statusClass}`}>
                  {statusLabel}
                </div>
                {application.is_public && (
                  <div className="public-indicator" title="Öffentlich sichtbar">
                    <BiWorld className="world-icon" />
                    <FaEye className="eye-icon" />
                  </div>
                )}
                <p style={{ margin: "8px 0 0 0" }}>
                  Antrag #{application.id} · Formular #
                  {application.form_id || application.formId}
                </p>
              </div>
            </div>
          </header>

          <section className="metadata-section">
            <h2>Metadaten</h2>
            <div className="metadata-text">
              <p>
                <strong>Formular-ID:</strong>{" "}
                {application.form_id || application.formId}
              </p>
              <p>
                <strong>Aktueller Status:</strong> {statusLabel}
              </p>
              <p>
                <strong>Erstellt am:</strong> {createdAtLabel}
              </p>
              <p>
                <strong>Öffentlich:</strong>{" "}
                {application.is_public ? "Ja" : "Nein"}
              </p>
              {(application.currentSnapshotID ||
                application.previousSnapshotID) &&
                application.previousSnapshotID !== -1 && (
                  <p>
                    <strong>Snapshots:</strong> aktuelle #
                    {application.currentSnapshotID || "–"}, vorherige #
                    {application.previousSnapshotID || "–"}
                  </p>
                )}
            </div>
            {renderWorkflow()}
          </section>

          <section className="form-data-section">
            <h2>Formulardaten</h2>
            {payloadEntries.length === 0 ? (
              <div className="form-data-text">
                <p>Keine Formulardaten vorhanden.</p>
              </div>
            ) : (
              <div className="form-data-text">
                {payloadEntries.map(([key, value]) => {
                  // Extract the actual value from the payload object structure
                  const displayValue =
                    typeof value === "object" && value?.value !== undefined
                      ? value.value
                      : typeof value === "object"
                      ? JSON.stringify(value, null, 2)
                      : String(value);

                  // Extract the label from the payload object structure, fallback to key
                  const displayLabel =
                    typeof value === "object" && value?.label
                      ? value.label
                      : key;

                  return (
                    <p key={key}>
                      <strong>{displayLabel}:</strong> {displayValue}
                    </p>
                  );
                })}
              </div>
            )}
          </section>

          <section className="action-buttons">
            <h3>Verfügbare Aktionen</h3>
            {renderRoleSpecificActions()}
          </section>

          {(currentRole === Role.ADMIN || currentRole === Role.REPORTER) && (
            <section className="revision-section">
              <h2>Historie</h2>
              <div className="revision-info">
                <p>
                  <FaHistory style={{ marginRight: "8px" }} />
                  Hier können Sie den kompletten Änderungsverlauf einsehen.
                </p>
                <button
                  type="button"
                  className="action-btn info-btn"
                  onClick={() =>
                    navigate(`/applications/${formId}/${applicationId}/revisions`)
                  }
                >
                  <FaHistory style={{ marginRight: "8px" }} />
                  Antragshistorie ansehen
                </button>
              </div>
            </section>
          )}
        </div>
      </div>
    </>
  );
}
