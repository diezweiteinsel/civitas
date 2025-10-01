from datetime import datetime

from backend.core import roleAuth
from backend.models.domain.application import ApplicationResponseItem
from backend.models.domain.user import UserType
from fastapi import HTTPException
from requests import session
from backend.businesslogic.user import assign_role, ensure_admin, ensure_applicant, ensure_reporter
from sqlalchemy.orm import Session


from backend.models import (
	User,
	Form,
	Application,
	ApplicationStatus,

)
from backend.crud import dbActions, application as applicationCrud, formCrud



def createApplication(user_id: int, form_id: int, payload: dict, session: Session) -> Application:
	""" Creates a new application for a user."""
	# Ensure the user specified in the application has the applicant role
	if not roleAuth.check_role(session, user_id=user_id, role="APPLICANT"): #TODO
		raise HTTPException(status_code=404, detail="User from application not found or is not applicant")
	# generate application from ApplicationFillout
	try:
		newApplication = Application(
		user_id=user_id,
		form_id=form_id,
		jsonPayload=payload
	) 
	except:
		raise HTTPException(status_code=420, detail="TODO") # TODO
	# insert application into db and return updated application (with id etc.)
	appFromTable = applicationCrud.insert_application(session, newApplication)
	newApplication=applicationCrud.rowToApplication(appFromTable)
	return newApplication



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


def app_list_to_appResp_list(session, appList: list[Application]):
	resultList = []
	for app in appList:
		resultList.append(ApplicationResponseItem(
				id=app.id,
				form_id=app.form_id,
				title=formCrud.get_form_by_id(session, app.form_id).form_name,
				status=app.status,
				created_at=app.created_at,
				is_public=app.is_public,
				snapshots=app.snapshots,
				jsonPayload=app.jsonPayload
				))
	return resultList