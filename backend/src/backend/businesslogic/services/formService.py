
from ast import List
import datetime

from backend.models import (Form, User, UserType, Section, BuildingBlock)

# simple in-memory store for tests
_forms: list[Form] = []
_form_id_counter = 1

def _ensure_admin(user: User) -> None:
    if not user or user.user_type != UserType.ADMIN:
        raise PermissionError("admin required")

def createForm(admin: User, sections: list[Section]) -> Form:
    """Create a form (admin only). Forms consist of sections, which consist of building blocks."""
    global _form_id_counter
    _ensure_admin(admin) # only admin can create forms
    if not isinstance(sections, list) or not all(isinstance(s, Section) for s in sections): # type check
        raise ValueError("Forms must be a list of Section")
    form = Form(formID=_form_id_counter, sections=sections)
    _form_id_counter += 1 #temporary id generation for tests
    _forms.append(form)
    return form

def getForm(formID: int):
	""" Retrieves a form by its ID."""
	for form in _forms:
		if form.formID == formID:
			return form
	# Logic to retrieve the form from the database is not defined yet
	return None

def listForms():
	""" Lists all forms in the system."""
	return _forms
	# Logic to list all forms from the database is not defined yet
	

def importForm(form_data: dict):
	""" Imports a form from external data."""
	# Logic to import the form is not defined yet
	pass

def exportForm(formID: int):
	""" Exports a form to external data."""
	# Logic to export the form is not defined yet
	pass