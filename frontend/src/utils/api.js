const API_BASE_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";

// works
export const createUser = async (userData) => {
  const response = await fetch(`${API_BASE_URL}/api/v1/users`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      username: userData.username,
      email: userData.email || "test@mail.com",
      password: userData.password,
      role: userData.role,
    }),
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.error || "Failed to create user");
  }

  return response.json();
};

export const loginUser = async (userData) => {
  // Create form data for OAuth2PasswordRequestForm
  const formData = new FormData();
  formData.append("username", userData.username);
  formData.append("password", userData.password);

  const response = await fetch(`${API_BASE_URL}/api/v1/auth/token`, {
    method: "POST",
    headers: {},
    body: formData,
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || errorData.error || "Failed to login");
  }

  const tokenData = await response.json();

  if (tokenData.access_token) {
    localStorage.setItem("access_token", tokenData.access_token);
  }

  return tokenData;
};

export const getAllUsers = async () => {
  // Get the access token from localStorage
  const accessToken = localStorage.getItem("access_token");

  const headers = {
    "Content-Type": "application/json",
  };

  // Add Authorization header if token exists
  if (accessToken) {
    headers.Authorization = `Bearer ${accessToken}`;
  }

  const response = await fetch(`${API_BASE_URL}/api/v1/users`, {
    method: "GET",
    headers: headers,
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(
      errorData.detail || errorData.error || "Failed to fetch users"
    );
  }

  const users = await response.json();

  return users;
};
