import { getToken } from "./data";

const API_BASE_URL = process.env.REACT_APP_API_URL; // || "http://localhost:8000";

// WORKS
export const createUser = async (userData) => {
  const response = await fetch(`${API_BASE_URL}/users`, {
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

  const response = await fetch(`${API_BASE_URL}/auth/token`, {
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

  const response = await fetch(`${API_BASE_URL}/users`, {
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

  const response = await fetch(`${API_BASE_URL}/applications`, {
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

export const getPublicApplications = async () => {
  const accessToken = getToken();
  const headers = {
    "Content-Type": "application/json",
  };
  if (accessToken) {
    headers.Authorization = `Bearer ${accessToken}`;
  }

  const response = await fetch(`${API_BASE_URL}/applications?public=true`, {
    method: "GET",
    headers: headers,
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(
      errorData.detail ||
        errorData.error ||
        "Failed to fetch public applications"
    );
  }

  const applications = await response.json();
  return applications;
};

export const getApplicationsByStatus = async (statuses) => {
  const accessToken = getToken();
  const headers = {
    "Content-Type": "application/json",
  };
  if (accessToken) {
    headers.Authorization = `Bearer ${accessToken}`;
  }

  // Create a new URLSearchParams object
  const params = new URLSearchParams();
  // Append each status to the params with the same key
  statuses.forEach((status) => params.append("status", status));

  // Use the generated query string
  const response = await fetch(
    `${API_BASE_URL}/applications?public=false&${params.toString()}`,
    {
      method: "GET",
      headers: headers,
    }
  );

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(
      errorData.detail ||
        errorData.error ||
        "Failed to fetch applications by status"
    );
  }

  const applications = await response.json();
  return applications;
};

export const getPublicApplicationsByStatus = async (statuses) => {
  const accessToken = getToken();
  const headers = {
    "Content-Type": "application/json",
  };
  if (accessToken) {
    headers.Authorization = `Bearer ${accessToken}`;
  }

  // Create a new URLSearchParams object
  const params = new URLSearchParams();
  // Append each status to the params with the same key
  statuses.forEach((status) => params.append("status", status));

  // Use the generated query string
  const response = await fetch(
    `${API_BASE_URL}/applications?public=true&${params.toString()}`,
    {
      method: "GET",
      headers: headers,
    }
  );

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(
      errorData.detail ||
        errorData.error ||
        "Failed to fetch public applications by status"
    );
  }

  const applications = await response.json();
  return applications;
};

export const getApplicationById = async (form_id, application_id) => {
  const accessToken = getToken();
  const headers = {
    "Content-Type": "application/json",
  };
  if (accessToken) {
    headers.Authorization = `Bearer ${accessToken}`;
  }

  // Changed URL structure
  const response = await fetch(
    `${API_BASE_URL}/applications/${form_id}/${application_id}`,
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

// WORKS
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
    form_id: applicationData.form_id,
    payload: applicationData.payload,
  };

  const response = await fetch(`${API_BASE_URL}/applications`, {
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

// WORKS
export const createForm = async (formData) => {
  const accessToken = getToken();
  const headers = {
    "Content-Type": "application/json",
  };
  if (accessToken) {
    headers.Authorization = `Bearer ${accessToken}`;
  }
  const response = await fetch(`${API_BASE_URL}/forms`, {
    method: "POST",
    headers: headers,
    body: JSON.stringify(formData),
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(
      errorData.detail || errorData.error || "Failed to create form"
    );
  }

  return response.json();
};

// WORKS
export const getAllForms = async () => {
  const accessToken = getToken();
  const headers = {
    "Content-Type": "application/json",
  };
  if (accessToken) {
    headers.Authorization = `Bearer ${accessToken}`;
  }

  const response = await fetch(`${API_BASE_URL}/forms`, {
    method: "GET",
    headers: headers,
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(
      errorData.detail || errorData.error || "Failed to fetch forms"
    );
  }

  const forms = await response.json();
  return forms;
};

export const getFormById = async (form_id) => {
  const accessToken = getToken();
  const headers = {
    "Content-Type": "application/json",
  };
  if (accessToken) {
    headers.Authorization = `Bearer ${accessToken}`;
  }

  const response = await fetch(`${API_BASE_URL}/forms/${form_id}`, {
    method: "GET",
    headers: headers,
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(
      errorData.detail || errorData.error || "Failed to fetch form by ID"
    );
  }

  const form = await response.json();
  return form;
};

export const updateApplication = async (applicationData) => {
  const accessToken = getToken();
  const headers = {
    "Content-Type": "application/json",
  };
  if (accessToken) {
    headers.Authorization = `Bearer ${accessToken}`;
  }

  const requestBody = {
    form_id: applicationData.form_id,
    application_id: applicationData.application_id,
    payload: applicationData.payload,
  };

  const response = await fetch(
    `${API_BASE_URL}/applications/${applicationData.form_id}/${applicationData.application_id}`,
    {
      method: "PUT",
      headers: headers,
      body: JSON.stringify(requestBody),
    }
  );

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(
      errorData.detail || errorData.error || "Failed to change application"
    );
  }

  const application = await response.json();
  return application;
};

export const updateApplicationStatus = async (
  form_id,
  application_id,
  status
) => {
  const accessToken = getToken();
  const headers = {
    "Content-Type": "application/json",
  };
  if (accessToken) {
    headers.Authorization = `Bearer ${accessToken}`;
  }

  const response = await fetch(
    `${API_BASE_URL}/applications/${form_id}/${application_id}?status=${status}`,
    {
      method: "PUT",
      headers: headers,
    }
  );

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(
      errorData.detail ||
        errorData.error ||
        "Failed to change application status"
    );
  }

  const application = await response.json();
  return application;
};

export const getAllRevisionsOfApplication = async (form_id, application_id) => {
  const accessToken = getToken();
  const headers = {
    "Content-Type": "application/json",
  };
  if (accessToken) {
    headers.Authorization = `Bearer ${accessToken}`;
  }

  const response = await fetch(
    `${API_BASE_URL}/revisions/${form_id}/${application_id}`,
    {
      method: "GET",
      headers: headers,
    }
  );

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(
      errorData.detail || errorData.error || "Failed to fetch revision history"
    );
  }

  const revisions = await response.json();
  return revisions;
};
