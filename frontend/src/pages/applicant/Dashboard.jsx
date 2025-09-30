import "./../../style/AdminApplicantReporterPage.css";
import Navbar from "./../../components/Navbar";
import ApplicationContainer from "./../../components/ApplicationContainer";
import { Role } from "../../utils/const";

export default function ApplicantPage() {
  return (
    <>
      <Navbar />
      <ApplicationContainer title="Eigene Anträge:" />
    </>
  );
}
