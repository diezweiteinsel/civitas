from datetime import datetime

from backend.models import User, Form, Application, ApplicationStatus, UserType
from backend.crud.dbActions import insertRow

def createUser(user: User,id:int, username: str, password: str, role: UserType):
	if user.user_type != UserType.ADMIN:
		raise PermissionError("Only admins can create new users.")
	if role==UserType.APPLICANT: 
		raise PermissionError("Applicants can only be created via self-registration.")
	""" Creates a new user in the system."""
	newUser = User(id=id, username=username, user_type=role, date_created=datetime.now(), email=None)
	# Hash the password and create an Account instance
	#newAccount = Account(user=newUser, hashed_password=password, status=AccountStatus.ACTIVE)
	# Save the User and Account to the database
	#insertRow(newUser)  # add the new user to the database
	return newUser


def createForm(user, form_structure):
	if user.user_type != UserType.ADMIN:
		raise PermissionError("Only admins can create new forms.")
	""" Creates a new form in the system."""
	newForm = Form(fields=form_structure, date_created=datetime.now())
	#insertRow(newForm)  # add the new form to the database
	return newForm


def adminApproveApplication(user: User, application: Application):
	if user.user_type != UserType.ADMIN:
		raise PermissionError("Only admins can approve applications.")
	""" Approves an application."""
	application.status = ApplicationStatus.APPROVED
	# Logic to save the updated application status is not defined yet
	return application


def adminRejectApplication(user: User, application: Application):
	if user.user_type != UserType.ADMIN:
		raise PermissionError("Only admins can reject applications.")
	""" Rejects an application."""
	application.status = ApplicationStatus.REJECTED
	# Logic to save the updated application status is not defined yet
	return application
