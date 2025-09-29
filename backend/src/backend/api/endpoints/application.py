# standard library imports
from datetime import datetime
from typing import Optional

# third party imports
from backend.core import db
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

# project imports
from backend.api.deps import   RoleChecker, get_current_user_payload
from backend.core import roleAuth
from backend.crud import userCrud
from backend.models.orm import roletable
from backend.businesslogic.services.applicationService import createApplication, getApplication, editApplication
from backend.businesslogic.services.formService import createForm
from backend.businesslogic.services.adminService import adminApproveApplication, adminRejectApplication
from backend.businesslogic.services.formService import createForm
from backend.models.domain.application import Application, ApplicationStatus, ApplicationID, ApplicationFillout
from backend.crud import userCrud
from backend.crud.user import get_user_by_id
from backend.models.domain.user import User, UserType
from backend.businesslogic.user import ensure_applicant, ensure_admin, ensure_reporter, assign_role
from backend.models import Form   
from datetime import date 
from backend.businesslogic.services.mockups import _global_applications_db, _global_users_db, _global_forms_db
from backend.models.domain.buildingblock import BuildingBlock
from backend.crud import formCrud, applicationCrud
from sqlalchemy.orm import Session

from backend.api import deps

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
# async def non_public_applications(public: Optional[bool] = False):
#     """
#     Dependency to filter applications based on their public status.
#     """
#     # print("Checking public status:", public)
#     if not public:
#         await Depends(admin_or_reporter_permission) # Ensure user is admin or reporter (as per JWT token)

# 2 - If public is True, allow access to everyone (no role check needed)
# 3 - If public is False, ensure the user has admin or reporter role (handled in the dependency above)
# @router.get("", 
#             response_model=list[Application],
#             dependencies=[Depends(non_public_applications)], # Custom dependency to handle public access
#             tags=["Applicati  ons"],
#             summary="List all applications")
# async def list_applications(
#     public: Optional[bool] = False):
#     """
#     Retrieve all applications in the system.
#     """
#     #TODO: add session management?
#     if public:
#         # Fetch applications from db that are public
#         pass
#     else:
#         # this should not be reachable because of the dependency above
#         pass

#     return applicationCrud.get_all_applications(session)

@router.get("", 
            response_model=list[Application],
            dependencies=[Depends(admin_or_reporter_permission)],
            tags=["Applications"],
            summary="List all applications")
async def list_applications(
    session: Session = Depends(db.get_session_dep),
    public: Optional[bool] = None,
    payload: Optional[dict] = Depends(deps.get_current_user_payload_optional)):
    """
    Retrieve all applications in the system.
    """
    is_privileged = False
    if payload:
        user_roles = payload.get("roles", [])
        if set(user_roles) & {"ADMIN", "REPORTER"}:
            is_privileged = True
    
    if is_privileged:
        if public:
            response = applicationCrud.get_all_public_applications(session)
            return response
        else:
            result = applicationCrud.get_all_applications(session)
            return result
    else:
        if public:
            result = applicationCrud.get_all_public_applications(session)
            return result
        else:
            raise HTTPException(status_code=403, detail="You do not have permission to perform this action. Only public applications are visible to all users.")


# @router.post("", response_model=ApplicationID,
#             dependencies=[Depends(applicant_permission)],
#             tags=["Applications"],
#             summary="Create a new application")
# async def create_application(application_data: dict, session: Session = Depends(db.get_session_dep)):
#     """
#     Create a new application in the system.
#     """
#     user_id = application_data.get("user_id", 1)  # Default to user 1 for testing
#     form_id = application_data.get("form_id", 1)  # Default to form 1 for testing
#     payload = application_data.get("payload", {})
    
#     # user = await get_user_by_id(user_id)
#     user = User(id=user_id, username="username", date_created=date.today(), hashed_password="pass") # temporary, replace with actual user retrieval logic
#     assign_role(user, UserType.APPLICANT) # temporary, remove when actual user retrieval logic is implemented
#     if not user:
#         raise ValueError("User not found")
#     if not ensure_applicant(user):
#         raise PermissionError("Only applicants can create applications.")

#     bb = BuildingBlock(label="Name", data_type="STRING")

#     form = Form(form_name="Sample Form", blocks={"1": bb})  # temporary, replace with actual form retrieval logic. But now we are skipping the form logic
#     form = formCrud.add_form(session, form)  # saving the form to get an id   
#     application = createApplication(user, form, payload, session)

#     return ApplicationID(id=application.id)

@router.post("", response_model=ApplicationID,
            dependencies=[Depends(applicant_permission)],
            tags=["Applications"],
            summary="Create a new application")
async def create_application(application_data: ApplicationFillout, session: Session = Depends(db.get_session_dep)):
    """
    Create a new application in the system.
    """
    jwtpayload = get_current_user_payload() # TODO change to get user_id from jwt directly
    username = jwtpayload.get("sub")
    user = userCrud.get_user_by_name(username)
    user_id = user.id
    form_id = application_data.form_id
    jsonPayload = application_data.jsonPayload
    
    application = createApplication(user_id, form_id, jsonPayload, session)

    return ApplicationID(id=application.id)



@router.get("/{application_id}",
            response_model=Application,
            tags=["Applications"],
            summary="Get application by ID")
async def get_application(application_id: int, form_id: int, session: Session = Depends(db.get_session_dep)):
    """
    Retrieve a specific application by its ID.
    """
    try:
        app_id = int(application_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid application ID format")

    application = applicationCrud.get_application_by_id(session, form_id, app_id)
    if not application:
        raise HTTPException(status_code=404, detail=f"Application with ID {app_id} not found")
    return application



@router.put("/{application_id}", response_model=Application, tags=["Applications"], summary="Update an application by ID")
async def update_application(application_id: int, new_application_data: dict, session: Session = Depends(db.get_session_dep)):
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



def example_usage():
    # Example usage
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
    print(_global_applications_db)

if __name__ == "__main__":
    example_usage()