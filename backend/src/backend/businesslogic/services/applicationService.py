from datetime import datetime

from requests import session

from backend.models import (
	User,
	Form,
	Application,
	ApplicationStatus,
	UserType,

)
from backend.crud import dbActions
# mockup db as list for testing purposes
applications_db = []
def createApplication(user: User, form: Form, payload: dict) -> Application:
	if user.user_type != UserType.APPLICANT:
		raise PermissionError("Only applicants can create applications.")
	""" Creates a new application for a user."""
	# get the needed id for the application from the application table has to be done
	#applicationId = dbActions.getNextId(session, Application). Something like this when the db is set up
	newApplication = Application(
	#	applicationID=1,  # Placeholder, should be set by the database
		userID=user.id,
		formID=form.formID,
		jsonPayload=payload
	) # Still missing : importing formfields into application, snapshots and filling them with data from payload 
	# Logic to save the new application is not defined yet
	return newApplication


def editApplication(user: User, application: Application, newApplicationData: dict) -> Application:
	""" Allows an applicant to edit their application before it getting processed."""
	if user.id != application.userID:  # Ensure the user is the owner of the application
		raise PermissionError("Users can only edit their own applications.")
	elif application.status != ApplicationStatus.PENDING:  # Only pending applications can be edited
			raise ValueError("Only pending applications can be edited.")
	application.jsonPayload = newApplicationData
	# Logic to save the updated application is not defined yet
	return application


def submitApplication(user: User, application: Application):
	""" Submits an application for processing."""
	if user.id != application.userID:  # Ensure the user is the owner of the application
		raise PermissionError("Users can only submit their own applications.")
	# Logic to submit the application is not defined yet
	# dbActions.insertRow(session, Application, application.__dict__)
	return application


def getApplication(user: User, applicationId: int) -> Application:
	application = dbActions.getRowById(session, Application, applicationId) # Retrieve the application from the database
	""" Retrieves an application."""
	if user.user_type == UserType.APPLICANT and application.userID != user.id and application.status != ApplicationStatus.PUBLIC:
		raise PermissionError("Applicants can only view their own applications.")
	return application

# Mock database of applications for demonstration purposes
allApplications = []  # This would be replaced with actual database queries


def listOwnApplications(user: User):
	listOfApplications = [
		app for app in allApplications if app.userID == user.id # Applicants can see their own applications
	]
	return listOfApplications


def listAllApplications(user: User):
	""" Lists all applications in the system. Admins and reporters can see all, applicants only public ones."""
	if user.user_type == UserType.ADMIN or user.user_type == UserType.REPORTER:
		return allApplications  # Admins and reporters can see all applications
	else :
		raise PermissionError("Applicants can only view their own applications or public applications.")


def listPendingApplications(user: User):
	""" Lists all pending applications. Only admins and reporters can see pending applications."""
	if user.user_type == UserType.ADMIN or user.user_type == UserType.REPORTER:
		return [app for app in allApplications if app.status == ApplicationStatus.PENDING]
	else:
		raise PermissionError("Only admins and reporters can view pending applications.")


def listAllPublicApplications(user: User):
	""" Lists all public applications. All user types can see public applications."""
	return [app for app in allApplications if app.status == ApplicationStatus.PUBLIC]
