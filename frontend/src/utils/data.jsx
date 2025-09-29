// Token management utility

// Save authentication token to localStorage
export const saveToken = (tokenData) => {
  if (tokenData.access_token) {
    localStorage.setItem("access_token", tokenData.access_token);
  }
  if (tokenData.token_type) {
    localStorage.setItem("token_type", tokenData.token_type);
  }
  if (tokenData.roles) {
    localStorage.setItem("user_roles", JSON.stringify(tokenData.roles));
  }
  if (tokenData.userid) {
    localStorage.setItem("user_id", tokenData.userid);
  }
};

// Get authentication token from localStorage
export const getToken = () => {
  return localStorage.getItem("access_token");
};

// Get token type from localStorage
export const getTokenType = () => {
  return localStorage.getItem("token_type");
};

// Get user roles from localStorage
export const getUserRoles = () => {
  const roles = localStorage.getItem("user_roles");
  return roles ? JSON.parse(roles) : [];
};

// Get user ID from localStorage
export const getUserId = () => {
  return localStorage.getItem("user_id");
};

// Remove all authentication data
export const clearAuthData = () => {
  localStorage.removeItem("access_token");
  localStorage.removeItem("token_type");
  localStorage.removeItem("user_roles");
  localStorage.removeItem("user_id");
};

// Check if user is authenticated
export const isAuthenticated = () => {
  return !!getToken();
};
