import { Routes, Route } from "react-router-dom";
import Login from "./pages/Login";
import AdminDashboard from "./pages/admin/Dashboard";
import ApplicantRegistration from "./pages/Registration";
import ApplicantDashboard from "./pages/applicant/Dashboard";
import SubmitApplications from "./pages/applicant/SubmitApplications";
import PublicApplication from "./pages/PublicApplication";
import ApplicationEdit from "./pages/applicant/ApplicationEdit";
import AdminRegistration from "./pages/admin/AdminRegistration";
import ReporterRegistration from "./pages/admin/ReporterRegistration";
import ApplicationView from "./pages/ApplicationView";
import CreateForms from "./pages/admin/CreateForms";
import ReporterDashboard from "./pages/reporter/Dashboard";

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
        <Route path="/application/:id" element={<ApplicationView />} />
      </Routes>
    </>
  );
};

export default App;
