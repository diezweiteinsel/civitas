import { useState, useEffect } from "react";
import "./../style/AdminApplicantReporterPage.css";
import Navbar from "../components/Navbar";
import ApplicationContainer from "../components/ApplicationContainer";
import { useSearchParams } from "react-router-dom";
import { Role } from "../utils/const";

export default function PublicApplication() {
  const [searchParams] = useSearchParams();
  const sourceRole = searchParams.get("from");

  const currentRole =
    sourceRole === "admin"
      ? Role.ADMIN
      : sourceRole === "applicant"
      ? Role.APPLICANT
      : Role.EMPTY;

  const getTitle = () => {
    if (sourceRole === "admin") return "Admin View - Public Applications:";
    if (sourceRole === "applicant")
      return "Applicant View - Public Applications:";
    return "Public Applications:";
  };

  return (
    <>
      <Navbar role={currentRole} />
      <ApplicationContainer applications={[]} title={getTitle()} />
    </>
  );
}
