

from typing import Optional
from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from fastapi import Depends 

from backend.models.domain.application import ApplicationResponseItem
from backend.core import db
from backend.api import deps
from backend.crud.application import get_all_global_revisions_of_type, get_all_revisions_of_application, get_global_revisions
from backend.businesslogic.services.applicationService import app_list_to_appResp_list


router = APIRouter(prefix="/revisions", tags=["Revisions"])




@router.get("/", 
            response_model=list[ApplicationResponseItem],
            tags=["Revisions"],
            summary="Get all revisions for all applications")
async def get_all_revisions(
    session: Session = Depends(db.get_session_dep),
    form_id : Optional[int] = None,
    payload: Optional[dict] = Depends(deps.get_current_user_payload_optional)):
    is_privileged = False
    user_id_in_token = None
    if payload:
        user_roles = payload.get("roles", [])
        user_id_in_token = payload.get("userid")
        if set(user_roles) & {"ADMIN", "REPORTER"}:
            is_privileged = True
    if is_privileged:
        if form_id:
            response = []
            revisions = get_all_global_revisions_of_type(session, form_id)
            response = app_list_to_appResp_list(session, revisions)
            return response
        else:
            response = []
            revisions = get_global_revisions(session)
            response = app_list_to_appResp_list(session, revisions)
            return response
    else:
        raise HTTPException(status_code=403, detail="Not authorized to view global revisions")
    


@router.get("/{form_id}/{application_id}",
            response_model=list[ApplicationResponseItem], 
            tags=["Revisions"],
            summary="Get all revisions for an application by ID")
async def get_revisions(form_id: int,
                        application_id: int,
                        session: Session = Depends(db.get_session_dep),
                        payload: Optional[dict] = Depends(deps.get_current_user_payload_optional)):
    is_privileged = False
    user_id_in_token = None
    if payload:
        user_roles = payload.get("roles", [])
        user_id_in_token = payload.get("userid")
        if set(user_roles) & {"ADMIN", "REPORTER"}:
            is_privileged = True
        
        # check if the user id matches the user id of the application
        from backend.crud.application import get_application_by_id
        wanted_app = get_application_by_id(session, form_id, application_id)
        if wanted_app and wanted_app.user_id == user_id_in_token:
            is_privileged = True
        elif wanted_app and wanted_app.user_id != user_id_in_token:
            raise HTTPException(status_code=403, detail="Not authorized to view revisions of this application")
        else:
            raise HTTPException(status_code=404, detail="Application not found")
    if is_privileged:
        revisions = get_all_revisions_of_application(session, form_id, application_id)
        response = app_list_to_appResp_list(session, revisions)
        return response
    