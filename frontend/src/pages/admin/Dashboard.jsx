import "../../style/AdminApplicantReporterPage.css";
import Navbar from "./../../components/Navbar";
import { Role } from "../../utils/const";
import ApplicationContainer from "./../../components/ApplicationContainer";

export default function AdminPage() {
  return (
    <>
      <Navbar />
      <div className="page-container">
        <ApplicationContainer
          statuses={["PENDING"]}
          title="Ausstehende Anträge:"
        />
        <div className="page-space"> </div>
        <ApplicationContainer
          statuses={["APPROVED"]}
          title="Genehmigte Anträge:"
        />
      </div>
    </>
  );
}
