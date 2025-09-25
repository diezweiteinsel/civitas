# standard library imports
from datetime import datetime

# third party imports
from fastapi import APIRouter

# project imports
from backend.api.deps import RoleChecker
from backend.models.domain.application import Application, ApplicationStatus

# print("i only exist because of merge conflicts")

router = APIRouter(prefix="/applications", tags=["applications"])
admin_or_reporter_permission = RoleChecker(["ADMIN", "REPORTER"])
applicant_permission = RoleChecker(["APPLICANT"])

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
    
    pass

@router.post("", response_model=Application, tags=["Applications"], summary="Create a new application")
async def create_application(application: Application):
    """
    Create a new application in the system.
    """
    application.applicationID = 1  # Simulate assigning a new ID
    application.createdAt = datetime.now()
    return application

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
