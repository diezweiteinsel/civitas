from backend.models.orm.base import Base
from fastapi import HTTPException
from sqlalchemy import Table
from backend.crud import dbActions
from backend.models.orm.formtable import OrmForm
from backend.models.domain.form import Form

def get_all_forms(session) -> list:
    """
    Returns a list containing all form ORM instances.
    """
    return dbActions.getRows(session, OrmForm)

def add_orm_form(session, form: OrmForm) -> OrmForm:
    """
    Adds a new form to the database.
    """
    return dbActions.insertRow(session, OrmForm, form)


def add_form(session, form:Form) -> Form:
    ormForm = form.to_orm_model()
    ormForm = add_orm_form(session, ormForm)
    updatedForm = Form.from_orm_model(ormForm)
    dbActions.updateRow(session, OrmForm, {"id": ormForm.id, "xoev":updatedForm.to_json()})
    return updatedForm

def get_form_by_id(session, id: int) -> OrmForm:
    """
    Retrieves a form by its ID.
    Raises HTTPException if not found.
    """
    result = dbActions.getRowById(session, OrmForm, id)
    if result:
        orm_form = result
        return orm_form
    raise HTTPException(status_code=404, detail="Form not found")