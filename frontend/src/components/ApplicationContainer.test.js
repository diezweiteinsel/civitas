/**
 * ApplicationContainer Component Tests
 *
 * Tests for the ApplicationContainer component that displays lists of applications
 * with various filtering and fetching capabilities.
 */

import { render, screen, fireEvent } from "@testing-library/react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { MemoryRouter } from "react-router-dom";
import "@testing-library/jest-dom";
import ApplicationContainer from "./ApplicationContainer";

// Mock react-router-dom
const mockNavigate = jest.fn();
const mockUseLocation = jest.fn();

jest.mock("react-router-dom", () => ({
  ...jest.requireActual("react-router-dom"),
  useNavigate: () => mockNavigate,
  useLocation: () => mockUseLocation(),
}));

// Mock the API functions that the component uses
const mockGetAllApplications = jest.fn();
const mockGetApplicationsByStatus = jest.fn();
const mockGetPublicApplications = jest.fn();
const mockGetPublicApplicationsByStatus = jest.fn();

jest.mock("../utils/api", () => ({
  getAllApplications: () => mockGetAllApplications(),
  getApplicationsByStatus: (status) => mockGetApplicationsByStatus(status),
  getPublicApplications: () => mockGetPublicApplications(),
  getPublicApplicationsByStatus: (status) =>
    mockGetPublicApplicationsByStatus(status),
}));

// Mock react-icons
jest.mock("react-icons/bi", () => ({
  BiWorld: () => <div data-testid="icon-world" />,
}));

jest.mock("react-icons/fa", () => ({
  FaEye: () => <div data-testid="icon-eye" />,
}));

// Test data
const mockApplications = [
  {
    id: 1,
    applicationID: 1,
    formID: 1,
    status: "PENDING",
    title: "Test Application 1",
    created_at: "2025-01-01T10:00:00Z",
    is_public: false,
  },
  {
    id: 2,
    applicationID: 2,
    formID: 2,
    status: "APPROVED",
    title: "Test Application 2",
    created_at: "2025-01-02T11:00:00Z",
    is_public: true,
  },
  {
    id: 3,
    applicationID: 3,
    formID: 3,
    status: "REJECTED",
    title: "Test Application 3",
    created_at: "2025-01-03T12:00:00Z",
    is_public: false,
  },
];

// Helper function to render with QueryClient
const renderWithQueryClient = (
  component,
  queryClient = new QueryClient({
    defaultOptions: {
      queries: { retry: false },
      mutations: { retry: false },
    },
  })
) => {
  return render(
    <QueryClientProvider client={queryClient}>
      <MemoryRouter>{component}</MemoryRouter>
    </QueryClientProvider>
  );
};

