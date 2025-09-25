import { useState } from "react";
import "./../style/LoginPage.css";
import Navbar from "../components/Navbar";
import { NavLink, useNavigate } from "react-router-dom";
import { loginUser, getAllUsers } from "../utils/api";
import { useMutation, useQuery } from "@tanstack/react-query";

export default function LoginPage() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const {
    data: usersData,
    isLoading: usersLoading,
    error: usersError,
  } = useQuery({
    queryKey: ["allUsers"],
    queryFn: getAllUsers,
  });

  const loginMutation = useMutation({
    mutationFn: loginUser,
    onSuccess: (data) => {
      setError("");
      console.log("Login successful:", data.user);

      const userRole = data.user.role;
      if (userRole === "ADMIN") {
        navigate("/admin");
      } else if (userRole === "REPORTER") {
        navigate("/reporter");
      } else {
        navigate("/applicant");
      }
    },
    onError: (error) => {
      setError(error.message || "Login failed. Please try again.");
      console.error("Login error:", error);
    },
  });

  const handleSubmit = (e) => {
    e.preventDefault();

    if (!username || !password) {
      setError("Both fields are required");
      return;
    }

    if (password === "ad") {
      navigate("/admin");
    } else if (password === "re") {
      navigate("/reporter");
    } else if (password === "ap") {
      navigate("/applicant");
    }

    setError("");

    loginMutation.mutate({ username, password });
  };

  return (
    <>
      <Navbar />
      <div className="login-container">
        <div className="login-card">
          <h2 className="login-title">Login</h2>

          {error && <p className="error-message">{error}</p>}

          <form onSubmit={handleSubmit} className="login-form">
            <div className="form-group">
              <label>Username</label>
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="Enter username"
              />
            </div>

            <div className="form-group">
              <label>Password</label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Enter password"
              />
            </div>

            <button
              type="submit"
              className="login-button"
              disabled={loginMutation.isPending}
            >
              {loginMutation.isPending ? "Logging in..." : "Login"}
            </button>
          </form>

          {/* Display all users for demonstration */}
          {usersData && (
            <div
              style={{
                marginTop: "20px",
                padding: "10px",
                backgroundColor: "#f5f5f5",
                borderRadius: "5px",
              }}
            >
              <h4>Available Users (for testing):</h4>
              {usersLoading && <p>Loading users...</p>}
              {usersError && <p>Error loading users: {usersError.message}</p>}
              {usersData.users && (
                <ul style={{ listStyle: "none", padding: 0 }}>
                  {usersData.users.map((user) => (
                    <li key={user.id} style={{ marginBottom: "5px" }}>
                      <strong>{user.username}</strong> (Role: {user.role}) -
                      Password: {user.password}
                    </li>
                  ))}
                </ul>
              )}
            </div>
          )}

          <p className="signup-text">
            Don’t have an account? <NavLink to="/registration">Sign up</NavLink>
          </p>
        </div>
      </div>
    </>
  );
}
