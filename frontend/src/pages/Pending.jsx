import "./../style/AdminApplicantReporterPage.css";
import Navbar from "../components/Navbar";
import ApplicationContainer from "../components/ApplicationContainer";
import { useSearchParams } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { Role } from "../utils/const";
import { getApplicationsByStatus } from "../utils/api";

export default function PendingApplication() {
  const [searchParams] = useSearchParams();
  const sourceRole = searchParams.get("from");

  const currentRole =
    sourceRole === "reporter"
      ? Role.REPORTER
      : Role.EMPTY;

  const {
    data: applications = [],
    isLoading,
    error,
    refetch,
  } = useQuery({
    queryKey: ["applications", "status", "PENDING"],
    queryFn: () => getApplicationsByStatus(["PENDING"]),
    retry: 1,
  });



  return (
    <>
      <Navbar />
      <ApplicationContainer
        applications={applications}
        title="Ausstehende Anträge:"
        enableFetch={false}
        isLoadingOverride={isLoading}
        errorOverride={error}
        onRetry={refetch}
      />
    </>
  );
}