describe("ApplicationContainer", () => {
  beforeEach(() => {
    jest.clearAllMocks();
    mockUseLocation.mockReturnValue({ pathname: "/default" });
  });

  describe("Rendering and Basic Functionality", () => {
    it("renders the custom title correctly", () => {
      renderWithQueryClient(
        <ApplicationContainer
          title="Custom Test Title"
          applications={[]}
          enableFetch={false}
        />
      );

      expect(screen.getByText("Custom Test Title")).toBeInTheDocument();
    });

    it("displays loading state when isLoadingOverride is true", () => {
      renderWithQueryClient(
        <ApplicationContainer
          applications={[]}
          enableFetch={false}
          isLoadingOverride={true}
        />
      );

      expect(screen.getByText("Loading applications...")).toBeInTheDocument();
    });

    it("displays error state when errorOverride is provided", () => {
      const mockError = new Error("Failed to fetch applications");

      renderWithQueryClient(
        <ApplicationContainer
          applications={[]}
          enableFetch={false}
          errorOverride={mockError}
        />
      );

      expect(
        screen.getByText(/Error loading applications/)
      ).toBeInTheDocument();
      expect(
        screen.getByText("Failed to fetch applications")
      ).toBeInTheDocument();
    });

    it('displays "No applications found" when no applications are provided', () => {
      renderWithQueryClient(
        <ApplicationContainer applications={[]} enableFetch={false} />
      );

      expect(screen.getByText("No applications found.")).toBeInTheDocument();
    });
  });

  describe("Application Display", () => {
    it("displays provided applications correctly", () => {
      renderWithQueryClient(
        <ApplicationContainer
          applications={mockApplications}
          enableFetch={false}
        />
      );

      expect(screen.getByText("Test Application 1")).toBeInTheDocument();
      expect(screen.getByText("Test Application 2")).toBeInTheDocument();
      expect(screen.getByText("Test Application 3")).toBeInTheDocument();
    });

    it("translates status labels correctly", () => {
      renderWithQueryClient(
        <ApplicationContainer
          applications={mockApplications}
          enableFetch={false}
        />
      );

      expect(screen.getByText("Ausstehend")).toBeInTheDocument(); // PENDING
      expect(screen.getByText("Genehmigt")).toBeInTheDocument(); // APPROVED
      expect(screen.getByText("Abgelehnt")).toBeInTheDocument(); // REJECTED
    });

    it("displays public indicator icons for public applications", () => {
      renderWithQueryClient(
        <ApplicationContainer
          applications={mockApplications}
          enableFetch={false}
        />
      );

      const worldIcons = screen.getAllByTestId("icon-world");
      const eyeIcons = screen.getAllByTestId("icon-eye");

      // Only one application is public
      expect(worldIcons).toHaveLength(1);
      expect(eyeIcons).toHaveLength(1);
    });

    it("formats creation dates correctly", () => {
      renderWithQueryClient(
        <ApplicationContainer
          applications={mockApplications}
          enableFetch={false}
        />
      );

      // Check that dates are displayed (exact format may vary by locale)
      expect(screen.getByText(/Erstellt:/)).toBeInTheDocument();
    });
  });

  describe("Navigation", () => {
    it('calls navigate with correct parameters when "Zeige Details" is clicked', () => {
      renderWithQueryClient(
        <ApplicationContainer
          applications={mockApplications}
          enableFetch={false}
        />
      );

      const detailButtons = screen.getAllByText("Zeige Details");
      fireEvent.click(detailButtons[0]);

      expect(mockNavigate).toHaveBeenCalledWith(
        "/applications/1/1",
        expect.objectContaining({
          state: expect.objectContaining({
            fromPage: "unknown",
            from: "/default",
          }),
        })
      );
    });

    it("determines correct fromPage context based on pathname", () => {
      mockUseLocation.mockReturnValue({ pathname: "/admin/dashboard" });

      renderWithQueryClient(
        <ApplicationContainer
          applications={mockApplications}
          enableFetch={false}
        />
      );

      const detailButtons = screen.getAllByText("Zeige Details");
      fireEvent.click(detailButtons[0]);

      expect(mockNavigate).toHaveBeenCalledWith(
        "/applications/1/1",
        expect.objectContaining({
          state: expect.objectContaining({
            fromPage: "admin-dashboard",
          }),
        })
      );
    });
  });

  describe("Props Handling", () => {
    it("uses provided applications when enableFetch is false", () => {
      const providedApps = [mockApplications[0]];

      renderWithQueryClient(
        <ApplicationContainer applications={providedApps} enableFetch={false} />
      );

      expect(screen.getByText("Test Application 1")).toBeInTheDocument();
      expect(screen.queryByText("Test Application 2")).not.toBeInTheDocument();
    });

    it("handles isLoadingOverride when enableFetch is false", () => {
      renderWithQueryClient(
        <ApplicationContainer
          applications={[]}
          enableFetch={false}
          isLoadingOverride={true}
        />
      );

      expect(screen.getByText("Loading applications...")).toBeInTheDocument();
    });

    it("handles errorOverride when enableFetch is false", () => {
      const mockError = new Error("Override error");

      renderWithQueryClient(
        <ApplicationContainer
          applications={[]}
          enableFetch={false}
          errorOverride={mockError}
        />
      );

      expect(
        screen.getByText(/Error loading applications/)
      ).toBeInTheDocument();
      expect(screen.getByText("Override error")).toBeInTheDocument();
    });
  });

  describe("Error Handling", () => {
    it("handles missing application identifiers gracefully", () => {
      const appsWithMissingIds = [
        {
          status: "PENDING",
          title: "Test Application",
          created_at: "2025-01-01T10:00:00Z",
          // Missing id and formId
        },
      ];

      renderWithQueryClient(
        <ApplicationContainer
          applications={appsWithMissingIds}
          enableFetch={false}
        />
      );

      const detailButtons = screen.getAllByText("Zeige Details");
      fireEvent.click(detailButtons[0]);

      // Should not navigate if ids are missing
      expect(mockNavigate).not.toHaveBeenCalled();
    });
  });
});
