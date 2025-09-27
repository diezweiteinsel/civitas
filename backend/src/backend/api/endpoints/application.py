# standard library imports
from datetime import datetime

# third party imports
from fastapi import APIRouter

# project imports
from backend.api.deps import   RoleChecker
from backend.businesslogic.services.applicationService import createApplication, getApplication
from backend.models.domain.application import Application, ApplicationStatus
from backend.crud.user import get_user_by_id
from backend.models.domain.user import User, UserType
from backend.businesslogic.user import ensure_applicant, ensure_admin, ensure_reporter, assign_role
from backend.models import Form   
from datetime import date 
from backend.businesslogic.services.applicationService import applications_db

# print("i only exist because of merge conflicts")

router = APIRouter(prefix="/applications", tags=["applications"])
# admin_or_reporter_permission = RoleChecker(["ADMIN", "REPORTER"])
# applicant_permission = RoleChecker(["APPLICANT"])

    # applicationID: int = -1
    # userID: int = -1
    # formID: int = -1
    # status: ApplicationStatus = ApplicationStatus.PENDING
    # createdAt: datetime = datetime.now()
    # currentSnapshotID: int = -1  # Points to the latest snapshot of the application
    # previousSnapshotID: int = -1  # Points to the previous snapshot of the application
    # jsonPayload: dict = {}  # The actual data of the application

@router.get("", response_model=list[Application], tags=["Applications"], summary="List all applications")
async def list_applications():
    """
    Retrieve all applications in the system.
    """
    return applications_db

@router.post("", response_model=bool, tags=["Applications"], summary="Create a new application")
async def create_application(application_data: dict):
    """
    Create a new application in the system.
    """
    user_id = application_data.get("user_id", 1)  # Default to user 1 for testing
    form_id = application_data.get("form_id", 1)  # Default to form 1 for testing
    payload = application_data.get("payload", {})
    
    # user = await get_user_by_id(user_id)
    user = User(id=user_id, username="username", date_created=date.today(), hashed_password="pass") # temporary, replace with actual user retrieval logic
    assign_role(user, UserType.APPLICANT) # temporary, remove when actual user retrieval logic is implemented
    if not user:
        raise ValueError("User not found")
    if not ensure_applicant(user):
        raise PermissionError("Only applicants can create applications.")
    form = Form(formID=form_id)  # temporary, replace with actual form retrieval logic. But now we are skipping the form logic
    
    application = createApplication(user, form, payload)

    # Save application to db

    return application in applications_db

@router.get("/{application_id}", response_model=Application, tags=["Applications"], summary="Get application by ID")
async def get_application(application_id: int):
    """
    Retrieve a specific application by its ID.
    """
    pass

@router.put("/{application_id}", response_model=Application, tags=["Applications"], summary="Update an application by ID")
async def update_application(application_id: int, application: Application):
    """
    Update a specific application by its ID.
    """
    application.applicationID = application_id  # Ensure the ID remains the same
    return application

@router.delete("/{application_id}", tags=["Applications"], summary="Delete an application by ID")
async def delete_application(application_id: int):
    """
    Delete a specific application by its ID.
    """
    pass
