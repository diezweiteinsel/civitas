from datetime import datetime

from backend.businesslogic.services.formService import createForm
from backend.models.domain.user import UserType
from requests import session
from backend.businesslogic.user import assign_role, ensure_admin, ensure_applicant, ensure_reporter
from .mockups import _global_applications_db, _global_forms_db

from backend.models import (
	User,
	Form,
	Application,
	ApplicationStatus,

)
from backend.crud import dbActions
<<<<<<< HEAD
# mockup db as list for testing purposes
applications_db = [
	first_application := Application(
		user_id=1,
		form_id=1,
		status=ApplicationStatus.PENDING,
		createdAt=datetime.now(),
		currentSnapshotID=1,
		previousSnapshotID=0,
		jsonPayload={}
	),
	second_application := Application(
		user_id=2,
		form_id=1,
		status=ApplicationStatus.APPROVED,
		createdAt=datetime.now(),
		currentSnapshotID=2,
		previousSnapshotID=1,
		jsonPayload={}
	),
	third_application := Application(	
		user_id=3,
		form_id=2,
		status=ApplicationStatus.PUBLIC,
		createdAt=datetime.now(),
		currentSnapshotID=3,
		previousSnapshotID=2,
		jsonPayload={}	
	)
]
=======


>>>>>>> 9a41683 (edited the update_app())
def createApplication(user: User, form: Form, payload: dict) -> Application:
	if not ensure_applicant(user):
		raise PermissionError("Only applicants can create applications.")
	""" Creates a new application for a user."""
	# get the needed id for the application from the application table has to be done
	#applicationId = dbActions.getNextId(session, Application). Something like this when the db is set up
	# Generate a unique application ID
	application_id = len(_global_applications_db) + 1
	
	newApplication = Application(
<<<<<<< HEAD
	#	applicationID=1,  # Placeholder, should be set by the database
		user_id=user.id,
		form_id=form.id,
=======
		applicationID=application_id,  # Use generated ID
		userID=user.id,
		formID=form.formID,
>>>>>>> 9a41683 (edited the update_app())
		jsonPayload=payload
	) # Still missing : importing formfields into application, snapshots and filling them with data from payload
	# Logic to save the new application into the db is not defined yet
	_global_applications_db.append(newApplication) # for testing purposes only
	return newApplication


def editApplication(user: User, application: Application, newApplicationData: dict) -> Application:
	""" Allows an applicant to edit their application before it getting processed."""
	if user.id != application.user_id:  # Ensure the user is the owner of the application
		raise PermissionError("Users can only edit their own applications.")
	elif application.status != ApplicationStatus.PENDING:  # Only pending applications can be edited
			raise ValueError("Only pending applications can be edited.")
	# Update the application data with the new data and update the db
	for app in _global_applications_db:
		if app.applicationID == application.applicationID:
			app.jsonPayload = newApplicationData
			application = app # update the reference to the modified application
			break
	# Logic to save the updated application is not defined yet
	return application

def getApplication(user: User, applicationId: int) -> Application:
	application = dbActions.getRowById(session, Application, applicationId) # Retrieve the application from the database
	""" Retrieves an application."""
	if ensure_applicant(user) and application.user_id != user.id and application.status != ApplicationStatus.PUBLIC:
		raise PermissionError("Applicants can only view their own applications.")
	return application

""" 
Publishing applications makes them publicly visible. Only applications with the status 'APPROVED' can be published. Only admins can publish or unpublish applications.
"""
def publishApplication(user: User, application: Application) -> Application:
	""" Publishes an application. Only admins can publish applications."""
	if not ensure_admin(user):
		raise PermissionError("Only admins can publish applications.")
	if application.status != ApplicationStatus.APPROVED:
		raise ValueError("Only approved applications can be published.")
	application.status = ApplicationStatus.PUBLIC
	return application
	# Logic to save the updated application status in the db is not defined yet

"""
Unpublishing applications reverts their status from 'PUBLIC' back to 'APPROVED'. Only admins can unpublish applications.
"""
def unpublishApplication(user: User, application: Application) -> Application:
	""" Unpublishes an application. Only admins can unpublish applications."""
	if not ensure_admin(user):
		raise PermissionError("Only admins can unpublish applications.")
	if application.status != ApplicationStatus.PUBLIC:
		raise ValueError("Only public applications can be unpublished.")
	application.status = ApplicationStatus.APPROVED
	return application
	# Logic to save the updated application status in the db is not defined yet

def submitApplication(user: User, application: Application):
	""" Submits an application for processing."""
	if user.id != application.user_id:  # Ensure the user is the owner of the application
		raise PermissionError("Users can only submit their own applications.")
	# Logic to submit the application is not defined yet
	# dbActions.insertRow(session, Application, application.__dict__)
	return application
	

# Mock database of applications for demonstration purposes
allApplications = []  # This would be replaced with actual database queries


def listOwnApplications(user: User):
	listOfApplications = [
		app for app in allApplications if app.user_id == user.id # Applicants can see their own applications
	]
	return listOfApplications


def listAllApplications(user: User):
	""" Lists all applications in the system. Admins and reporters can see all, applicants only public ones."""
	if ensure_admin(user) or ensure_reporter(user):
		return allApplications  # Admins and reporters can see all applications
	else :
		raise PermissionError("Applicants can only view their own applications or public applications.")


def listPendingApplications(user: User):
	""" Lists all pending applications. Only admins and reporters can see pending applications."""
	if ensure_admin(user) or ensure_reporter(user):
		return [app for app in allApplications if app.status == ApplicationStatus.PENDING]
	else:
		raise PermissionError("Only admins and reporters can view all pending applications.")


def listAllPublicApplications(user: User):
	""" Lists all public applications. All user types can see public applications."""
	return [app for app in allApplications if app.status == ApplicationStatus.PUBLIC]


