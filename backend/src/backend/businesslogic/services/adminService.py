from datetime import date

from backend.models import User, Form, Application, ApplicationStatus, UserType
from backend.models.domain.user import RoleAssignment
from backend.businesslogic.user import ensure_admin, assign_role
from backend.depr_auth import hash_password
from backend.crud.dbActions import insertRow



def createUser(user: User,id:int, username: str, password: str, role: UserType):
	if not ensure_admin(user):
		return None
	if role==UserType.APPLICANT: 
		raise PermissionError("Applicants can only be created via self-registration.")
	""" Creates a new user in the system."""
	# Hash the password and create an Account instance	
	hashed_pw = hash_password(password)
	newUser = User(id=id, username=username, date_created=date.today(), hashed_password=hashed_pw)
	newUser.user_roles.append(RoleAssignment(
		user_id=newUser.id,
		role=role,
		assignment_date=date.today()
	))
	# Save the User to the database
	#insertRow(newUser)  # add the new user to the database
	return newUser


def adminApproveApplication(user: User, application: Application):
	if not ensure_admin(user):
		raise PermissionError("Only admins can approve applications.")
	""" Approves an application."""
	application.status = ApplicationStatus.APPROVED
	# Logic to save the updated application status is not defined yet
	return application


def adminRejectApplication(user: User, application: Application):
	if not ensure_admin(user):
		raise PermissionError("Only admins can reject applications.")
	""" Rejects an application."""
	application.status = ApplicationStatus.REJECTED
	# Logic to save the updated application status is not defined yet
	return application
