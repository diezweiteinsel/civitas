from backend.businesslogic.services.applicationService import createApplication, editApplication, submitApplication, getApplication, listOwnApplications,listAllApplications,listAllPublicApplications,listPendingApplications, allApplications
from backend.businesslogic.services.adminService import adminApprove
from backend.models.domain.user import UserType, User
from backend.models.domain.buildingblock import BuildingBlock, BBType
from backend.models.domain.application import Application, ApplicationStatus
from backend.models.domain.form import Form
from datetime import datetime


#test ApplicationService

applicant=User(id=2, username="applicant", user_type=UserType.APPLICANT, date_created=datetime.now(), email="applicant@example.com")
admin = User(id=1, username="admin", user_type=UserType.ADMIN, date_created=datetime.now(), email="admin@example.com")

payload = {
        "type": BBType.STRING,
        "label": "First Name",
        "required": True,
        "value": "John"
    } # Example payload, will be replaced with actual data from user
form = Form(formID=1) # Example form, will be replaced with actual form from DB

def test_createApplication():
    #list of building blocks
    form = Form(formID=1) # Example form, will be replaced with actual form from DB
    application = createApplication(applicant, form, payload)
    assert application is not None
    assert application.userID == applicant.id
    assert application.formID == form.formID
    assert application.jsonPayload == payload
    assert application.createdAt is not None

test_createApplication()

def test_editApplication(): 
    application = createApplication(applicant, form, payload)
    newPayload = {
        "type": BBType.STRING,
        "label": "First Name",
        "required": True,
        "value": "Jane"
    }
    editApplication(applicant, application, newPayload)
    assert application.jsonPayload == newPayload
    assert application.status == ApplicationStatus.PENDING
    admin=User(id=1, username="admin", user_type=UserType.ADMIN, date_created=datetime.now(), email="admin@example.com") # Example admin user
    adminApprove(admin, application) # Admin approves the application
    assert application.status == ApplicationStatus.APPROVED # Application status should be updated to APPROVED

test_editApplication()

def test_submitApplication():
    application = createApplication(applicant, form, payload)
    submitApplication(applicant, application)
    assert application.status == ApplicationStatus.PENDING # Status should remain PENDING as submit logic is not defined yet

test_submitApplication()

def test_getApplication():
    application = createApplication(applicant, form, payload)
    retrievedApp = getApplication(applicant, application.applicationID)
    assert retrievedApp == application

#test_getApplication()

# Mock database of applications for demonstration purposes
application1 = createApplication(applicant, form, payload)
application2 = createApplication(applicant, form, payload)
application3 = createApplication(applicant, form, {})
allApplications.extend([application1, application2, application3])  # Simulate saving to a database

def test_listOwnApplications():
    userApplications = listOwnApplications(applicant)
    assert len(userApplications) == 3
    assert application1 in userApplications
    assert application2 in userApplications
    assert application3 in userApplications
test_listOwnApplications()

def test_listAllApplications():
    allApps = listAllApplications(admin)
    assert len(allApps) == 3
    try:
        applicantApps = listAllApplications(applicant)
    except PermissionError as e:
        assert str(e) == "Applicants can only view their own applications or public applications."
test_listAllApplications()

def test_listPendingApplications():
    pendingApps = listPendingApplications(admin)
    assert len(pendingApps) == 3
    try:
        applicantPendingApps = listPendingApplications(applicant)
    except PermissionError as e:
        assert str(e) == "Only admins and reporters can view pending applications."

test_listPendingApplications()


def test_listAllPublicApplications(user: User):
    publicApps = listAllPublicApplications(user)
    assert len(publicApps) == 3
    assert application1 in publicApps
    assert application2 in publicApps
    assert application3 in publicApps