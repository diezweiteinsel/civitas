# standard library imports
from typing import List, Optional

# third party imports
from backend.core import db
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

# project imports
from backend.api.deps import   RoleChecker, get_current_user_payload, get_current_user_payload_optional
from backend.core import roleAuth
from backend.crud import userCrud
from backend.models.orm import roletable
from backend.businesslogic.services.applicationService import createApplication, getApplication
from backend.businesslogic.services.adminService import adminApproveApplication, adminRejectApplication
from backend.models.domain.application import Application, ApplicationStatus, ApplicationID, ApplicationFillout, ApplicationUpdate
from backend.crud import userCrud
from backend.crud.user import get_user_by_id
from backend.models.domain.user import User, UserType
from backend.businesslogic.user import ensure_applicant, ensure_admin, ensure_reporter, assign_role
from backend.models import Form   
from datetime import date 
from backend.models.domain.buildingblock import BuildingBlock
from backend.crud import formCrud, applicationCrud
from backend.businesslogic.services.applicationService import app_list_to_appResp_list
from sqlalchemy.orm import Session

from backend.api import deps

from backend.models.domain.application import ApplicationResponseItem

from backend.models.domain.application import application_to_response_item

router = APIRouter(prefix="/applications", tags=["applications"])

# CAN READ ALL
admin_or_reporter_permission = RoleChecker(["ADMIN", "REPORTER"])

# CAN EDIT FORMS AND REGISTER USERS
admin_permission = RoleChecker(["ADMIN"])

# CAN CREATE APPLICATIONS
applicant_permission = RoleChecker(["APPLICANT"])



@router.get("", 
            response_model=list[ApplicationResponseItem],
            tags=["Applications"],
            summary="List all applications")
async def list_applications(
    session: Session = Depends(db.get_session_dep),
    public: Optional[bool] = None,
    status: Optional[List[ApplicationStatus]] = Query(None, description="Filter by one or more statuses."),
    payload: Optional[dict] = Depends(deps.get_current_user_payload_optional)):
    """
    Retrieve all applications in the system.
    
    Possible query parameters:
    - **public**: `true` or `false`. If `true`, only public applications are returned. If `false` or not provided, all applications are returned, if you have the right permissions.
    - **status**: Filter applications by one or more statuses (e.g., `PENDING`, `APPROVED`, `REJECTED`).
    - **user_id**: Filter applications by a specific user ID.
    """
    is_privileged = False
    user_id_in_token = None
    if payload:
        user_roles = payload.get("roles", [])
        user_id_in_token = payload.get("userid")
        if set(user_roles) & {"ADMIN", "REPORTER"}:
            is_privileged = True
    if is_privileged:

        if status and public is None:
            status = [s.upper() for s in status]
            result = []
            for s in status:
                result.extend(applicationCrud.get_applications_all_by_status(session, s))
                
            return app_list_to_appResp_list(session, result)
            
        if status and not public:
            status = [s.upper() for s in status]
            result = []
            for s in status:
                result.extend(applicationCrud.get_applications_private_by_status(session, s))
            return app_list_to_appResp_list(session, result)
        
        elif status and public:
            status = [s.upper() for s in status]
            result = []
            for s in status:
                result.extend(applicationCrud.get_applications_public_by_status(session, s))
            return app_list_to_appResp_list(session, result)
        
        elif public is None:
            apps = applicationCrud.get_all_applications(session)
            return app_list_to_appResp_list(session, apps)
        
        elif public:
            apps = applicationCrud.get_all_public_applications(session)
            return app_list_to_appResp_list(session, apps)
        
        elif not public:
            apps = applicationCrud.get_all_private_applications(session)
            return app_list_to_appResp_list(session, apps)
    else:
        if status and public:
            status = [s.upper() for s in status]
            result = []
            for s in status:
                result.extend(applicationCrud.get_applications_public_by_status(session, s))
            return app_list_to_appResp_list(session, result)
        
        elif public:
            applications = applicationCrud.get_all_public_applications(session)
            return app_list_to_appResp_list(session, applications)
        
        else:
            result = applicationCrud.get_applications_by_user_id(session, user_id_in_token)
            return app_list_to_appResp_list(session, result)
        

@router.post("", response_model=ApplicationID,
            dependencies=[Depends(applicant_permission)],
            tags=["Applications"],
            summary="Create a new application")
async def create_application( application_data: ApplicationFillout,
                              session: Session = Depends(db.get_session_dep),
                              payload: Optional[dict] = Depends(deps.get_current_user_payload_optional)

                             ):
    """
    Create a new application in the system.
    """
    user_id = payload.get("userid") 
    if userCrud.get_user_by_id(user_id, session) == None:
        raise Exception("User not found")
    form_id = application_data.form_id
    jsonPayload = application_data.payload
    
    application = createApplication(user_id, form_id, jsonPayload, session)

    return ApplicationID(id=application.id)



@router.get("/{form_id}/{application_id}",
            response_model=ApplicationResponseItem,
            tags=["Applications"],
            summary="Get application by ID")
async def get_application(application_id: int, form_id: int, session: Session = Depends(db.get_session_dep)):
    """
    Retrieve a specific application by its ID.
    """
    try:
        form_id = int(form_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid form ID format")
    try:
        app_id = int(application_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid application ID format")

    application = applicationCrud.get_application_by_id(session, form_id, app_id)
    if not application:
        raise HTTPException(status_code=404, detail=f"Application with ID {app_id} in form {form_id} not found")
    app = ApplicationResponseItem(
            id=application.id,
            form_id=application.form_id,
            title=formCrud.get_form_by_id(session, application.form_id).form_name,
            status=application.status,
            created_at=application.created_at,
            is_public=application.is_public,
            currentSnapshotID=application.currentSnapshotID,
            previousSnapshotID=application.previousSnapshotID,
            jsonPayload=application.jsonPayload
            )
    app.title = formCrud.get_form_by_id(session, form_id).form_name
    
    return app

class CreationStatus(BaseModel):
    success: bool
    message: str


@router.put("/{application_id}", response_model=CreationStatus, tags=["Applications"], summary="Update an application by ID")

async def update_application(   application_update: ApplicationUpdate,
                                session: Session = Depends(db.get_session_dep),
                                payload: Optional[dict] = Depends(deps.get_current_user_payload_optional)
                                  ):
    """
    Update a specific application by its ID.
    """

    user_id = payload.get("userid")

    form_id = application_update.form_id
    application_id = application_update.application_id
    jsonPayload = application_update.payload # {1: {"label": "bla", "value": "blup"}}

    application = applicationCrud.get_application_by_id(session, form_id, application_id)

    if application.user_id != user_id:
        raise HTTPException(status_code=403, detail="Wrong user_id! Only the user who created an application may edit it!")

    try:
        applicationCrud.update_application(form_id, application_id, jsonPayload, session)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating application: {e}")
    return CreationStatus(success=True, message="Application updated successfully")


@router.delete("/{application_id}", tags=["Applications"], summary="Delete an application by ID")
async def delete_application(application_id: int):
    """
    Delete a specific application by its ID.
    """
    pass

