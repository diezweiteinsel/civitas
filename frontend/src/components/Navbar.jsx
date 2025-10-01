import "./../style/Navbar.css";
import logo from "./../img/civitas.png";
import { GiHamburgerMenu } from "react-icons/gi";
import { NavLink, useNavigate } from "react-router-dom";
import { useRef, useState, useEffect } from "react";
import { Role } from "../utils/const";
import { getUserRoles } from "../utils/data";

function Logo() {
  return <img src={logo} alt="Logo" className="navbar-img" />;
}

export default function Navbar() {
  const navigate = useNavigate();
  const [showDropdown, setShowDropdown] = useState(false);
  const dropdownRef = useRef(null);

  // Get role dynamically on every render
  const roles = getUserRoles();
  const role = roles && roles.length > 0 ? roles[0] : Role.EMPTY;

  // Helper function to get home route based on role
  const getHomeRoute = () => {
    switch (role) {
      case Role.ADMIN:
        return "/admin";
      case Role.REPORTER:
        return "/reporter";
      default:
        return "/applicant";
    }
  };

  // Close dropdown when clicking outside
  useEffect(() => {
    function handleClickOutside(event) {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setShowDropdown(false);
      }
    }
    if (showDropdown) {
      document.addEventListener("mousedown", handleClickOutside);
    }
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [showDropdown]);

  const handleLogout = () => {
    setShowDropdown(false);
    // Clear user data from localStorage
    localStorage.clear();
  };

  return (
    <nav className="navbar">
      <NavLink to={getHomeRoute()} className="navbar-logo">
        <Logo />
      </NavLink>

      <NavLink to={getHomeRoute()} className="navbar-home">
        <div className="navbar-brand">CIVITAS</div>
      </NavLink>

      <div
        ref={dropdownRef}
        className={`dropdown ${role === Role.EMPTY ? "hidden" : ""}`}
      >
        <button
          className="dropdown-toggle"
          onClick={() => setShowDropdown((prev) => !prev)}
          aria-expanded={showDropdown}
          aria-haspopup="true"
        >
          <GiHamburgerMenu className="burger-icon" />
        </button>
        {showDropdown && (
          <div className="dropdown-menu">
            {role === Role.ADMIN && (
              <>
                <div className="dropdown-item">
                  <NavLink
                    className="nav-link"
                    to="/admin"
                    onClick={() => setShowDropdown(false)}
                  >
                    Startseite
                  </NavLink>
                </div>
                <div className="dropdown-item">
                  <NavLink
                    className="nav-link"
                    to="/admin/public?from=admin"
                    onClick={() => setShowDropdown(false)}
                  >
                    Öffentliche Anträge
                  </NavLink>
                </div>
                <div className="dropdown-item">
                  <NavLink
                    className="nav-link"
                    to="/admin/create-forms"
                    onClick={() => setShowDropdown(false)}
                  >
                    Formular erstellen
                  </NavLink>
                </div>
                <div className="dropdown-item">
                  <NavLink
                    className="nav-link"
                    to="/admin/admin-registration"
                    onClick={() => setShowDropdown(false)}
                  >
                    Admin registrieren
                  </NavLink>
                </div>
                <div className="dropdown-item">
                  <NavLink
                    className="nav-link"
                    to="/admin/reporter-registration"
                    onClick={() => setShowDropdown(false)}
                  >
                    Reporter registrieren
                  </NavLink>
                </div>
              </>
            )}

            {role === Role.APPLICANT && (
              <>
                <div className="dropdown-item">
                  <NavLink
                    className="nav-link"
                    to="/applicant"
                    onClick={() => setShowDropdown(false)}
                  >
                    Startseite
                  </NavLink>
                </div>
                <div className="dropdown-item">
                  <NavLink
                    className="nav-link"
                    to="/applicant/public?from=applicant"
                    onClick={() => setShowDropdown(false)}
                  >
                    Öffentliche Anträge
                  </NavLink>
                </div>
                <div className="dropdown-item">
                  <NavLink
                    className="nav-link"
                    to="/applicant/submit"
                    onClick={() => setShowDropdown(false)}
                  >
                    Antrag einreichen
                  </NavLink>
                </div>
              </>
            )}

            {role === Role.REPORTER && (
              <>
                <div className="dropdown-item">
                  <NavLink
                    className="nav-link"
                    to="/reporter"
                    onClick={() => setShowDropdown(false)}
                  >
                    Startseite
                  </NavLink>
                </div>
                <div className="dropdown-item">
                  <NavLink
                    className="nav-link"
                    to="/reporter/public"
                    onClick={() => setShowDropdown(false)}
                  >
                    Öffentliche Anträge
                  </NavLink>
                </div>
                <div className="dropdown-item">
                  <NavLink
                    className="nav-link"
                    to="/reporter/pending"
                    onClick={() => setShowDropdown(false)}
                  >
                    Ausstehende Anträge
                  </NavLink>
                </div>
                <div className="dropdown-item">
                  <NavLink
                    className="nav-link"
                    to="/reporter/approved"
                    onClick={() => setShowDropdown(false)}
                  >
                    Genehmigte Anträge
                  </NavLink>
                </div>
                <div className="dropdown-item">
                  <NavLink
                    className="nav-link"
                    to="/reporter/rejected"
                    onClick={() => setShowDropdown(false)}
                  >
                    Abgelehnte Anträge
                  </NavLink>
                </div>
              </>
            )}

            <div className="dropdown-divider" />
            <div className="dropdown-item">
              <NavLink
                className="nav-link"
                style={{ color: "red" }}
                to="/"
                onClick={() => handleLogout()}
              >
                Abmelden
              </NavLink>
            </div>
          </div>
        )}
      </div>
    </nav>
  );
}
