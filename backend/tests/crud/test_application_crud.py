from datetime import date
import os
from importlib import reload # for reloading modules

from backend.models.domain.application import Application
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
from backend.crud import application as appCrud

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


def test_get_application_by_id_func():
        
        block1 = BuildingBlock(label="label", data_type=BBType.STRING, required=True, constraintsJson={})
        form1 = Form(id=1, form_name="formname", blocks= {"1":block1} )
        form1_json = form1.to_json()


        Form1 = OrmForm(form_name="Form 1", created_at=date.today(), is_active=True, xoev=form1_json)

        with db.get_session() as session:
            form = formCrud.add_orm_form(session, Form1)

            pydantic_application = Application(
            user_id=1,
            form_id=form.id,
            jsonPayload={"1": {"label": "label", "value": "Hiya"}}
        )

        created_orm_app = appCrud.insert_application(session, pydantic_application)

        applicationFromGetFunc = appCrud.get_application_by_id(session, form.id, created_orm_app.id)

        assert pydantic_application.jsonPayload["1"]["value"] == applicationFromGetFunc.jsonPayload["1"]["value"]

def test_get_all_app_of_type():

        block1 = BuildingBlock(label="label", data_type=BBType.STRING, required=True, constraintsJson={})
        form1 = Form(id=1, form_name="formname", blocks= {"1":block1} )
        form1_json = form1.to_json()


        Form1 = OrmForm(form_name="Form 1", created_at=date.today(), is_active=True, xoev=form1_json)

        with db.get_session() as session:
            form = formCrud.add_orm_form(session, Form1)

            application = Application(
                user_id=1,
                form_id=form.id,
                jsonPayload={"1": {"label": "label", "value": "Hiya"}}
            )
            application2 = Application(
                user_id=1,
                form_id=form.id,
                jsonPayload={"1": {"label": "label", "value": "Hiya"}}
            )

            appCrud.insert_application(session, application)
            assert len(appCrud.get_all_applications_of_type(session,form.id)) == 1
            appCrud.insert_application(session, application2)
            assert len(appCrud.get_all_applications_of_type(session,form.id)) == 2


            applicationsFromGetFunc = appCrud.get_all_applications_of_type(session,form.id)

        assert application.jsonPayload["1"]["value"] == applicationsFromGetFunc[0].jsonPayload["1"]["value"]
        assert applicationsFromGetFunc[0].jsonPayload["1"]["value"] == applicationsFromGetFunc[1].jsonPayload["1"]["value"]
        assert applicationsFromGetFunc[0].form_id == applicationsFromGetFunc[1].form_id
        assert applicationsFromGetFunc[0].user_id == applicationsFromGetFunc[1].user_id



def test_insert_application_func():
    block1 = BuildingBlock(label="label", data_type=BBType.STRING, required=True, constraintsJson={})
    form_domain = Form(id=1, form_name="Yoyoyo", blocks={"1": block1})
    form_orm_obj = OrmForm(form_name="Yoyoyo", created_at=date.today(), is_active=True, xoev=form_domain.to_json())

    with db.get_session() as session:
        # 1. Create the form and get its real, database-assigned ID
        form = formCrud.add_orm_form(session, form_orm_obj)
        session.commit()
        session.refresh(form)
        
        # 2. Use the correct form.id from the database
        application1 = Application(user_id=1, form_id=form.id, jsonPayload={"1": {"label": "label", "value": "Hiya"}})
        application2 = Application(user_id=1, form_id=form.id, jsonPayload={"1": {"label": "label", "value": "Hiya again"}})

        # 3. Insert the applications
        orm_app1 = appCrud.insert_application(session, application1)
        session.commit() # Commit after each insert to finalize the transaction
        orm_app2 = appCrud.insert_application(session, application2)
        session.commit()

        assert len(appCrud.get_all_applications_of_type(session, form.id)) == 2

        # 4. Convert back to Pydantic models to check values
        pydantic_app1 = appCrud.rowToApplication(orm_app1)
        pydantic_app2 = appCrud.rowToApplication(orm_app2)

        # 5. Assertions are now robust and access the model correctly
        assert pydantic_app1.id is not None
        assert -1 == pydantic_app1.snapshots.currentSnapshotID # Correct access

        assert pydantic_app2.id is not None
        assert pydantic_app2.id > pydantic_app1.id # Don't assume ID=2, just that it's greater
        assert -1 == pydantic_app2.snapshots.currentSnapshotID # Correct access

