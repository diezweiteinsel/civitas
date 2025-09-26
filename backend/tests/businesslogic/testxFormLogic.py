"""testing form logic and operations"""
import pytest
from backend.models import (User, UserType, Section, BuildingBlock, BBType)
from backend.businesslogic.services.formService import createForm, _forms, _form_id_counter
from datetime import date
from backend.businesslogic.user import assign_role
from backend.businesslogic.selfRegistration import register_Applicant

admin=User(id=1, username="admin", date_created=date.today(), hashed_password="hashed")
assign_role(admin, UserType.ADMIN)
applicant=register_Applicant("applicant1", "password1")

def test_create_form():
    """Test creating a form with sections and building blocks."""
    global _forms, _form_id_counter
    _forms.clear()
    _form_id_counter = 1

    # Create some building blocks
    bb1 = BuildingBlock(id=1, key="name", label="Name", dataType=BBType.STRING, required=True, order=1)
    bb2 = BuildingBlock(id=2, key="age", label="Age", dataType=BBType.INTEGER, required=False, order=2)

    # Create a section with the building blocks
    section = Section(id=1, name="Personal Information", blocks=[bb1, bb2])

    # Create a form with the section
    form = createForm(admin, sections=[section])

    assert form.formID == 1
    assert len(form.sections) == 1
    assert form.sections[0].name == "Personal Information"
    assert len(form.sections[0].blocks) == 2
    assert form.sections[0].blocks[0].label == "Name"
    assert form.sections[0].blocks[1].label == "Age"
    assert len(_forms) == 1
    assert _forms[0].formID == 1
    with pytest.raises(PermissionError):
        createForm(applicant, sections=[section])
    form2 = createForm(admin, sections=[section])
    assert form2.formID == 2
test_create_form()

section=Section(id=1, name="Personal Information", blocks=[
    BuildingBlock(id=1, key="name", label="Name", dataType=BBType.STRING, required=True, order=1),
    BuildingBlock(id=2, key="age", label="Age", dataType=BBType.INTEGER, required=False, order=2)
])

createForm(admin, sections=[section])
createForm(admin, sections=[section])
def test_list_forms():
    """Test listing all forms."""
    forms = _forms
    assert len(forms) == 4  # from previous test and two here
    assert forms[0].formID == 1
    assert forms[1].formID == 2
    assert forms[2].formID == 3
    assert forms[3].formID == 4

test_list_forms()

def test_get_form():
    """Test retrieving a form by ID."""
    form = None
    for f in _forms:
        if f.formID == 2:
            form = f
            break
    assert form is not None
    assert form.formID == 2
    assert len(form.sections) == 1
    assert form.sections[0].name == "Personal Information"
    assert len(form.sections[0].blocks) == 2
    assert form.sections[0].blocks[0].label == "Name"
    assert form.sections[0].blocks[1].label == "Age"

test_get_form()
