import "./../../style/RegisterPage.css";
import Navbar from "./../../components/Navbar";
import { Role } from "./../../utils/const";
import RegistrationContainer from "./../../components/RegistrationContainer";

export default function AdminRegistration() {
  return (
    <>
      <Navbar />
      <RegistrationContainer roleToRegister={Role.ADMIN} />
    </>
  );
}
