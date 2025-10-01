/**
 * AdminRegistration Component
 * 
 * This component provides a registration page specifically for creating new admin users.
 * It's part of the admin panel and allows existing admins to register new administrative accounts.
 * 
 * @component
 * @example
 * // Used in routing for admin user registration
 * <Route path="/admin/admin-registration" element={<AdminRegistration />} />
 * 
 * @author Civitas Development Team
 * @since 2025
 */

// Styling imports
import "./../../style/RegisterPage.css"; // Common registration page styles

// Component imports
import Navbar from "./../../components/Navbar"; // Site navigation component
import RegistrationContainer from "./../../components/RegistrationContainer"; // Reusable registration form container

// Utility imports
import { Role } from "./../../utils/const"; // Role constants for user types

/**
 * AdminRegistration functional component
 * 
 * Renders a complete admin registration page with navigation and form.
 * Uses the RegistrationContainer component with Role.ADMIN to create 
 * admin-specific registration functionality.
 * 
 * Features:
 * - Site navigation via Navbar
 * - Admin-specific user registration form
 * - Consistent styling with other registration pages
 * - Role-based registration (ADMIN role)
 * 
 * Access Control:
 * - This page should only be accessible to existing admin users
 * - Route protection should be implemented at the router level
 * 
 * @returns {JSX.Element} Complete admin registration page
 */
export default function AdminRegistration() {
  return (
    <>
      {/* Site navigation bar */}
      <Navbar />
      
      {/* Registration form container configured for admin role */}
      <RegistrationContainer roleToRegister={Role.ADMIN} />
    </>
  );
}
