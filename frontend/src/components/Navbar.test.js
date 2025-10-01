/**
 * Navbar Component Tests
 *
 * Tests for the navigation bar component that provides role-based navigation
 * and dropdown menu functionality.
 */

import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import "@testing-library/jest-dom";
import Navbar from "./Navbar";
import { Role } from "../utils/const";

// Mock getUserRoles function
const mockGetUserRoles = jest.fn();
jest.mock("../utils/data", () => ({
  getUserRoles: () => mockGetUserRoles(),
}));

// Mock react-router-dom navigation
const mockNavigate = jest.fn();
jest.mock("react-router-dom", () => ({
  useNavigate: () => mockNavigate,
  MemoryRouter: ({ children }) => children,
  NavLink: ({ to, children, className, onClick, style, ...props }) => (
    <a
      href={to}
      className={className}
      onClick={onClick}
      style={style}
      {...props}
    >
      {children}
    </a>
  ),
}));

describe("Navbar", () => {
  const renderNavbar = () => {
    return render(<Navbar />);
  };

  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe("Role-based Rendering", () => {
    it("renders correctly for ADMIN role", async () => {
      mockGetUserRoles.mockReturnValue([Role.ADMIN]);
      renderNavbar();

      // Check that dropdown button is present
      const toggleButton = screen.getByRole("button");
      expect(toggleButton).toBeInTheDocument();

      // Open dropdown
      fireEvent.click(toggleButton);

      // Check admin-specific links
      const adminLinks = [
        "Startseite",
        "Öffentliche Anträge",
        "Formular erstellen",
        "Admin registrieren",
        "Reporter registrieren",
        "Abmelden",
      ];

      adminLinks.forEach((linkText) => {
        expect(screen.getByText(linkText)).toBeInTheDocument();
      });

      // Should not have applicant-specific links
      expect(screen.queryByText("Antrag einreichen")).not.toBeInTheDocument();
    });

    it("renders correctly for APPLICANT role", async () => {
      mockGetUserRoles.mockReturnValue([Role.APPLICANT]);
      renderNavbar();

      const toggleButton = screen.getByRole("button");
      fireEvent.click(toggleButton);

      const applicantLinks = [
        "Startseite",
        "Öffentliche Anträge",
        "Antrag einreichen",
        "Abmelden",
      ];

      applicantLinks.forEach((linkText) => {
        expect(screen.getByText(linkText)).toBeInTheDocument();
      });

      // Should not have admin-specific links
      expect(screen.queryByText("Admin registrieren")).not.toBeInTheDocument();
      expect(screen.queryByText("Formular erstellen")).not.toBeInTheDocument();
    });

    it("renders correctly for REPORTER role", async () => {
      mockGetUserRoles.mockReturnValue([Role.REPORTER]);
      renderNavbar();

      const toggleButton = screen.getByRole("button");
      fireEvent.click(toggleButton);

      const reporterLinks = [
        "Startseite",
        "Ausstehende Anträge",
        "Genehmigte Anträge",
        "Abgelehnte Anträge",
        "Öffentliche Anträge",
        "Abmelden",
      ];

      reporterLinks.forEach((linkText) => {
        expect(screen.getByText(linkText)).toBeInTheDocument();
      });
    });

    it("handles no role (empty array) gracefully", () => {
      mockGetUserRoles.mockReturnValue([]);
      renderNavbar();

      // Should show navbar but hide dropdown
      const dropdown = document.querySelector(".dropdown");
      expect(dropdown).toHaveClass("hidden");
    });
  });

  describe("Dropdown Functionality", () => {
    beforeEach(() => {
      mockGetUserRoles.mockReturnValue([Role.APPLICANT]);
    });

    it("toggles dropdown menu on button click", async () => {
      renderNavbar();
      const toggleButton = screen.getByRole("button");

      // Initially closed
      expect(toggleButton).toHaveAttribute("aria-expanded", "false");

      // Open dropdown
      fireEvent.click(toggleButton);
      expect(toggleButton).toHaveAttribute("aria-expanded", "true");
      expect(screen.getByText("Abmelden")).toBeInTheDocument();

      // Close dropdown
      fireEvent.click(toggleButton);
      expect(toggleButton).toHaveAttribute("aria-expanded", "false");
      expect(screen.queryByText("Abmelden")).not.toBeInTheDocument();
    });

    it("closes dropdown when clicking a link", async () => {
      renderNavbar();
      const toggleButton = screen.getByRole("button");

      // Open dropdown
      fireEvent.click(toggleButton);
      expect(screen.getByText("Startseite")).toBeInTheDocument();

      // Click a link
      fireEvent.click(screen.getByText("Startseite"));

      // Dropdown should close
      await waitFor(() => {
        expect(screen.queryByText("Startseite")).not.toBeInTheDocument();
      });
      expect(toggleButton).toHaveAttribute("aria-expanded", "false");
    });

    it("closes dropdown when clicking outside", async () => {
      renderNavbar();
      const toggleButton = screen.getByRole("button");

      // Open dropdown
      fireEvent.click(toggleButton);
      expect(screen.getByText("Abmelden")).toBeInTheDocument();

      // Click outside
      fireEvent.mouseDown(document.body);

      // Dropdown should close
      await waitFor(() => {
        expect(screen.queryByText("Abmelden")).not.toBeInTheDocument();
      });
      expect(toggleButton).toHaveAttribute("aria-expanded", "false");
    });

    it("does not close dropdown when clicking inside", async () => {
      renderNavbar();
      const toggleButton = screen.getByRole("button");

      // Open dropdown
      fireEvent.click(toggleButton);
      const logoutLink = screen.getByText("Abmelden");

      // Click inside dropdown (but not on a link)
      const dropdownContainer = logoutLink.closest(".dropdown-menu");
      if (dropdownContainer) {
        fireEvent.mouseDown(dropdownContainer);
      }

      // Dropdown should remain open
      expect(screen.getByText("Abmelden")).toBeInTheDocument();
      expect(toggleButton).toHaveAttribute("aria-expanded", "true");
    });
  });

  describe("Navigation Links", () => {
    it("has correct href attributes for admin links", async () => {
      mockGetUserRoles.mockReturnValue([Role.ADMIN]);
      renderNavbar();

      const toggleButton = screen.getByRole("button");
      fireEvent.click(toggleButton);

      const linkMappings = [
        { text: "Startseite", href: "/admin" },
        { text: "Öffentliche Anträge", href: "/admin/public?from=admin" },
        { text: "Formular erstellen", href: "/admin/create-forms" },
        { text: "Admin registrieren", href: "/admin/admin-registration" },
        { text: "Reporter registrieren", href: "/admin/reporter-registration" },
        { text: "Abmelden", href: "/" },
      ];

      linkMappings.forEach(({ text, href }) => {
        const link = screen.getByText(text);
        expect(link).toHaveAttribute("href", href);
      });
    });

    it("has correct href attributes for applicant links", async () => {
      mockGetUserRoles.mockReturnValue([Role.APPLICANT]);
      renderNavbar();

      const toggleButton = screen.getByRole("button");
      fireEvent.click(toggleButton);

      const linkMappings = [
        { text: "Startseite", href: "/applicant" },
        {
          text: "Öffentliche Anträge",
          href: "/applicant/public?from=applicant",
        },
        { text: "Antrag einreichen", href: "/applicant/submit" },
        { text: "Abmelden", href: "/" },
      ];

      linkMappings.forEach(({ text, href }) => {
        const link = screen.getByText(text);
        expect(link).toHaveAttribute("href", href);
      });
    });

    it("has correct href attributes for reporter links", async () => {
      mockGetUserRoles.mockReturnValue([Role.REPORTER]);
      renderNavbar();

      const toggleButton = screen.getByRole("button");
      fireEvent.click(toggleButton);

      const linkMappings = [
        { text: "Startseite", href: "/reporter" },
        { text: "Ausstehende Anträge", href: "/reporter/pending" },
        { text: "Genehmigte Anträge", href: "/reporter/approved" },
        { text: "Abgelehnte Anträge", href: "/reporter/rejected" },
        { text: "Öffentliche Anträge", href: "/reporter/public" },
        { text: "Abmelden", href: "/" },
      ];

      linkMappings.forEach(({ text, href }) => {
        const link = screen.getByText(text);
        expect(link).toHaveAttribute("href", href);
      });
    });
  });

  describe("Accessibility", () => {
    beforeEach(() => {
      mockGetUserRoles.mockReturnValue([Role.APPLICANT]);
    });

    it("has proper ARIA attributes", () => {
      renderNavbar();

      const navbar = screen.getByRole("navigation");
      expect(navbar).toBeInTheDocument();

      const toggleButton = screen.getByRole("button");
      expect(toggleButton).toHaveAttribute("aria-expanded", "false");
      expect(toggleButton).toHaveAttribute("aria-haspopup", "true");
    });

    it("updates aria-expanded when dropdown state changes", async () => {
      mockGetUserRoles.mockReturnValue([Role.APPLICANT]);
      renderNavbar();
      const toggleButton = screen.getByRole("button");

      // Initially false
      expect(toggleButton).toHaveAttribute("aria-expanded", "false");

      // After opening
      fireEvent.click(toggleButton);
      expect(toggleButton).toHaveAttribute("aria-expanded", "true");

      // After closing
      fireEvent.click(toggleButton);
      expect(toggleButton).toHaveAttribute("aria-expanded", "false");
    });
  });

  describe("Edge Cases", () => {
    it("handles getUserRoles returning null", () => {
      mockGetUserRoles.mockReturnValue(null);
      renderNavbar();

      // Should show navbar but hide dropdown
      const dropdown = document.querySelector(".dropdown");
      expect(dropdown).toHaveClass("hidden");
    });

    it("handles getUserRoles returning undefined", () => {
      mockGetUserRoles.mockReturnValue(undefined);
      renderNavbar();

      // Should show navbar but hide dropdown
      const dropdown = document.querySelector(".dropdown");
      expect(dropdown).toHaveClass("hidden");
    });

    it("handles multiple roles by using the first one", async () => {
      mockGetUserRoles.mockReturnValue([Role.ADMIN, Role.REPORTER]);
      renderNavbar();

      const toggleButton = screen.getByRole("button");
      fireEvent.click(toggleButton);

      // Should show admin links (first role)
      expect(screen.getByText("Formular erstellen")).toBeInTheDocument();
    });
  });
});
