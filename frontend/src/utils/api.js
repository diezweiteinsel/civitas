const API_BASE_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";

// WORKS
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

// WORKS
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

// WORKS
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

export const getAllApplications = async () => {
  const accessToken = localStorage.getItem("access_token");
  const headers = {
    "Content-Type": "application/json",
  };
  if (accessToken) {
    headers.Authorization = `Bearer ${accessToken}`;
  }

  const response = await fetch(`${API_BASE_URL}/api/v1/applications`, {
    method: "GET",
    headers: headers,
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(
      errorData.detail || errorData.error || "Failed to fetch applications"
    );
  }

  const applications = await response.json();

  return applications;
};

export const getApplicationById = async (id) => {
  const accessToken = localStorage.getItem("access_token");
  const headers = {
    "Content-Type": "application/json",
  };
  if (accessToken) {
    headers.Authorization = `Bearer ${accessToken}`;
  }

  const response = await fetch(`${API_BASE_URL}/api/v1/applications/${id}`, {
    method: "GET",
    headers: headers,
    body: JSON.stringify(id),
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(
      errorData.detail || errorData.error || "Failed to fetch application by ID"
    );
  }

  const application = await response.json();

  return application;
};

export const createApplication = async (applicationData) => {
  const accessToken = localStorage.getItem("access_token");
  const headers = {
    "Content-Type": "application/json",
  };
  if (accessToken) {
    headers.Authorization = `Bearer ${accessToken}`;
  }

  const response = await fetch(`${API_BASE_URL}/api/v1/applications`, {
    method: "POST",
    headers: headers,
    body: JSON.stringify(applicationData),
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(
      errorData.detail || errorData.error || "Failed to create applications"
    );
  }

  const applications = await response.json();

  return applications;
};
