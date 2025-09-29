import Navbar from "../components/Navbar";
import ApplicationContainer from "../components/ApplicationContainer";
import { useSearchParams } from "react-router-dom";
import { Role } from "../utils/const";

export default function PendingApplication() {
  const [searchParams] = useSearchParams();
  const sourceRole = searchParams.get("from");

  const currentRole =
    sourceRole === "admin"
      ? Role.ADMIN
      : sourceRole === "applicant"
      ? Role.REPORTER
      :sourceRole === "reporter"
      ? Role.APPLICANT
      : Role.EMPTY;

  const getTitle = () => {
    if (sourceRole === "admin") return "Admin-Ansicht – Ausstehende Anträge:";
    if (sourceRole === "applicant")
      return "Bürger-Ansicht – Ausstehende Anträge:";
    if (sourceRole === "reporter") return "Reporter-Ansicht - Ausstehende Anträge:"
    return "Öffentliche Anträge:";
  };

  return (
    <>
      <Navbar role={currentRole} />
      <ApplicationContainer applications={[]} title={getTitle()} />
    </>
  );
}