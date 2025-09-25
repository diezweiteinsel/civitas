const API_BASE_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";

export const createUser = async (userData) => {
  const response = await fetch(`${API_BASE_URL}/api/v1/users`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
        "username": userData.username,
        "email": userData.email || "test@mail.com",
        "password": userData.password,
        "role": userData.role
      }),
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.error || "Failed to create user");
  }

  return response.json();
};

export const getAllUsers = async () => {
  const response = await fetch(`${API_BASE_URL}/api/v1/users`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.error || "Failed to fetch users");
  }

  return response.json();
};

export const loginUser = async (credentials) => {
  const usersResponse = await getAllUsers();
  const users = usersResponse.users;

  const user = users.find(
    (u) =>
      u.username === credentials.username && u.password === credentials.password
  );

  if (!user) {
    throw new Error("Invalid username or password");
  }

  const { password, ...userWithoutPassword } = user;
  return { user: userWithoutPassword };
};
