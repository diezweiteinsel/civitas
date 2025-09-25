""" Service for publishing and unpublishing applications. """

from backend.models import (
	User,
	UserType,
	Application,
	ApplicationStatus,
)

def publishApplication(user: User, application: Application) -> Application:
	""" Publishes an application. Only admins can publish applications."""
	if user.user_type != UserType.ADMIN:
		raise PermissionError("Only admins can publish applications.")
	if application.status != ApplicationStatus.APPROVED:
		raise ValueError("Only approved applications can be published.")
	application.status = ApplicationStatus.PUBLIC
	return application
	# Logic to save the updated application status in the db is not defined yet

def unpublishApplication(user: User, application: Application) -> Application:
	""" Unpublishes an application. Only admins can unpublish applications."""
	if user.user_type != UserType.ADMIN:
		raise PermissionError("Only admins can unpublish applications.")
	if application.status != ApplicationStatus.PUBLIC:
		raise ValueError("Only public applications can be unpublished.")
	application.status = ApplicationStatus.APPROVED
	return application
	# Logic to save the updated application status in the db is not defined yet
	