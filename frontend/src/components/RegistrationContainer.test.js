import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import RegistrationContainer from "./RegistrationContainer";
import { Role } from "../utils/const";
import * as api from "../utils/api";

// Mock the API module
jest.mock("../utils/api");
const mockedApi = api;

// Mock window.alert
global.alert = jest.fn();

// Mock the navigate function
const mockNavigate = jest.fn();
jest.mock("react-router-dom", () => ({
  useNavigate: () => mockNavigate,
  NavLink: ({ children, to }) => <a href={to}>{children}</a>,
  MemoryRouter: ({ children }) => <div>{children}</div>,
}));

// Import after mocking
const { MemoryRouter } = require("react-router-dom");

// Helper function to render component with providers
const renderWithProviders = (component) => {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: {
        retry: false,
      },
      mutations: {
        retry: false,
      },
    },
  });

  return render(
    <QueryClientProvider client={queryClient}>
      <MemoryRouter>{component}</MemoryRouter>
    </QueryClientProvider>
  );
};

describe("RegistrationContainer", () => {
  beforeEach(() => {
    jest.clearAllMocks();
    mockNavigate.mockClear();
  });

  describe("Rendering", () => {
    it("renders registration form with all fields", () => {
      renderWithProviders(<RegistrationContainer />);

      expect(
        screen.getByText("Bürger/-innen Registrieren")
      ).toBeInTheDocument();
      expect(
        screen.getByPlaceholderText("Benutzername eingeben")
      ).toBeInTheDocument();
      expect(screen.getByPlaceholderText("Email eingeben")).toBeInTheDocument();
      expect(
        screen.getByPlaceholderText("Passwort eingeben")
      ).toBeInTheDocument();
      expect(
        screen.getByPlaceholderText("Passwort bestätigen")
      ).toBeInTheDocument();
      expect(
        screen.getByRole("button", { name: "Registrieren" })
      ).toBeInTheDocument();
    });

    it("renders different title based on role", () => {
      renderWithProviders(
        <RegistrationContainer roleToRegister={Role.ADMIN} />
      );
      expect(screen.getByText("Admin Registrieren")).toBeInTheDocument();

      renderWithProviders(
        <RegistrationContainer roleToRegister={Role.REPORTER} />
      );
      expect(screen.getByText("Reporter Registrieren")).toBeInTheDocument();

      renderWithProviders(
        <RegistrationContainer roleToRegister={Role.APPLICANT} />
      );
      expect(
        screen.getByText("Bürger/-innen Registrieren")
      ).toBeInTheDocument();
    });

    it("shows login link only for applicant role", () => {
      const { unmount } = renderWithProviders(
        <RegistrationContainer roleToRegister={Role.APPLICANT} />
      );
      expect(
        screen.getByText("Sie haben bereits einen Account?")
      ).toBeInTheDocument();
      expect(screen.getByText("Anmelden")).toBeInTheDocument();

      // Unmount and render admin version
      unmount();
      renderWithProviders(
        <RegistrationContainer roleToRegister={Role.ADMIN} />
      );
      expect(
        screen.queryByText("Sie haben bereits einen Account?")
      ).not.toBeInTheDocument();
    });
  });

  describe("Form Validation", () => {
    it("shows error when required fields are empty", async () => {
      renderWithProviders(<RegistrationContainer />);

      fireEvent.click(screen.getByRole("button", { name: "Registrieren" }));

      await waitFor(() => {
        expect(screen.getByText("All fields are required")).toBeInTheDocument();
      });
    });

    it("shows error when passwords do not match", async () => {
      renderWithProviders(<RegistrationContainer />);

      fireEvent.change(screen.getByPlaceholderText("Benutzername eingeben"), {
        target: { value: "testuser" },
      });
      fireEvent.change(screen.getByPlaceholderText("Email eingeben"), {
        target: { value: "test@example.com" },
      });
      fireEvent.change(screen.getByPlaceholderText("Passwort eingeben"), {
        target: { value: "password123" },
      });
      fireEvent.change(screen.getByPlaceholderText("Passwort bestätigen"), {
        target: { value: "password456" },
      });

      fireEvent.click(screen.getByRole("button", { name: "Registrieren" }));

      await waitFor(() => {
        expect(screen.getByText("Passwords do not match")).toBeInTheDocument();
      });
    });

    it("validates required username field only", async () => {
      renderWithProviders(<RegistrationContainer />);

      fireEvent.change(screen.getByPlaceholderText("Email eingeben"), {
        target: { value: "test@example.com" },
      });
      fireEvent.change(screen.getByPlaceholderText("Passwort eingeben"), {
        target: { value: "password123" },
      });
      fireEvent.change(screen.getByPlaceholderText("Passwort bestätigen"), {
        target: { value: "password123" },
      });

      fireEvent.click(screen.getByRole("button", { name: "Registrieren" }));

      await waitFor(() => {
        expect(screen.getByText("All fields are required")).toBeInTheDocument();
      });
    });
  });

  describe("Form Submission", () => {
    it("submits form with correct data on successful registration", async () => {
      const mockUserData = {
        id: 1,
        username: "testuser",
        email: "test@example.com",
        role: Role.APPLICANT,
      };

      mockedApi.createUser.mockResolvedValue(mockUserData);

      renderWithProviders(
        <RegistrationContainer roleToRegister={Role.APPLICANT} />
      );

      fireEvent.change(screen.getByPlaceholderText("Benutzername eingeben"), {
        target: { value: "testuser" },
      });
      fireEvent.change(screen.getByPlaceholderText("Email eingeben"), {
        target: { value: "test@example.com" },
      });
      fireEvent.change(screen.getByPlaceholderText("Passwort eingeben"), {
        target: { value: "password123" },
      });
      fireEvent.change(screen.getByPlaceholderText("Passwort bestätigen"), {
        target: { value: "password123" },
      });

      fireEvent.click(screen.getByRole("button", { name: "Registrieren" }));

      await waitFor(() => {
        expect(mockedApi.createUser).toHaveBeenCalledWith(
          {
            username: "testuser",
            email: "test@example.com",
            password: "password123",
            role: Role.APPLICANT,
          },
          expect.anything()
        );
      });

      await waitFor(() => {
        expect(
          screen.getByText("Registration successful!")
        ).toBeInTheDocument();
      });
    });

    it("shows loading state during form submission", async () => {
      mockedApi.createUser.mockImplementation(
        () => new Promise((resolve) => setTimeout(() => resolve({}), 100))
      );

      renderWithProviders(<RegistrationContainer />);

      fireEvent.change(screen.getByPlaceholderText("Benutzername eingeben"), {
        target: { value: "testuser" },
      });
      fireEvent.change(screen.getByPlaceholderText("Email eingeben"), {
        target: { value: "test@example.com" },
      });
      fireEvent.change(screen.getByPlaceholderText("Passwort eingeben"), {
        target: { value: "password123" },
      });
      fireEvent.change(screen.getByPlaceholderText("Passwort bestätigen"), {
        target: { value: "password123" },
      });

      fireEvent.click(screen.getByRole("button", { name: "Registrieren" }));

      await waitFor(() => {
        expect(screen.getByText("Account erstellen...")).toBeInTheDocument();
      });
      expect(
        screen.getByRole("button", { name: "Account erstellen..." })
      ).toBeDisabled();
    });

    it("handles registration error", async () => {
      const errorMessage = "Username already exists";
      mockedApi.createUser.mockRejectedValue(new Error(errorMessage));

      renderWithProviders(<RegistrationContainer />);

      fireEvent.change(screen.getByPlaceholderText("Benutzername eingeben"), {
        target: { value: "testuser" },
      });
      fireEvent.change(screen.getByPlaceholderText("Email eingeben"), {
        target: { value: "test@example.com" },
      });
      fireEvent.change(screen.getByPlaceholderText("Passwort eingeben"), {
        target: { value: "password123" },
      });
      fireEvent.change(screen.getByPlaceholderText("Passwort bestätigen"), {
        target: { value: "password123" },
      });

      fireEvent.click(screen.getByRole("button", { name: "Registrieren" }));

      await waitFor(() => {
        expect(screen.getByText(errorMessage)).toBeInTheDocument();
      });
    });

    it("handles registration error without message", async () => {
      mockedApi.createUser.mockRejectedValue(new Error());

      renderWithProviders(<RegistrationContainer />);

      fireEvent.change(screen.getByPlaceholderText("Benutzername eingeben"), {
        target: { value: "testuser" },
      });
      fireEvent.change(screen.getByPlaceholderText("Email eingeben"), {
        target: { value: "test@example.com" },
      });
      fireEvent.change(screen.getByPlaceholderText("Passwort eingeben"), {
        target: { value: "password123" },
      });
      fireEvent.change(screen.getByPlaceholderText("Passwort bestätigen"), {
        target: { value: "password123" },
      });

      fireEvent.click(screen.getByRole("button", { name: "Registrieren" }));

      await waitFor(() => {
        expect(
          screen.getByText("Registration failed. Please try again.")
        ).toBeInTheDocument();
      });
    });
  });

  describe("Navigation", () => {
    it("navigates to home after successful applicant registration", async () => {
      const mockUserData = {
        id: 1,
        username: "testuser",
        email: "test@example.com",
        role: Role.APPLICANT,
      };

      mockedApi.createUser.mockResolvedValue(mockUserData);

      renderWithProviders(
        <RegistrationContainer roleToRegister={Role.APPLICANT} />
      );

      fireEvent.change(screen.getByPlaceholderText("Benutzername eingeben"), {
        target: { value: "testuser" },
      });
      fireEvent.change(screen.getByPlaceholderText("Email eingeben"), {
        target: { value: "test@example.com" },
      });
      fireEvent.change(screen.getByPlaceholderText("Passwort eingeben"), {
        target: { value: "password123" },
      });
      fireEvent.change(screen.getByPlaceholderText("Passwort bestätigen"), {
        target: { value: "password123" },
      });

      fireEvent.click(screen.getByRole("button", { name: "Registrieren" }));

      await waitFor(() => {
        expect(
          screen.getByText("Registration successful!")
        ).toBeInTheDocument();
      });

      // Wait for navigation timeout
      await waitFor(
        () => {
          expect(mockNavigate).toHaveBeenCalledWith("/");
        },
        { timeout: 2000 }
      );
    });

    it("does not navigate after successful admin/reporter registration", async () => {
      const mockUserData = {
        id: 1,
        username: "reporter",
        email: "reporter@example.com",
        role: Role.REPORTER,
      };

      mockedApi.createUser.mockResolvedValue(mockUserData);

      renderWithProviders(
        <RegistrationContainer roleToRegister={Role.REPORTER} />
      );

      // Clear the mock after rendering to avoid counting any initial calls
      mockNavigate.mockClear();

      fireEvent.change(screen.getByPlaceholderText("Benutzername eingeben"), {
        target: { value: "reporter" },
      });
      fireEvent.change(screen.getByPlaceholderText("Email eingeben"), {
        target: { value: "reporter@example.com" },
      });
      fireEvent.change(screen.getByPlaceholderText("Passwort eingeben"), {
        target: { value: "password123" },
      });
      fireEvent.change(screen.getByPlaceholderText("Passwort bestätigen"), {
        target: { value: "password123" },
      });

      fireEvent.click(screen.getByRole("button", { name: "Registrieren" }));

      await waitFor(() => {
        expect(
          screen.getByText("Registration successful!")
        ).toBeInTheDocument();
      });

      // Wait a bit to ensure navigation doesn't happen
      await new Promise((resolve) => setTimeout(resolve, 1000));
      expect(mockNavigate).not.toHaveBeenCalled();
    });
  });

  describe("Form Reset", () => {
    it("resets form fields after successful registration", async () => {
      const mockUserData = {
        id: 1,
        username: "testuser",
        email: "test@example.com",
        role: Role.APPLICANT,
      };

      mockedApi.createUser.mockResolvedValue(mockUserData);

      renderWithProviders(<RegistrationContainer />);

      const usernameInput = screen.getByPlaceholderText(
        "Benutzername eingeben"
      );
      const emailInput = screen.getByPlaceholderText("Email eingeben");
      const passwordInput = screen.getByPlaceholderText("Passwort eingeben");
      const confirmInput = screen.getByPlaceholderText("Passwort bestätigen");

      fireEvent.change(usernameInput, { target: { value: "testuser" } });
      fireEvent.change(emailInput, { target: { value: "test@example.com" } });
      fireEvent.change(passwordInput, { target: { value: "password123" } });
      fireEvent.change(confirmInput, { target: { value: "password123" } });

      fireEvent.click(screen.getByRole("button", { name: "Registrieren" }));

      await waitFor(() => {
        expect(
          screen.getByText("Registration successful!")
        ).toBeInTheDocument();
      });

      // Check that form fields are reset
      expect(usernameInput.value).toBe("");
      expect(emailInput.value).toBe("");
      expect(passwordInput.value).toBe("");
      expect(confirmInput.value).toBe("");
    });
  });

  describe("Success Message", () => {
    it("shows success message and hides it after timeout", async () => {
      const mockUserData = {
        id: 1,
        username: "testuser",
        email: "test@example.com",
        role: Role.APPLICANT,
      };

      mockedApi.createUser.mockResolvedValue(mockUserData);

      renderWithProviders(<RegistrationContainer />);

      fireEvent.change(screen.getByPlaceholderText("Benutzername eingeben"), {
        target: { value: "testuser" },
      });
      fireEvent.change(screen.getByPlaceholderText("Email eingeben"), {
        target: { value: "test@example.com" },
      });
      fireEvent.change(screen.getByPlaceholderText("Passwort eingeben"), {
        target: { value: "password123" },
      });
      fireEvent.change(screen.getByPlaceholderText("Passwort bestätigen"), {
        target: { value: "password123" },
      });

      fireEvent.click(screen.getByRole("button", { name: "Registrieren" }));

      await waitFor(() => {
        expect(
          screen.getByText("Registration successful!")
        ).toBeInTheDocument();
      });

      // Wait for success message to disappear
      await waitFor(
        () => {
          expect(
            screen.queryByText("Registration successful!")
          ).not.toBeInTheDocument();
        },
        { timeout: 4000 }
      );
    });
  });

  describe("Input Validation", () => {
    it("accepts valid email format", async () => {
      renderWithProviders(<RegistrationContainer />);

      const emailInput = screen.getByPlaceholderText("Email eingeben");
      fireEvent.change(emailInput, { target: { value: "valid@email.com" } });

      expect(emailInput.value).toBe("valid@email.com");
    });

    it("updates form fields correctly", () => {
      renderWithProviders(<RegistrationContainer />);

      const usernameInput = screen.getByPlaceholderText(
        "Benutzername eingeben"
      );
      const emailInput = screen.getByPlaceholderText("Email eingeben");
      const passwordInput = screen.getByPlaceholderText("Passwort eingeben");
      const confirmInput = screen.getByPlaceholderText("Passwort bestätigen");

      fireEvent.change(usernameInput, { target: { value: "newuser" } });
      fireEvent.change(emailInput, { target: { value: "new@email.com" } });
      fireEvent.change(passwordInput, { target: { value: "newpassword" } });
      fireEvent.change(confirmInput, { target: { value: "newpassword" } });

      expect(usernameInput.value).toBe("newuser");
      expect(emailInput.value).toBe("new@email.com");
      expect(passwordInput.value).toBe("newpassword");
      expect(confirmInput.value).toBe("newpassword");
    });
  });
});
