from backend.businesslogic.services.adminService import createUser, adminApproveApplication, adminRejectApplication, ensure_admin
from backend.models.domain.user import UserType, User,RoleAssignment
from backend.models.domain.buildingblock import BuildingBlock, BBType
from backend.models.domain.application import Application, ApplicationStatus
from datetime import date
import pytest

#test AdminService
# pytest tests/businesslogic/testServices.py::test_create_user
admin=User(id=1, username="admin", date_created=date.today(), hashed_password="hashed")
admin_role_assignment = RoleAssignment(
    user_id=admin.id,
    role=UserType.ADMIN,
    assignment_date=date.today()
)
admin.user_roles.append(admin_role_assignment)

def test_ensure_admin():
    assert ensure_admin(admin) is True
    try:
        ensure_admin(None)
    except PermissionError:
        pass

    non_admin = User(id=2, username="user", date_created=date.today(), hashed_password="hashed")
    try:
        ensure_admin(non_admin)
    except False:
        pass
test_ensure_admin()



def test_create_user():
    # Test creating a user with admin privileges
    user = createUser(admin,id=2, username="testuser", password="password", role=UserType.ADMIN)
    assert user.id == 2
    assert user.username == "testuser"
    assert user.user_roles[0].role == UserType.ADMIN
    assert user.date_created is not None
    try:
        createUser(admin,id=3, username="testuser2", password="password2", role=UserType.APPLICANT)
    except PermissionError:
        pass
    else:
        assert False, "Expected PermissionError when creating an applicant user"

test_create_user()

def test_adminApprove():
    # Mock application object
    application = Application(applicationID=1, userID=2, formID=1)
    adminApproveApplication(admin, application)  # Approve the application
    assert application.status == ApplicationStatus.APPROVED

test_adminApprove()

def test_adminReject():
    # Mock application object
    application = Application(applicationID=1, userID=2, formID=1)
    adminRejectApplication(admin, application)  # Reject the application
    assert application.status == ApplicationStatus.REJECTED

test_adminReject()
