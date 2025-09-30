import { Routes, Route } from "react-router-dom";
import "./style/fonts.css"; /* Chose Atkinson Hyperlegible as font */
import "./style/App.css"; /* Global styles, rn only font-family */
import Login from "./pages/Login";
import AdminDashboard from "./pages/admin/Dashboard";
import ApplicantRegistration from "./pages/Registration";
import ApplicantDashboard from "./pages/applicant/Dashboard";
import SubmitApplications from "./pages/applicant/SubmitApplications";
import PublicApplication from "./pages/PublicApplication";
import ApplicationEdit from "./pages/applicant/ApplicationEdit";
import ApplicationRevise from "./pages/applicant/ApplicationRevise";
import ApplicationRevision from "./pages/ApplicationRevision";
import AdminRegistration from "./pages/admin/AdminRegistration";
import ReporterRegistration from "./pages/admin/ReporterRegistration";
import ApplicationView from "./pages/ApplicationView";
import CreateForms from "./pages/admin/CreateForms";
import ReporterDashboard from "./pages/reporter/Dashboard";
import RejectedApplication from "./pages/Rejected";
import ApprovedApplication from "./pages/Approved";
import PendingApplication from "./pages/Pending";

const App = () => {
  return (
    <>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/registration" element={<ApplicantRegistration />} />
        <Route path="/applicant" element={<ApplicantDashboard />} />
        <Route path="/applicant/submit" element={<SubmitApplications />} />
        <Route path="/applicant/public" element={<PublicApplication />} />
        <Route
          path="/applicant/application-edit/:id"
          element={<ApplicationEdit />}
        />
        <Route
          path="/applicant/application-revise/:formId/:applicationId"
          element={<ApplicationRevise />}
        />
        <Route path="/admin" element={<AdminDashboard />} />
        <Route path="/reporter" element={<ReporterDashboard />} />
        <Route path="/admin/public" element={<PublicApplication />} />
        <Route
          path="/admin/admin-registration"
          element={<AdminRegistration />}
        />
        <Route
          path="/admin/reporter-registration"
          element={<ReporterRegistration />}
        />
        <Route path="/admin/create-forms" element={<CreateForms />} />
        <Route
          path="/applications/:formId/:applicationId"
          element={<ApplicationView />}
        />
        <Route
          path="/applications/:formId/:applicationId/revisions"
          element={<ApplicationRevision />}
        />

        <Route path="/reporter/approved" element={<ApprovedApplication />} />
        <Route path="/reporter/public" element={<PublicApplication />} />
        <Route path="/reporter/rejected" element={<RejectedApplication />} />
        <Route path="/reporter/pending" element={<PendingApplication />} />
      </Routes>
    </>
  );
};

export default App;
