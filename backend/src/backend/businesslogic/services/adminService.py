from datetime import date

from backend.models import User, Form, Application, ApplicationStatus, UserType
from backend.models.domain.user import RoleAssignment
from backend.businesslogic.user import ensure_admin, assign_role
from sqlalchemy.orm import Session
from backend.depr_auth import hash_password
from backend.crud.dbActions import insertRow
from backend.crud.application import get_application_by_id, updateApplicationStatus



def createUser(user: User,id:int, username: str, password: str, role: UserType):
	if not ensure_admin(user):
		return None
	if role==UserType.APPLICANT: 
		raise PermissionError("Applicants can only be created via self-registration.")
	""" Creates a new user in the system."""
	# Hash the password and create an Account instance	
	hashed_pw = hash_password(password)
	newUser = User(id=id, username=username, date_created=date.today(), hashed_password=hashed_pw)
	assign_role(newUser, role)  
	# Logic to save the user to the database is not defined yet
	return newUser


def adminApproveApplication(application_id: int,
                         	form_id: int,
                          	session: Session) -> bool:
	updateApplicationStatus(session, form_id, application_id, ApplicationStatus.APPROVED)
	# Logic to save the updated application status is not defined yet
	return True


def adminRejectApplication(application_id: int,
                         	form_id: int,
                          	session: Session):
	updateApplicationStatus(session, form_id, application_id, ApplicationStatus.REJECTED)
	# Logic to save the updated application status is not defined yet
	return True
