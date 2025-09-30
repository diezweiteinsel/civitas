import "./../../style/AdminApplicantReporterPage.css";
import Navbar from "./../../components/Navbar";
import { Role } from "../../utils/const";
import ApplicationContainer from "./../../components/ApplicationContainer";

export default function AdminPage() {
  return (
    <>
      <Navbar role={Role.ADMIN} />
      <div className="page-container">
        <ApplicationContainer applications={[]} title="Ausstehende Anträge:" />
        <div className="page-space"> </div>
        <ApplicationContainer applications={[]} title="Genehmigte Anträge:" />
      </div>
    </>
  );
}
