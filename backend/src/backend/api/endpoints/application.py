# standard library imports
from datetime import datetime
from typing import Optional

# third party imports
from fastapi import APIRouter, Depends, HTTPException

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

# CAN READ ALL
admin_or_reporter_permission = RoleChecker(["ADMIN", "REPORTER"])

# CAN EDIT FORMS AND REGISTER USERS
admin_permission = RoleChecker(["ADMIN"])

# CAN CREATE APPLICATIONS
applicant_permission = RoleChecker(["APPLICANT"])

    # applicationID: int = -1
    # userID: int = -1
    # formID: int = -1
    # status: ApplicationStatus = ApplicationStatus.PENDING
    # createdAt: datetime = datetime.now()
    # currentSnapshotID: int = -1  # Points to the latest snapshot of the application
    # previousSnapshotID: int = -1  # Points to the previous snapshot of the application
    # jsonPayload: dict = {}  # The actual data of the application



# GET ALL APPLICATIONS
# Using query `?public=true` to filter public applications
# If `public` is false or not provided, only admin or reporter can access,
# and all applications are returned.
# If `public` is true, anyone can access, but only public applications are returned.

# 1 - Define a dependency to check the public status and user role
async def non_public_applications(public: Optional[bool] = False):
    """
    Dependency to filter applications based on their public status.
    """
    # print("Checking public status:", public)
    if not public:
        await Depends(admin_or_reporter_permission) # Ensure user is admin or reporter (as per JWT token)

# 2 - If public is True, allow access to everyone (no role check needed)
# 3 - If public is False, ensure the user has admin or reporter role (handled in the dependency above)
@router.get("", 
            response_model=list[Application],
            dependencies=[Depends(non_public_applications)], # Custom dependency to handle public access
            tags=["Applications"],
            summary="List all applications")
async def list_applications(
    public: Optional[bool] = False):
    """
    Retrieve all applications in the system.
    """
    #TODO: add session management?
    if public:
        # Fetch applications from db that are public
        pass
    else:
        # this should not be reachable because of the dependency above
        pass



@router.post("", response_model=bool,
            dependencies=[Depends(applicant_permission)],
            tags=["Applications"],
            summary="Create a new application")
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
    form = Form(id=form_id)  # temporary, replace with actual form retrieval logic. But now we are skipping the form logic
    
    application = createApplication(user, form, payload)

    # Save application to db

    return application in applications_db


@router.get("/{application_id}",
            response_model=Application,
            tags=["Applications"],
            summary="Get application by ID")
async def get_application(application_id: int):
    """
    Retrieve a specific application by its ID.
    """
    try:
        app_id = int(application_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid application ID format")
    
    for app in applications_db:
        if app.applicationID == app_id:
            return app
    
    raise HTTPException(status_code=404, detail=f"Application with ID {app_id} not found")


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


