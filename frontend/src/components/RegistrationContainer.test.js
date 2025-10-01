/**
 * RegistrationContainer Component Tests
 *
 * Tests for the registration form container component that handles
 * user registration for different roles.
 */

import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { MemoryRouter } from "react-router-dom";
import "@testing-library/jest-dom";
import RegistrationContainer from "./RegistrationContainer";
import { Role } from "../utils/const";

// Mock the API
const mockCreateUser = jest.fn();
jest.mock("../utils/api", () => ({
  createUser: (userData) => mockCreateUser(userData),
}));

// Mock react-router-dom
const mockNavigate = jest.fn();
jest.mock("react-router-dom", () => ({
  useNavigate: () => mockNavigate,
  MemoryRouter: ({ children }) => children,
}));

// Helper function to render with providers
const renderWithProviders = (
  component,
  queryClient = new QueryClient({
    defaultOptions: {
      queries: { retry: false },
      mutations: { retry: false },
    },
  })
) => {
  return render(
    <QueryClientProvider client={queryClient}>{component}</QueryClientProvider>
  );
};

describe("RegistrationContainer", () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe("Rendering", () => {
    it("renders registration form with all required fields", () => {
      renderWithProviders(
        <RegistrationContainer roleToRegister={Role.APPLICANT} />
      );

      expect(screen.getByLabelText(/benutzername/i)).toBeInTheDocument();
      expect(screen.getByLabelText(/e-mail/i)).toBeInTheDocument();
      expect(screen.getByLabelText(/passwort/i)).toBeInTheDocument();
      expect(screen.getByLabelText(/passwort bestätigen/i)).toBeInTheDocument();
      expect(
        screen.getByRole("button", { name: /registrieren/i })
      ).toBeInTheDocument();
    });

    it("displays correct title for different roles", () => {
      const { rerender } = renderWithProviders(
        <RegistrationContainer roleToRegister={Role.APPLICANT} />
      );
      expect(
        screen.getByText(/antragsteller registrierung/i)
      ).toBeInTheDocument();

      rerender(
        <QueryClientProvider client={new QueryClient()}>
          <MemoryRouter>
            <RegistrationContainer roleToRegister={Role.ADMIN} />
          </MemoryRouter>
        </QueryClientProvider>
      );
      expect(
        screen.getByText(/administrator registrierung/i)
      ).toBeInTheDocument();

      rerender(
        <QueryClientProvider client={new QueryClient()}>
          <MemoryRouter>
            <RegistrationContainer roleToRegister={Role.REPORTER} />
          </MemoryRouter>
        </QueryClientProvider>
      );
      expect(screen.getByText(/reporter registrierung/i)).toBeInTheDocument();
    });
  });

  describe("Form Validation", () => {
    it("shows error when required fields are empty", async () => {
      renderWithProviders(
        <RegistrationContainer roleToRegister={Role.APPLICANT} />
      );

      const submitButton = screen.getByRole("button", {
        name: /registrieren/i,
      });
      fireEvent.click(submitButton);

      // Should show validation errors or prevent submission
      expect(mockCreateUser).not.toHaveBeenCalled();
    });

    it("shows error when passwords do not match", async () => {
      renderWithProviders(
        <RegistrationContainer roleToRegister={Role.APPLICANT} />
      );

      fireEvent.change(screen.getByLabelText(/benutzername/i), {
        target: { value: "testuser" },
      });
      fireEvent.change(screen.getByLabelText(/e-mail/i), {
        target: { value: "test@example.com" },
      });
      fireEvent.change(screen.getByLabelText(/^passwort$/i), {
        target: { value: "password123" },
      });
      fireEvent.change(screen.getByLabelText(/passwort bestätigen/i), {
        target: { value: "differentpassword" },
      });

      const submitButton = screen.getByRole("button", {
        name: /registrieren/i,
      });
      fireEvent.click(submitButton);

      expect(
        screen.getByText(/passwörter stimmen nicht überein/i)
      ).toBeInTheDocument();
      expect(mockCreateUser).not.toHaveBeenCalled();
    });

    it("shows error for invalid email format", async () => {
      renderWithProviders(
        <RegistrationContainer roleToRegister={Role.APPLICANT} />
      );

      fireEvent.change(screen.getByLabelText(/benutzername/i), {
        target: { value: "testuser" },
      });
      fireEvent.change(screen.getByLabelText(/e-mail/i), {
        target: { value: "invalid-email" },
      });
      fireEvent.change(screen.getByLabelText(/^passwort$/i), {
        target: { value: "password123" },
      });
      fireEvent.change(screen.getByLabelText(/passwort bestätigen/i), {
        target: { value: "password123" },
      });

      const submitButton = screen.getByRole("button", {
        name: /registrieren/i,
      });
      fireEvent.click(submitButton);

      // Should show email validation error
      expect(screen.getByText(/gültige e-mail/i)).toBeInTheDocument();
      expect(mockCreateUser).not.toHaveBeenCalled();
    });

    it("shows error for weak password", async () => {
      renderWithProviders(
        <RegistrationContainer roleToRegister={Role.APPLICANT} />
      );

      fireEvent.change(screen.getByLabelText(/benutzername/i), {
        target: { value: "testuser" },
      });
      fireEvent.change(screen.getByLabelText(/e-mail/i), {
        target: { value: "test@example.com" },
      });
      fireEvent.change(screen.getByLabelText(/^passwort$/i), {
        target: { value: "123" },
      });
      fireEvent.change(screen.getByLabelText(/passwort bestätigen/i), {
        target: { value: "123" },
      });

      const submitButton = screen.getByRole("button", {
        name: /registrieren/i,
      });
      fireEvent.click(submitButton);

      // Should show password strength error
      expect(screen.getByText(/passwort muss mindestens/i)).toBeInTheDocument();
      expect(mockCreateUser).not.toHaveBeenCalled();
    });
  });

  describe("Form Submission", () => {
    const validFormData = {
      username: "testuser",
      email: "test@example.com",
      password: "securePassword123",
      confirmPassword: "securePassword123",
    };

    it("submits form with valid data", async () => {
      mockCreateUser.mockResolvedValue({ success: true });

      renderWithProviders(
        <RegistrationContainer roleToRegister={Role.APPLICANT} />
      );

      fireEvent.change(screen.getByLabelText(/benutzername/i), {
        target: { value: validFormData.username },
      });
      fireEvent.change(screen.getByLabelText(/e-mail/i), {
        target: { value: validFormData.email },
      });
      fireEvent.change(screen.getByLabelText(/^passwort$/i), {
        target: { value: validFormData.password },
      });
      fireEvent.change(screen.getByLabelText(/passwort bestätigen/i), {
        target: { value: validFormData.confirmPassword },
      });

      const submitButton = screen.getByRole("button", {
        name: /registrieren/i,
      });
      fireEvent.click(submitButton);

      await waitFor(() => {
        expect(mockCreateUser).toHaveBeenCalledWith({
          username: validFormData.username,
          email: validFormData.email,
          password: validFormData.password,
          role: Role.APPLICANT,
        });
      });
    });

    it("passes correct role to API", async () => {
      mockCreateUser.mockResolvedValue({ success: true });

      renderWithProviders(
        <RegistrationContainer roleToRegister={Role.ADMIN} />
      );

      fireEvent.change(screen.getByLabelText(/benutzername/i), {
        target: { value: validFormData.username },
      });
      fireEvent.change(screen.getByLabelText(/e-mail/i), {
        target: { value: validFormData.email },
      });
      fireEvent.change(screen.getByLabelText(/^passwort$/i), {
        target: { value: validFormData.password },
      });
      fireEvent.change(screen.getByLabelText(/passwort bestätigen/i), {
        target: { value: validFormData.confirmPassword },
      });

      const submitButton = screen.getByRole("button", {
        name: /registrieren/i,
      });
      fireEvent.click(submitButton);

      await waitFor(() => {
        expect(mockCreateUser).toHaveBeenCalledWith({
          username: validFormData.username,
          email: validFormData.email,
          password: validFormData.password,
          role: Role.ADMIN,
        });
      });
    });

    it("shows loading state during submission", async () => {
      mockCreateUser.mockImplementation(
        () =>
          new Promise((resolve) => {
            setTimeout(() => resolve({ success: true }), 100);
          })
      );

      renderWithProviders(
        <RegistrationContainer roleToRegister={Role.APPLICANT} />
      );

      fireEvent.change(screen.getByLabelText(/benutzername/i), {
        target: { value: validFormData.username },
      });
      fireEvent.change(screen.getByLabelText(/e-mail/i), {
        target: { value: validFormData.email },
      });
      fireEvent.change(screen.getByLabelText(/^passwort$/i), {
        target: { value: validFormData.password },
      });
      fireEvent.change(screen.getByLabelText(/passwort bestätigen/i), {
        target: { value: validFormData.confirmPassword },
      });

      const submitButton = screen.getByRole("button", {
        name: /registrieren/i,
      });
      fireEvent.click(submitButton);

      // Should show loading state
      expect(screen.getByText(/wird registriert/i)).toBeInTheDocument();
      expect(submitButton).toBeDisabled();
    });

    it("navigates on successful registration", async () => {
      mockCreateUser.mockResolvedValue({ success: true });

      renderWithProviders(
        <RegistrationContainer roleToRegister={Role.APPLICANT} />
      );

      fireEvent.change(screen.getByLabelText(/benutzername/i), {
        target: { value: validFormData.username },
      });
      fireEvent.change(screen.getByLabelText(/e-mail/i), {
        target: { value: validFormData.email },
      });
      fireEvent.change(screen.getByLabelText(/^passwort$/i), {
        target: { value: validFormData.password },
      });
      fireEvent.change(screen.getByLabelText(/passwort bestätigen/i), {
        target: { value: validFormData.confirmPassword },
      });

      const submitButton = screen.getByRole("button", {
        name: /registrieren/i,
      });
      fireEvent.click(submitButton);

      await waitFor(() => {
        expect(mockNavigate).toHaveBeenCalledWith("/login");
      });
    });

    it("displays error message on registration failure", async () => {
      const errorMessage = "Benutzername bereits vergeben";
      mockCreateUser.mockRejectedValue(new Error(errorMessage));

      renderWithProviders(
        <RegistrationContainer roleToRegister={Role.APPLICANT} />
      );

      fireEvent.change(screen.getByLabelText(/benutzername/i), {
        target: { value: validFormData.username },
      });
      fireEvent.change(screen.getByLabelText(/e-mail/i), {
        target: { value: validFormData.email },
      });
      fireEvent.change(screen.getByLabelText(/^passwort$/i), {
        target: { value: validFormData.password },
      });
      fireEvent.change(screen.getByLabelText(/passwort bestätigen/i), {
        target: { value: validFormData.confirmPassword },
      });

      const submitButton = screen.getByRole("button", {
        name: /registrieren/i,
      });
      fireEvent.click(submitButton);

      await waitFor(() => {
        expect(screen.getByText(errorMessage)).toBeInTheDocument();
      });

      // Should not navigate on error
      expect(mockNavigate).not.toHaveBeenCalled();
    });
  });

  describe("User Experience", () => {
    it("clears form on successful submission", async () => {
      mockCreateUser.mockResolvedValue({ success: true });

      renderWithProviders(
        <RegistrationContainer roleToRegister={Role.APPLICANT} />
      );

      const usernameInput = screen.getByLabelText(/benutzername/i);
      const emailInput = screen.getByLabelText(/e-mail/i);
      const passwordInput = screen.getByLabelText(/^passwort$/i);
      const confirmPasswordInput =
        screen.getByLabelText(/passwort bestätigen/i);

      fireEvent.change(usernameInput, { target: { value: "testuser" } });
      fireEvent.change(emailInput, { target: { value: "test@example.com" } });
      fireEvent.change(passwordInput, {
        target: { value: "securePassword123" },
      });
      fireEvent.change(confirmPasswordInput, {
        target: { value: "securePassword123" },
      });

      const submitButton = screen.getByRole("button", {
        name: /registrieren/i,
      });
      fireEvent.click(submitButton);

      await waitFor(() => {
        expect(usernameInput).toHaveValue("");
        expect(emailInput).toHaveValue("");
        expect(passwordInput).toHaveValue("");
        expect(confirmPasswordInput).toHaveValue("");
      });
    });

    it("focuses on first input field on mount", () => {
      renderWithProviders(
        <RegistrationContainer roleToRegister={Role.APPLICANT} />
      );

      const usernameInput = screen.getByLabelText(/benutzername/i);
      expect(usernameInput).toHaveFocus();
    });
  });
});