def test_update_application():
    # --- 1. Setup: Create the necessary data for this test ---
    block1 = BuildingBlock(label="label", data_type=BBType.STRING, required=True, constraintsJson={})
    form_domain = Form(id=1, form_name="UpdateTestForm", blocks={"1": block1})
    form_orm_obj = OrmForm(form_name="UpdateTestForm", created_at=date.today(), is_active=True, xoev=form_domain.to_json())

    with db.get_session() as session:
        # Create a form specifically for this test
        form = formCrud.add_orm_form(session, form_orm_obj)
        session.commit()
        session.refresh(form)
        
        # Create an initial application to be updated
        initial_application = Application(
            user_id=1,
            form_id=form.id,
            jsonPayload={"1": {"label": "label", "value": "Original Value"}}
        )
        original_orm_app = appCrud.insert_application(session, initial_application)
        session.commit()
        session.refresh(original_orm_app)
        
        original_app_id = original_orm_app.id

        # --- 2. Action: Perform the update ---
        updated_payload = {"1": {"label": "label", "value": "Hohoho"}}
        # The update function should return the new ORM object
        new_orm_app = appCrud.update_application(form.id, original_app_id, updated_payload, session)
        session.commit()
        session.refresh(new_orm_app)
        
        new_app_id = new_orm_app.id

        # --- 3. Assertions: Verify the results ---
        # Convert the final state of the ORM objects back to Pydantic models
        original_app_final_state = appCrud.get_application_by_id(session, form.id, original_app_id)
        new_app_final_state = appCrud.get_application_by_id(session, form.id, new_app_id)

        # Check the snapshot chain
        assert new_app_final_state.snapshots.previousSnapshotID == original_app_id
        assert original_app_final_state.snapshots.nextSnapshotID == new_app_id
        
        # Check the values
        assert new_app_final_state.jsonPayload["1"]["value"] == "Hohoho"
        assert original_app_final_state.jsonPayload["1"]["value"] == "Original Value" # Should be unchanged
        


if __name__ == "__main__":

    # Remnants of my mental breakdown

    user_db_setup()  # Ensure tables are created before tests run


    block1 = BuildingBlock(label="label", data_type=BBType.STRING, required=True, constraintsJson={})
    form1 = Form(id=None, form_name="formname", blocks= {"1":block1} )
    form1_json = form1.to_json()
    Form1 = OrmForm(form_name="Form 1", created_at=date.today(), is_active=True, xoev=form1_json)

    with db.get_session() as session:
        form = formCrud.add_orm_form(session, Form1)

        print(form.id)
        print(form.xoev)

        Base = db.get_base()

        print("All table classes: \n")
        for name, cls in Base.classes.items():
            print(name, cls)

        print("All tables: \n")
        for table_name, table in Base.metadata.tables.items():
            print(table_name, table)


        print("All columns in the form_1 table: \n")
        table = Base.metadata.tables["form_1"]

        for column in table.columns:
            print(column.name, column.type)

        applicationTableClass = dbActions.get_application_table_by_id(form.id)
        application = applicationTableClass(user_id = 1, form_id = Form1.id, label= "Hiya")
        dbActions.insertRow(session, applicationTableClass, application)

        applicationRow = dbActions.getRowById(session=session, tableClass=applicationTableClass, id=1)
        print("row: ", applicationRow)
        for column in applicationRow.__table__.columns:
            print(column.name, getattr(applicationRow, column.name))
        print("ACHTUNG: ", appCrud.getRowJsonPayload(applicationTableClass, applicationRow))
        application = applicationTableClass(user_id = 1, form_id = Form1.id, label= "Hiya")

        dbActions.insertRow(session, applicationTableClass, application)

