from backend.businesslogic.services.applicationService import createApplication, editApplication, submitApplication, getApplication, listOwnApplications,listAllApplications,listAllPublicApplications,listPendingApplications, allApplications
from backend.businesslogic.services.adminService import adminApproveApplication
from backend.businesslogic.user import assign_role, ensure_admin
from backend.models.domain.user import RoleAssignment, UserType, User
from backend.models.domain.buildingblock import BuildingBlock, BBType
from backend.models.domain.application import Application, ApplicationStatus
from backend.models.domain.form import Form
from datetime import date



#test ApplicationService

applicant=User(id=2, username="applicant", hashed_password="hashed", date_created=date.today())
admin = User(id=1, username="admin", hashed_password="hashed", date_created=date.today())
assign_role(applicant, UserType.APPLICANT)
assign_role(admin, UserType.ADMIN)

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
    adminApproveApplication(admin, application) # Admin approves the application
    assert application.status == ApplicationStatus.APPROVED # Application status should be updated to APPROVED
test_editApplication()

def test_submitApplication():
    application = createApplication(applicant, form, payload)
    submitApplication(applicant, application)
    assert application.status == ApplicationStatus.PENDING # Status should remain PENDING as submit logic is not defined yet
    # testing the db not implemented yet

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
        assert str(e) == "Only admins and reporters can view all pending applications."

test_listPendingApplications()


def test_listAllPublicApplications():
    user = applicant
    publicApps = listAllPublicApplications(user)
    assert len(publicApps) == 0
    assert application1 not in publicApps
    assert application2 not in publicApps
    assert application3 not in publicApps

test_listAllPublicApplications()