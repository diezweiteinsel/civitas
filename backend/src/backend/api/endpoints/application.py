# standard library imports
from datetime import datetime

# third party imports
from fastapi import APIRouter, HTTPException

# project imports
from backend.api.deps import   RoleChecker
from backend.businesslogic.services.applicationService import createApplication, getApplication, editApplication
<<<<<<< HEAD
from backend.businesslogic.services.formService import createForm
from backend.businesslogic.services.adminService import adminApproveApplication, adminRejectApplication
=======
>>>>>>> 6bd32a3 (edited the update_app())
from backend.models.domain.application import Application, ApplicationStatus
from backend.crud.user import get_user_by_id
from backend.models.domain.user import User, UserType
from backend.businesslogic.user import ensure_applicant, ensure_admin, ensure_reporter, assign_role
from backend.models import Form   
from datetime import date 
<<<<<<< HEAD
from backend.businesslogic.services.mockups import _global_applications_db, _global_users_db, _global_forms_db
=======
from backend.businesslogic.services.mockups import _global_applications_db as applications_db
>>>>>>> 6bd32a3 (edited the update_app())

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
<<<<<<< HEAD
    return _global_applications_db
=======
    pass
>>>>>>> 6bd32a3 (edited the update_app())

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
    form = Form(id=form_id)  # temporary, replace with actual form retrieval logic. But now we are skipping the form logic
    
    application = createApplication(user, form, payload)

    # Save application to db

    return application in _global_applications_db

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
        if app.applicationID == app_id:
            return app
    
    raise HTTPException(status_code=404, detail=f"Application with ID {app_id} not found")

@router.put("/{application_id}", response_model=Application, tags=["Applications"], summary="Update an application by ID")
async def update_application(application_id: int, new_application_data: dict):
    """
    Update a specific application by its ID.
    """
    from fastapi import HTTPException
    
<<<<<<< HEAD
    for app in _global_applications_db:
=======
    for app in applications_db:
>>>>>>> 6bd32a3 (edited the update_app())
        if app.applicationID == application_id:
            # Create User object for editApplication
            user = User(id=app.userID, username="username", date_created=date.today(), hashed_password="pass") # TODO: should be replaced with actual user retrieval logic e.g. get_user_by_id()
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


if __name__ == "__main__":
    # tests
    Admin = User(id=1, username="admin", date_created=date.today(), hashed_password="admin")
    assign_role(Admin, UserType.ADMIN)
    Applicant = User(id=2, username="applicant", date_created=date.today(), hashed_password="applicant")
    assign_role(Applicant, UserType.APPLICANT)
    Reporter = User(id=3, username="reporter", date_created=date.today(), hashed_password="reporter")
    assign_role(Reporter, UserType.REPORTER)
    _global_users_db.extend([Admin, Applicant, Reporter])
    form = createForm(Admin, {"title": "Form 1", "fields": [{"name": "field1", "type": "text"}, {"name": "field2", "type": "number"}]})
    createApplication(Applicant, form ,{"field1": "value1", "field2": "value2"})
    createApplication(Applicant, form ,{"field1": "value3", "field2": "value4"})
    adminRejectApplication(Admin, _global_applications_db[1])
    createApplication(Applicant, form ,{"field1": "value5", "field2": "value6"})
    adminApproveApplication(Admin, _global_applications_db[2])