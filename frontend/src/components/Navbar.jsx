import "./../style/Navbar.css";
import logo from "./../img/civitas.png";
import { GiHamburgerMenu } from "react-icons/gi";
import Dropdown from "react-bootstrap/Dropdown";
import { NavLink, useNavigate } from "react-router-dom";
import { useRef, useState, useEffect } from "react";
import { Role } from "../utils/const";

function Logo() {
  return <img src={logo} alt="Logo" className="navbar-img" />;
}

export default function Navbar({ role = Role.EMPTY }) {
  const navigate = useNavigate();
  const [showDropdown, setShowDropdown] = useState(false);
  const dropdownRef = useRef(null);

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
      <NavLink
        to={
          role === Role.ADMIN
            ? "/admin"
            : role === Role.REPORTER
            ? "/reporter"
            : "/applicant"
        }
        className="navbar-logo"
      >
        <Logo />
      </NavLink>

      <NavLink
        to={
          role === Role.ADMIN
            ? "/admin"
            : role === Role.REPORTER
            ? "/reporter"
            : "/applicant"
        }
        className="navbar-home"
      >
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
                    to="/reporter/reporter/public"
                    onClick={() => setShowDropdown(false)}
                  >
                    Offentliche Anträge
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
