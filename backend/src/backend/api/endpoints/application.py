# standard library imports
from datetime import datetime

# third party imports
from backend.core import db
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

# project imports
from backend.api.deps import   RoleChecker
from backend.businesslogic.services.applicationService import createApplication, getApplication, editApplication
from backend.businesslogic.services.formService import createForm
from backend.businesslogic.services.adminService import adminApproveApplication, adminRejectApplication
from backend.businesslogic.services.formService import createForm
from backend.models.domain.application import Application, ApplicationStatus
from backend.crud.user import get_user_by_id
from backend.models.domain.user import User, UserType
from backend.businesslogic.user import ensure_applicant, ensure_admin, ensure_reporter, assign_role
from backend.models import Form   
from datetime import date 
from backend.businesslogic.services.mockups import _global_applications_db, _global_users_db, _global_forms_db
from backend.models.domain.buildingblock import BuildingBlock
from backend.crud import formCrud, application as applicationCrud
from sqlalchemy.orm import Session

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

    return _global_applications_db

@router.post("", response_model=bool, tags=["Applications"], summary="Create a new application")
async def create_application(application_data: dict, session: Session = Depends(db.get_session_dep)):
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

    bb = BuildingBlock(label="Name", data_type="STRING")

    form = Form(form_name="Sample Form", blocks={"1": bb})  # temporary, replace with actual form retrieval logic. But now we are skipping the form logic
    form = formCrud.add_form(session, form)  # saving the form to get an id   
    application = createApplication(user, form, payload, session)

    # Save application to db

    return application == applicationCrud.get_application_by_id(session, application.form_id, application.id)

@router.get("/{application_id}", response_model=Application, tags=["Applications"], summary="Get application by ID")
async def get_application(application_id: int):
    """
    Retrieve a specific application by its ID.
    """
    try:
        app_id = int(application_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid application ID format")
    
    for app in _global_applications_db:
        if app.id == app_id:
            return app
    
    raise HTTPException(status_code=404, detail=f"Application with ID {app_id} not found")

@router.put("/{application_id}", response_model=Application, tags=["Applications"], summary="Update an application by ID")
async def update_application(application_id: int, new_application_data: dict):
    """
    Update a specific application by its ID.
    """
    from fastapi import HTTPException

    for app in _global_applications_db:
        if app.id == application_id:
            # Create User object for editApplication
            user = User(id=app.user_id, username="username", date_created=date.today(), hashed_password="pass") # TODO: should be replaced with actual user retrieval logic e.g. get_user_by_id()
            assign_role(user, UserType.APPLICANT) 
            
            # Update the application with new data
            app.jsonPayload = new_application_data.get("json_payload", app.jsonPayload)
            
            editApplication(user, app, new_application_data.get("json_payload", {}))
            return app
    
    # If no application found, raise 404 error instead of returning None
    raise HTTPException(status_code=404, detail="Application not found")

@router.delete("/{application_id}", tags=["Applications"], summary="Delete an application by ID")
async def delete_application(application_id: int):
    """
    Delete a specific application by its ID.
    """
    pass



# Test data initialization should be moved to a separate initialization file or startup event
# This code should not run at module import time

