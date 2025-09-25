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

  return (
    <nav className="navbar">
      <Logo />
      <div className="navbar-brand">CIVITAS</div>
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
                    Homepage
                  </NavLink>
                </div>
                <div className="dropdown-item">
                  <NavLink
                    className="nav-link"
                    to="/admin/public?from=admin"
                    onClick={() => setShowDropdown(false)}
                  >
                    Public Applications
                  </NavLink>
                </div>
                <div className="dropdown-item">
                  <NavLink
                    className="nav-link"
                    to="/admin/edit-form"
                    onClick={() => setShowDropdown(false)}
                  >
                    Edit Form
                  </NavLink>
                </div>
                <div className="dropdown-item">
                  <NavLink
                    className="nav-link"
                    to="/admin/admin-registration"
                    onClick={() => setShowDropdown(false)}
                  >
                    Register Admin
                  </NavLink>
                </div>
                <div className="dropdown-item">
                  <NavLink
                    className="nav-link"
                    to="/admin/reporter-registration"
                    onClick={() => setShowDropdown(false)}
                  >
                    Register Reporter
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
                    Homepage
                  </NavLink>
                </div>
                <div className="dropdown-item">
                  <NavLink
                    className="nav-link"
                    to="/applicant/public?from=applicant"
                    onClick={() => setShowDropdown(false)}
                  >
                    Public Applications
                  </NavLink>
                </div>
                <div className="dropdown-item">
                  <NavLink
                    className="nav-link"
                    to="/applicant/submit"
                    onClick={() => setShowDropdown(false)}
                  >
                    Submit Application
                  </NavLink>
                </div>
              </>
            )}

            {role === Role.REPORTER && (
              <>
                <div className="dropdown-item">
                  <NavLink
                    className="nav-link"
                    to="/applicant"
                    onClick={() => setShowDropdown(false)}
                  >
                    Homepage
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
                onClick={() => setShowDropdown(false)}
              >
                Log out
              </NavLink>
            </div>
          </div>
        )}
      </div>
    </nav>
  );
}
