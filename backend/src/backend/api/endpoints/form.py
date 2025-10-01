# standard library imports
from datetime import datetime
from backend.models.orm.formtable import OrmForm
from pydantic import BaseModel

# third party imports
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

# project imports
from backend.models.domain.form import Form, FormCreate
from backend.crud import dbActions, formCrud
from backend.api.deps import RoleChecker
from backend.core import db

admin_permission = RoleChecker(["ADMIN"])

router = APIRouter(prefix="/forms", tags=["forms"])

@router.get("", response_model=list[Form], tags=["Forms"], summary="List all forms") #TODO: Once UI is ready, implement Admin guard
async def list_forms(session: Session = Depends(db.get_session_dep)):
  forms_list = formCrud.get_all_forms(session)
  forms = [Form.from_orm_model(orm_form) for orm_form in forms_list]
  return forms


@router.get("/{form_id}",
            response_model=Form,
            tags=["Forms"],
            summary="Get form by ID")
async def get_form(form_id: int,
                  returnAsXml: bool = False,
                  session: Session = Depends(db.get_session_dep)):
  
  ormForm = formCrud.get_form_by_id(session, form_id)
  # if returnAsXml:
  #   form = FormXML.from_orm_model(ormForm)
  #   return form
  form = Form.from_orm_model(ormForm)
  return form


class CreationStatus(BaseModel):
    success: bool
    message: str

@router.post("", response_model=CreationStatus, tags=["Forms"], summary="Create a new form", dependencies=[Depends(admin_permission)])
async def create_form(formCreate: FormCreate, session: Session = Depends(db.get_session_dep)):
  form = formCreate.toForm()
  form_db = formCrud.add_form(session, form)
  if form.form_name == form_db.form_name and form.blocks == form_db.blocks:
    return CreationStatus(success=True, message="Form created successfully")
  else:
    return CreationStatus(success=False, message="Form creation failed")
  


# explicitly no PUT method, forms are immutable after creation

@router.delete("/{form_id}", tags=["Forms"], summary="Delete a form by ID")
async def delete_form(form_id: int, session: Session = Depends(db.get_session_dep)):
  dbActions.updateRow(session, OrmForm, {"id": form_id, "is_active": False}) # Sets is_active in the given form to False
  return dbActions.getRowById(session, OrmForm, form_id).is_active == False # Should hopefully, maybe, possibly, potentially check if given form.is_active == False 



