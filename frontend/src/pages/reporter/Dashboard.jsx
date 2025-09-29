// Reporter dashboard listing with filtering capabilities

import { useState, useMemo } from "react";
import { useQuery } from "@tanstack/react-query";
import "./../../style/AdminApplicantReporterPage.css";
import Navbar from "./../../components/Navbar";
import ApplicationContainer from "./../../components/ApplicationContainer";
import { Role } from "../../utils/const";
import { getAllApplications, getAllForms } from "../../utils/api";

const toDateOrNull = (value) => {
  if (!value) return null;
  const parsed = new Date(value);
  return Number.isNaN(parsed.getTime()) ? null : parsed;
};

const formatStatusOption = (status) => {
  if (!status) return "Unbekannt";
  const lower = status.toLowerCase();
  return lower.charAt(0).toUpperCase() + lower.slice(1);
};

export default function ReporterPage() {
  const [statusFilter, setStatusFilter] = useState("");
  const [formFilter, setFormFilter] = useState("");
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");

  const {
    data: applicationsData,
    isLoading: applicationsLoading,
    error: applicationsError,
    refetch: refetchApplications,
  } = useQuery({
    queryKey: ["AllApplications"],
    queryFn: getAllApplications,
    retry: 1,
  });

  const {
    data: formsData,
    isLoading: formsLoading,
    error: formsError,
    refetch: refetchForms,
  } = useQuery({
    queryKey: ["AllForms"],
    queryFn: getAllForms,
    retry: 1,
  });

  const forms = formsData ?? [];
  const applications = applicationsData ?? [];

  const formMap = useMemo(() => {
    const map = new Map();
    forms.forEach((form) => {
      const id = form.id ?? form.form_id ?? form.formId;
      if (id == null) return;
      const name =
        form.form_name ??
        form.formName ??
        form.name ??
        `Formular #${id}`;
      map.set(id, name);
    });
    return map;
  }, [forms]);

  const normalizedApplications = useMemo(() => {
    return applications.map((app) => {
      const id = app.id ?? app.applicationID ?? app.applicationId;
      const formId = app.form_id ?? app.formId ?? app.formID;
      const createdRaw = app.created_at ?? app.createdAt ?? null;
      const statusUpper = (app.status ?? "").toString().toUpperCase();
      const formName =
        app.formName ??
        app.form_name ??
        (formId != null ? formMap.get(formId) : undefined) ??
        `Formular #${formId ?? "?"}`;

      return {
        ...app,
        id,
        formId,
        status: statusUpper || app.status,
        formName,
        createdAt: createdRaw ?? app.createdAt ?? app.created_at,
        created_at: createdRaw ?? app.created_at ?? app.createdAt,
      };
    });
  }, [applications, formMap]);

  const statusOptions = useMemo(() => {
    const set = new Set();
    normalizedApplications.forEach((app) => {
      if (app.status) {
        set.add(app.status.toUpperCase());
      }
    });
    return Array.from(set).sort();
  }, [normalizedApplications]);

  const formOptions = useMemo(() => {
    const set = new Set();
    normalizedApplications.forEach((app) => {
      if (app.formName) {
        set.add(app.formName);
      }
    });
    return Array.from(set).sort((a, b) => a.localeCompare(b));
  }, [normalizedApplications]);

  const getApplicationDate = (app) => {
    const raw = app.createdAt ?? app.created_at;
    return toDateOrNull(raw);
  };

  const filteredApplications = useMemo(() => {
    return normalizedApplications
      .filter((app) => {
        const appStatus = (app.status ?? "").toUpperCase();
        if (statusFilter && appStatus !== statusFilter.toUpperCase()) {
          return false;
        }

        const appFormName = app.formName || "";
        if (formFilter && appFormName !== formFilter) {
          return false;
        }

        const appDate = getApplicationDate(app);
        if (startDate) {
          const start = toDateOrNull(startDate);
          if (!appDate || !start || appDate < start) {
            return false;
          }
        }

        if (endDate) {
          const end = toDateOrNull(endDate);
          if (!appDate || !end) {
            return false;
          }
          const endOfDay = new Date(end);
          endOfDay.setHours(23, 59, 59, 999);
          if (appDate > endOfDay) {
            return false;
          }
        }

        return true;
      })
      .sort((a, b) => {
        const dateA = getApplicationDate(a)?.getTime() ?? 0;
        const dateB = getApplicationDate(b)?.getTime() ?? 0;
        return dateB - dateA;
      });
  }, [normalizedApplications, statusFilter, formFilter, startDate, endDate]);

  const isLoading = applicationsLoading || formsLoading;
  const combinedError = applicationsError || formsError;

  const handleRetry = () => {
    if (refetchApplications) refetchApplications();
    if (refetchForms) refetchForms();
  };

  const handleResetFilters = () => {
    setStatusFilter("");
    setFormFilter("");
    setStartDate("");
    setEndDate("");
  };

  const handleExport = () => {
    const exportData = filteredApplications.map(({ jsonPayload, ...rest }) => ({
      ...rest,
      formName: rest.formName,
    }));

    const blob = new Blob([JSON.stringify(exportData, null, 2)], {
      type: "application/json",
    });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = `applications-export-${new Date()
      .toISOString()
      .split("T")[0]}.json`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.URL.revokeObjectURL(url);
  };

  return (
    <>
      <Navbar role={Role.REPORTER} />
      <div className="filter-bar">
        <div className="filter-group">
          <label htmlFor="status-filter">Status</label>
          <select
            id="status-filter"
            value={statusFilter}
            onChange={(event) => setStatusFilter(event.target.value)}
          >
            <option value="">Alle</option>
            {statusOptions.map((status) => (
              <option key={status} value={status}>
                {formatStatusOption(status)}
              </option>
            ))}
          </select>
        </div>

        <div className="filter-group">
          <label htmlFor="form-filter">Antragstyp</label>
          <select
            id="form-filter"
            value={formFilter}
            onChange={(event) => setFormFilter(event.target.value)}
          >
            <option value="">Alle</option>
            {formOptions.map((name) => (
              <option key={name} value={name}>
                {name}
              </option>
            ))}
          </select>
        </div>

        <div className="filter-group">
          <label htmlFor="start-date">Von Datum</label>
          <input
            id="start-date"
            type="date"
            value={startDate}
            onChange={(event) => setStartDate(event.target.value)}
          />
        </div>

        <div className="filter-group">
          <label htmlFor="end-date">Bis Datum</label>
          <input
            id="end-date"
            type="date"
            value={endDate}
            onChange={(event) => setEndDate(event.target.value)}
          />
        </div>

        <div className="filter-actions">
          <button
            type="button"
            className="reset-btn"
            onClick={handleResetFilters}
          >
            Filter zurücksetzen
          </button>
          <button
            type="button"
            className="export-btn"
            onClick={handleExport}
          >
            Exportieren
          </button>
        </div>
      </div>

      <ApplicationContainer
        applications={filteredApplications}
        title={`Anträge (${filteredApplications.length})`}
        enableFetch={false}
        isLoadingOverride={isLoading}
        errorOverride={combinedError}
        onRetry={handleRetry}
      />
    </>
  );
}
