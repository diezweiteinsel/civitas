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
      : Role.REPORTER
      ? sourceRole === "reporter"
      : Role.EMPTY;

  const getTitle = () => {
    if (sourceRole === "admin") return "Admin-Ansicht – Öffentliche Anträge:";
    if (sourceRole === "applicant")
      return "Bürger-Ansicht – Öffentliche Anträge:";
    if (sourceRole === "reporter")
      return "Reporter =-Ansicht - öffentliche Anträge";
    return "Öffentliche Anträge:";
  };

  return (
    <>
      <Navbar />
      <ApplicationContainer
        statuses={["APPROVED"]}
        isPublic={true}
        title={getTitle()}
      />
    </>
  );
}
