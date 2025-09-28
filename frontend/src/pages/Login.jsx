import { useState } from "react";
import "./../style/LoginPage.css";
import Navbar from "../components/Navbar";
import { NavLink, useNavigate } from "react-router-dom";
import { loginUser, getAllUsers } from "../utils/api";
import { useMutation, useQuery } from "@tanstack/react-query";
import { saveToken } from "../utils/data";

export default function LoginPage() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const {
    data: usersData,
    isLoading: usersLoading,
    error: usersError,
    refetch: refetchUsers,
  } = useQuery({
    queryKey: ["allUsers"],
    queryFn: getAllUsers,
    enabled: false,
    retry: false,
  });

  const loginMutation = useMutation({
    mutationFn: loginUser,
    onSuccess: (data) => {
      setError("");
      console.log("Anmeldung erfolgreich:", data);

      saveToken(data);

      if (data.roles && data.roles.length > 0) {
        const primaryRole = data.roles[0];

        switch (primaryRole) {
          case "ADMIN":
            navigate("/admin");
            break;
          case "REPORTER":
            navigate("/reporter");
            break;
          case "APPLICANT":
            navigate("/applicant");
            break;
        }
      }
    },
    onError: (error) => {
      setError(
        error.message ||
          "Anmeldung fehlgeschlagen. Bitte versuchen Sie es erneut."
      );
      console.error("Login error:", error);
    },
  });

  const handleSubmit = (e) => {
    e.preventDefault();

    if (!username || !password) {
      setError("Beide Felder sind erforderlich");
      return;
    }

    setError("");
    loginMutation.mutate({ username, password });
  };

  return (
    <>
      <Navbar />
      <div className="login-container">
        <div className="login-card">
          <h2 className="login-title">Anmeldung</h2>

          {error && <p className="error-message">{error}</p>}

          <form onSubmit={handleSubmit} className="login-form">
            <div className="form-group">
              <label htmlFor="username">Benutzername</label>
              <input
                id="username"
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="Benutzername eingeben"
              />
            </div>

            <div className="form-group">
              <label htmlFor="password">Passwort</label>
              <input
                id="password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Passwort eingeben"
              />
            </div>

            <button
              type="submit"
              className="login-button"
              disabled={loginMutation.isPending}
            >
              {loginMutation.isPending ? "Anmeldung läuft..." : "Anmelden"}
            </button>
          </form>

          {/* Display all users for demonstration */}
          <div
            style={{
              marginTop: "20px",
              padding: "10px",
              backgroundColor: "#f5f5f5",
              borderRadius: "5px",
            }}
          >
            <h4>Verfügbare Benutzer (zum Testen):</h4>
            <button
              onClick={() => refetchUsers()}
              style={{ marginBottom: "10px", padding: "5px 10px" }}
              disabled={usersLoading}
            >
              {usersLoading ? "Laden..." : "Benutzer abrufen"}
            </button>
            {usersLoading && <p>Benutzer werden geladen...</p>}
            {usersError && (
              <p>Fehler beim Laden der Benutzer: {usersError.message}</p>
            )}
            {usersData && Array.isArray(usersData) && usersData.length > 0 && (
              <ul style={{ listStyle: "none", padding: 0 }}>
                {usersData.map((user) => (
                  <li key={user.id} style={{ marginBottom: "5px" }}>
                    <strong>{user.username}</strong>
                    {user.user_roles && user.user_roles.length > 0 && (
                      <span> (Rolle: {user.user_roles[0].role})</span>
                    )}
                    <span> - Email: {user.email}</span>
                  </li>
                ))}
              </ul>
            )}
            {usersData &&
              Array.isArray(usersData) &&
              usersData.length === 0 && <p>Keine Benutzer gefunden.</p>}
          </div>

          <p className="signup-text">
            Sie besitzen noch keinen Account?{" "}
            <NavLink to="/registration">Registrieren</NavLink>
          </p>
        </div>
      </div>
    </>
  );
}
