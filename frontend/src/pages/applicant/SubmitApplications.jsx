import "./../../style/AdminApplicantReporterPage.css";
import Navbar from "../../components/Navbar";
import { FaDog, FaFire, FaInfoCircle } from "react-icons/fa";
import { useNavigate } from "react-router-dom";
import { Role } from "../../utils/const";
import { useQuery } from "@tanstack/react-query";
import { getAllForms } from "../../utils/api";

export default function SubmitApplications() {
  const navigate = useNavigate();

  // Icon mapping for different form types
  const getIconForFormType = (formName) => {
    const lowerFormName = formName?.toLowerCase() || "";
    if (lowerFormName.includes("hund") || lowerFormName.includes("dog")) {
      return <FaDog />;
    } else if (
      lowerFormName.includes("feuer") ||
      lowerFormName.includes("fire")
    ) {
      return <FaFire />;
    } else {
      return <FaInfoCircle />;
    }
  };

  const {
    data: formsData,
    isLoading: formsLoading,
    error: formsError,
    refetch: refetchForms,
  } = useQuery({
    queryKey: ["allForms"],
    queryFn: getAllForms,
    enabled: true, // Enable automatic fetching when component mounts
    retry: 1,
  });

  const handleEditApplication = (formId) => {
    alert(`ApplicationContainer - Navigating to form ID: ${formId}`);

    navigate(`/applicant/application-edit/${formId}`);
  };

  return (
    <>
      <Navbar />
      <div className="page-container">
        <div className="containers-card">
          <h2 className="card-title">Antrag einreichen</h2>

          {/* Loading State */}
          {formsLoading && (
            <div className="loading-message">
              <p>Formulare werden geladen...</p>
            </div>
          )}

          {/* Error State */}
          {formsError && (
            <div className="error-message">
              <p>Fehler beim Laden der Formulare: {formsError.message}</p>
              <button onClick={() => refetchForms()} className="retry-btn">
                Erneut versuchen
              </button>
            </div>
          )}

          {/* Forms List */}
          {formsData && Array.isArray(formsData) && formsData.length > 0 && (
            <div className="container-list">
              {formsData.map((form) => (
                <div key={form.id} className="container-item">
                  <div className="container-header">
                    <div className="icon">
                      {getIconForFormType(form.form_name)}
                    </div>
                    <div className="info">
                      <div className="form-type">{form.form_name}</div>
                      {form.description && (
                        <div className="form-description">
                          {form.description}
                        </div>
                      )}
                    </div>
                    <button
                      className="toggle-btn"
                      onClick={() => handleEditApplication(form.id)}
                    >
                      Ausfüllen
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}

          {/* No Forms State */}
          {formsData && Array.isArray(formsData) && formsData.length === 0 && (
            <div className="no-forms-message">
              <p>Keine Formulare verfügbar.</p>
            </div>
          )}
          <div className="page-space"></div>
        </div>
      </div>
    </>
  );
}
