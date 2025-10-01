import { useState } from "react";
import { useMutation } from "@tanstack/react-query";
import { NavLink, useNavigate } from "react-router-dom";
import { Role } from "../utils/const";
import { createUser } from "../utils/api";
import "./../style/RegisterPage.css";

export default function RegistrationContainer({
  roleToRegister = Role.APPLICANT,
}) {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirm, setConfirm] = useState("");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const navigate = useNavigate();
  const title =
    {
      [Role.ADMIN]: "Admin ",
      [Role.REPORTER]: "Reporter ",
      [Role.APPLICANT]: "Bürger/-innen ",
    }[roleToRegister] || "Bürger/-innen ";

  // Function to reset form fields
  const resetForm = () => {
    setUsername("");
    setEmail("");
    setPassword("");
    setConfirm("");
    setError("");
  };

  // Mutation for creating a user
  const createUserMutation = useMutation({
    mutationFn: createUser,
    onSuccess: (data) => {
      setError("");
      alert("Registration successful!");
      setSuccess("Registration successful!");
      console.log("User created successfully:", data);

      resetForm();

      setTimeout(() => {
        setSuccess("");
      }, 3000);

      switch (roleToRegister) {
        case Role.ADMIN:
          break;
        case Role.REPORTER:
          break;
        case Role.APPLICANT:
          setTimeout(() => {
            navigate("/");
          }, 1500);
          break;
        default:
          setTimeout(() => {
            navigate("/");
          }, 1500);
      }
    },
    onError: (error) => {
      setSuccess("");
      setError(error.message || "Registration failed. Please try again.");
      console.error("Registration error:", error);
    },
  });

  // Handle form submission
  const handleSubmit = (e) => {
    e.preventDefault();

    if (!username || !password || !confirm) {
      setError("All fields are required");
      setSuccess("");
      return;
    }

    if (password !== confirm) {
      setError("Passwords do not match");
      setSuccess("");
      return;
    }

    createUserMutation.mutate({
      username,
      email,
      password,
      role: roleToRegister,
    });
  };

  return (
    <div className="register-container">
      <div className="register-card">
        <h2 className="register-title">{title}Registrieren</h2>

        {error && <p className="error-message">{error}</p>}
        {success && <p className="success-message">{success}</p>}

        <form onSubmit={handleSubmit} className="register-form">
          <div className="form-group">
            <label>Benutzername</label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="Benutzername eingeben"
            />
          </div>

          <div className="form-group">
            <label>Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="Email eingeben"
            />
          </div>

          <div className="form-group">
            <label>Passwort</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Passwort eingeben"
            />
          </div>

          <div className="form-group">
            <label>Passwort bestätigen</label>
            <input
              type="password"
              value={confirm}
              onChange={(e) => setConfirm(e.target.value)}
              placeholder="Passwort bestätigen"
            />
          </div>

          <button
            type="submit"
            className="register-button"
            disabled={createUserMutation.isPending}
          >
            {createUserMutation.isPending
              ? "Account erstellen..."
              : "Registrieren"}
          </button>
          {roleToRegister === Role.APPLICANT && (
            <p className="signup-text">
              Sie haben bereits einen Account?{" "}
              <NavLink to="/">Anmelden</NavLink>
            </p>
          )}
        </form>
      </div>
    </div>
  );
}
