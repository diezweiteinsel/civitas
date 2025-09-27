import { getToken } from "./data";

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
  const accessToken = getToken();

  const headers = {
    "Content-Type": "application/json",
  };

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

// WORKS
export const getAllApplications = async () => {
  const accessToken = getToken();
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

export const getApplicationById = async (application_id) => {
  const accessToken = getToken();
  const headers = {
    "Content-Type": "application/json",
  };
  if (accessToken) {
    headers.Authorization = `Bearer ${accessToken}`;
  }

  const response = await fetch(
    `${API_BASE_URL}/api/v1/applications/${application_id}`,
    {
      method: "GET",
      headers: headers,
    }
  );

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
  const accessToken = getToken();
  const headers = {
    "Content-Type": "application/json",
  };
  if (accessToken) {
    headers.Authorization = `Bearer ${accessToken}`;
  }

  // Structure the data to match backend expectations
  const requestBody = {
    user_id: applicationData.user_id || 1, // Default to user 1 if not provided
    form_id: applicationData.form_id || 1, // Default to form 1 if not provided
    payload: applicationData.payload || applicationData, // Use payload if provided, otherwise use the entire data
  };

  const response = await fetch(`${API_BASE_URL}/api/v1/applications`, {
    method: "POST",
    headers: headers,
    body: JSON.stringify(requestBody),
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(
      errorData.detail || errorData.error || "Failed to create application"
    );
  }

  const application = await response.json();
  return application;
};
