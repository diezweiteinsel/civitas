// frontend/src/pages/LoginPage.test.jsx

import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import "@testing-library/jest-dom";
import React from "react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

// Provide a light manual mock for `react-router-dom` so Jest does not try to
// resolve the real (ESM) package. We expose a minimal `MemoryRouter`, a
// `useNavigate` hook (we'll set the function in tests), and a simple
// `NavLink` implementation.
// Use the manual mock in src/__mocks__/react-router-dom.js and set the
// navigate implementation before importing the component under test.
const rrdomMock = require("react-router-dom");
let mockNavigate = jest.fn();
rrdomMock.__setMockNavigate(mockNavigate);

const { MemoryRouter } = rrdomMock;
import LoginPage from "./Login";

// --- Mocking Dependencies ---
// We mock the modules that contain external dependencies.
const mockLoginUser = jest.fn();
jest.mock("../utils/api", () => ({
  loginUser: (args) => mockLoginUser(args),
  getAllUsers: jest.fn(), // Mock this too, though we won't use it
}));

const mockSaveToken = jest.fn();
const mockGetUserRoles = jest.fn();
jest.mock("../utils/data", () => ({
  saveToken: (args) => mockSaveToken(args),
  getUserRoles: () => mockGetUserRoles(),
}));

// --- Custom Render Function ---
// This helper wraps our component in the providers it needs to run.
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: false, // Disable retries for tests
    },
  },
});

const renderWithProviders = (ui) => {
  return render(
    <QueryClientProvider client={queryClient}>
      <MemoryRouter>{ui}</MemoryRouter>
    </QueryClientProvider>
  );
};

// (Continue in LoginPage.test.jsx)

describe("LoginPage", () => {
  // Clear all mocks before each test to ensure a clean slate.
  beforeEach(() => {
    jest.clearAllMocks();
    mockNavigate = jest.fn();
    // Reset the manual mock's navigate function for each test
    rrdomMock.__setMockNavigate(mockNavigate);
    // Mock getUserRoles to return empty array (no user logged in)
    mockGetUserRoles.mockReturnValue([]);
  });

  // Test 1: Does the component render correctly?
  it("should render the login form with all fields", () => {
    renderWithProviders(<LoginPage />);

    // Check for the title
    expect(
      screen.getByRole("heading", { name: /anmeldung/i })
    ).toBeInTheDocument();

    // Check for input fields using their accessible labels
    expect(screen.getByLabelText(/benutzername/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/passwort/i)).toBeInTheDocument();

    // Check for the submit button
    expect(
      screen.getByRole("button", { name: /anmelden/i })
    ).toBeInTheDocument();
  });

  // Test 2: Does it show a validation error if the form is submitted empty?
  it("should show an error message when submitting with empty fields", async () => {
    renderWithProviders(<LoginPage />);

    const submitButton = screen.getByRole("button", { name: /anmelden/i });
    fireEvent.click(submitButton);

    // Find the error message
    expect(
      await screen.findByText("Beide Felder sind erforderlich")
    ).toBeInTheDocument();

    // Ensure no API call was made
    expect(mockLoginUser).not.toHaveBeenCalled();
  });

  // Test 3: Does it handle a successful login?
  it("should call loginUser, save token, and navigate on successful submission", async () => {
    // Arrange: Mock a successful API response
    const mockSuccessResponse = { token: "fake-jwt-token", roles: ["ADMIN"] };
    mockLoginUser.mockResolvedValue(mockSuccessResponse);

    renderWithProviders(<LoginPage />);

    // Act: Fill out the form and submit
    fireEvent.change(screen.getByLabelText(/benutzername/i), {
      target: { value: "testadmin" },
    });
    fireEvent.change(screen.getByLabelText(/passwort/i), {
      target: { value: "password123" },
    });
    fireEvent.click(screen.getByRole("button", { name: /anmelden/i }));

    // Assert: Check that the correct functions were called with the correct data
    await waitFor(() => {
      // 1. API was called correctly
      expect(mockLoginUser).toHaveBeenCalledWith({
        username: "testadmin",
        password: "password123",
      });

      // 2. Token was saved
      expect(mockSaveToken).toHaveBeenCalledWith(mockSuccessResponse);

      // 3. User was redirected
      expect(mockNavigate).toHaveBeenCalledWith("/admin");
    });
  });

  // Test 4: Does it handle a failed login?
  it("should display an error message on a failed API call", async () => {
    // Arrange: Mock a failed API response
    const errorMessage = "Invalid credentials";
    mockLoginUser.mockRejectedValue(new Error(errorMessage));

    renderWithProviders(<LoginPage />);

    // Act: Fill out the form and submit
    fireEvent.change(screen.getByLabelText(/benutzername/i), {
      target: { value: "wronguser" },
    });
    fireEvent.change(screen.getByLabelText(/passwort/i), {
      target: { value: "wrongpass" },
    });
    fireEvent.click(screen.getByRole("button", { name: /anmelden/i }));

    // Assert: Check that the error message from the API is shown
    expect(await screen.findByText(errorMessage)).toBeInTheDocument();

    // Ensure navigation did not happen
    expect(mockNavigate).not.toHaveBeenCalled();
  });
});
