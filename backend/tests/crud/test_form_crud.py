from datetime import date
import os
from importlib import reload # for reloading modules

from backend.models.domain.buildingblock import BBType, BuildingBlock
from backend.models.domain.form import Form
from testcontainers.postgres import PostgresContainer
import pytest

from backend import dbActions
from backend import db
from backend.core.ormUtil import user_db_setup
from backend.models.domain import user
from backend.crud import roleCrud
from backend.models.orm.formtable import OrmForm
from backend.crud import formCrud

postgres = PostgresContainer("postgres:15-alpine")

@pytest.fixture(scope="module", autouse=True)
def setup(request):
    postgres.start()

    def remove_container():
        postgres.stop()

    request.addfinalizer(remove_container)
    os.environ["DB_CONN"] = str(postgres.get_connection_url())
    os.environ["DB_HOST"] = str(postgres.get_container_host_ip())
    os.environ["DB_PORT"] = str(postgres.get_exposed_port(5432))
    os.environ["DB_USERNAME"] = str(postgres.username)
    os.environ["DB_PASSWORD"] = str(postgres.password)
    os.environ["DB_NAME"] = str(postgres.dbname)
    os.environ["DEV_SQLITE"] = "0" # ensure not using sqlite for tests
    reload(db)
    reload(dbActions)
    user_db_setup()  # Ensure tables are created before tests run




def test_add_and_getById_func():
    Base = db.get_base(reload=True)  # Ensure we have the latest Base
    Base.metadata.drop_all(bind=db.engine) # Clean up before test
    Base.metadata.clear()  # löscht alle Tabellen, die bisher registriert wurden, in memory not db
    user_db_setup()  

    with db.get_session() as session:
        # Create table if not exists
        # OrmUser.__table__.create(bind=session.get_bind(), checkfirst=True)

        block1 = BuildingBlock(label="label", data_type=BBType.STRING, required=True, constraintsJson={})
        form1 = Form(id=1, form_name="formname", blocks= {"1":block1} )
        form1_json = form1.to_json()


        Form1 = OrmForm(form_name="Form 1", created_at=date.today(), is_active=True, xoev=form1_json)

        # Insert a form
        form = formCrud.add_orm_form(session, Form1)
        ormFormRows = dbActions.getRows(session, OrmForm)
        assert len(ormFormRows) == 1

        # Try to get the form by id
        fetchedForm = formCrud.get_form_by_id(session, form.id)
        assert fetchedForm is not None
        assert fetchedForm.id == form.id
        assert fetchedForm.form_name == form.form_name
        assert fetchedForm.created_at == form.created_at
        assert fetchedForm.is_active == form.is_active
        assert fetchedForm.xoev == form.xoev

        # Try to get a non-existent form by id
        with pytest.raises(Exception) as exc_info:
            nonExistentForm = formCrud.get_form_by_id(session, 9999)
            assert nonExistentForm is None

def test_get_all_forms_func():
    Base = db.get_base(True)
    Base.metadata.drop_all(bind=db.engine)   # alle Tabellen löschen in db
    Base.metadata.clear()  # löscht alle Tabellen, die bisher registriert wurden, in memory not db
    user_db_setup()

    with db.get_session() as session:
        block1 = BuildingBlock(label="label", data_type=BBType.STRING, required=True, constraintsJson={})

        form1 = Form(id=1, form_name="formname", blocks= {"1":block1} )
        form2 = Form(id=2, form_name="formname", blocks= {"1":block1} )
        form3 = Form(id=3, form_name="formname", blocks= {"1":block1} )


        form1_json = form1.to_json()
        form2_json = form2.to_json()
        form3_json = form3.to_json()


        # Insert multiple forms
        OrmForm1 = OrmForm(form_name="Form 1", created_at=date.today(), is_active=True, xoev=form1_json)
        OrmForm2 = OrmForm(form_name="Form 2", created_at=date.today(), is_active=False, xoev=form2_json)
        OrmForm3 = OrmForm(form_name="Form 3", created_at=date.today(), is_active=True, xoev=form3_json)

        formCrud.add_orm_form(session, OrmForm1)
        formCrud.add_orm_form(session, OrmForm2)
        formCrud.add_orm_form(session, OrmForm3)

        # Fetch all forms
        allForms = formCrud.get_all_forms(session)
        assert len(allForms) == 3
        table_names = [form.form_name for form in allForms]
        assert table_names == ["Form 1", "Form 2", "Form 3"]
        Base = db.get_base(reload=True)
        alltables = Base.metadata.tables

        assert len(alltables) == 6

