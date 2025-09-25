import { useState } from "react";
import "./../style/LoginPage.css";
import Navbar from "../components/Navbar";
import { NavLink, useNavigate } from "react-router-dom";
import { loginUser, getAllUsers } from "../utils/api";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

export default function LoginPage() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  const {
    data: usersData,
    isLoading: usersLoading,
    error: usersError,
    refetch: refetchUsers,
  } = useQuery({
    queryKey: ["allUsers"],
    queryFn: getAllUsers,
    enabled: false, // Disable automatic query execution
    retry: false, // Don't retry failed requests
  });

  const loginMutation = useMutation({
    mutationFn: loginUser,
    onSuccess: (data) => {
      setError("");
      console.log("Login successful:", data);

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

          {/* Display all users for demonstration
          <div
            style={{
              marginTop: "20px",
              padding: "10px",
              backgroundColor: "#f5f5f5",
              borderRadius: "5px",
            }}
          >
            <h4>Available Users (for testing):</h4>
            <button
              onClick={() => refetchUsers()}
              style={{ marginBottom: "10px", padding: "5px 10px" }}
              disabled={usersLoading}
            >
              {usersLoading ? "Loading..." : "Fetch Users"}
            </button>
            {usersLoading && <p>Loading users...</p>}
            {usersError && <p>Error loading users: {usersError.message}</p>}
            {usersData && Array.isArray(usersData) && usersData.length > 0 && (
              <ul style={{ listStyle: "none", padding: 0 }}>
                {usersData.map((user) => (
                  <li key={user.id} style={{ marginBottom: "5px" }}>
                    <strong>{user.username}</strong>
                    {user.user_roles && user.user_roles.length > 0 && (
                      <span> (Role: {user.user_roles[0].role})</span>
                    )}
                    <span> - Email: {user.email}</span>
                  </li>
                ))}
              </ul>
            )}
            {usersData &&
              Array.isArray(usersData) &&
              usersData.length === 0 && <p>No users found.</p>}
          </div> */}

          <p className="signup-text">
            Don’t have an account? <NavLink to="/registration">Sign up</NavLink>
          </p>
        </div>
      </div>
    </>
  );
}
