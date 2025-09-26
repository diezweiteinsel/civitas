
from ast import List
import datetime

from backend.models import (Form, User, UserType, Section, BuildingBlock)
from backend.businesslogic.buildingblock import createBuildingBlockFromDictionary, createDictionaryFromBuildingBlock
from backend.businesslogic.user import ensure_admin

# simple in-memory store for tests
_forms: list[Form] = []
_form_id_counter = 1


def createForm(admin: User, sections: list[Section]) -> Form:
    """Create a form (admin only). Forms consist of sections, which consist of building blocks."""
    global _form_id_counter
    if not ensure_admin(admin): # only admin can create forms
        raise PermissionError("Only admins can create forms.")
	
    if not isinstance(sections, list) or not all(isinstance(s, Section) for s in sections): # type check
        raise ValueError("Forms must be a list of Section")
    form = Form(formID=_form_id_counter, sections=sections)
    _form_id_counter += 1 #temporary id generation for tests
    _forms.append(form)
	# Logic to save the form to the database is not defined yet
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
	

def importForm(admin: User, form_data: dict):
	""" Imports a form from external data. Admins only and they process the 
	imported forms manually via adding or deleting sections and building blocks."""
	ensure_admin(admin) # only admin can import forms

	form = createForm(admin, sections=[])
	global _form_id_counter
	form.formID = _form_id_counter
	_form_id_counter += 1
	_forms.append(form)

	for section_data in form_data.get("sections", []):
		section = Section(	
			id=section_data.get("id", -1),
			name=section_data.get("name", ""),
			blocks=[createBuildingBlockFromDictionary(bb) for bb in section_data.get("blocks", [])]
		)
		form.sections.append(section)
	return form

	# Logic to save the form to the database is not defined yet
	

def exportForm(formID: int):
	""" Exports a form to external data."""
	# Logic to export the form is not defined yet
	pass