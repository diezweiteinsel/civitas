# tests for publicationService
from backend.businesslogic.services.publicationService import publishApplication, unpublishApplication
from backend.businesslogic.services.applicationService import createApplication
from backend.businesslogic.services.adminService import adminApproveApplication
from backend.businesslogic.selfRegistration import register_Applicant
from backend.models import User, UserType, Application, ApplicationStatus, Form

# Create a mock admin user
admin_user = User(id=1, username="admin", user_type=UserType.ADMIN)

# mock register applicant user
applicant_user = register_Applicant(username="applicant", password="password")
applicant_user.id = 2  # Manually set ID for testing
# create a mock application
form = Form()  # Create a new form instance
application = createApplication(user=applicant_user, form=form, payload={"field": "value"})

# Approve the application to make it eligible for publishing
application = adminApproveApplication(admin_user, application)

def test_publish_application():
    # Publish the application
    published_application = publishApplication(admin_user, application)

    assert published_application.status == ApplicationStatus.PUBLIC

test_publish_application()
def test_unpublish_application():
    # Approve the application to make it eligible for publishing
    adminApproveApplication(admin_user, application)
    # First, ensure the application is published
    published_application = publishApplication(admin_user, application)

    # Now, unpublish the application
    unpublished_application = unpublishApplication(admin_user, published_application)

    assert unpublished_application.status == ApplicationStatus.APPROVED

test_unpublish_application()