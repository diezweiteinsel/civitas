# standard library imports
from datetime import datetime

# third party imports
from fastapi import APIRouter

# project imports
from backend.models.domain.form import Form, FormCreate
from backend.crud import formCrud


router = APIRouter(prefix="/forms", tags=["forms"])

@router.get("", response_model=list[Form], tags=["Forms"], summary="List all forms")
async def list_forms():
  pass


@router.get("/{form_id}",
            response_model=Form,
            tags=["Forms"],
            summary="Get form by ID")
async def get_form(form_id: int,
                  returnAsXml: bool = False):
  pass

# "/api/v1/forms/{form_id}?returnAsXml=true"

@router.post("", response_model=Form, tags=["Forms"], summary="Create a new form")
async def create_form(formCreate: FormCreate):
  form = formCreate.toForm()
  form_db = formCrud.add_form(form)
  if form.form_name == form_db.form_name and form.blocks == form_db.blocks:
    return True
  else:
    return False

# explicitly no PUT method, forms are immutable after creation

@router.delete("/{form_id}", tags=["Forms"], summary="Delete a form by ID")
async def delete_form(form_id: int):
  pass



