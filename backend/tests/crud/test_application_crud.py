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

            applicationTableClass = dbActions.get_application_table_by_id(form.id)
            application = applicationTableClass(user_id = 1, form_id = Form1.id, label= "Hiya")

            dbActions.insertRow(session, applicationTableClass, application)

            applicationFromGetFunc = appCrud.get_application_by_id(session,form.id,1)

        assert application.label == applicationFromGetFunc.jsonPayload["1"]["value"]

def test_get_all_app_of_type():

        block1 = BuildingBlock(label="label", data_type=BBType.STRING, required=True, constraintsJson={})
        form1 = Form(id=1, form_name="formname", blocks= {"1":block1} )
        form1_json = form1.to_json()


        Form1 = OrmForm(form_name="Form 1", created_at=date.today(), is_active=True, xoev=form1_json)

        with db.get_session() as session:
            form = formCrud.add_orm_form(session, Form1)

            applicationTableClass = dbActions.get_application_table_by_id(form.id)
            application = applicationTableClass(user_id = 1, form_id = Form1.id, label= "Hiya")
            application2 = applicationTableClass(user_id = 1, form_id = Form1.id, label= "Hiya")


            dbActions.insertRow(session, applicationTableClass, application)
            assert len(appCrud.get_all_applications_of_type(session,form.id)) == 1
            dbActions.insertRow(session, applicationTableClass, application2)
            assert len(appCrud.get_all_applications_of_type(session,form.id)) == 2


            applicationsFromGetFunc = appCrud.get_all_applications_of_type(session,form.id)

        assert application.label == applicationsFromGetFunc[0].jsonPayload["1"]["value"]
        assert applicationsFromGetFunc[0].jsonPayload["1"]["value"] == applicationsFromGetFunc[1].jsonPayload["1"]["value"]
        assert applicationsFromGetFunc[0].form_id == applicationsFromGetFunc[1].form_id
        assert applicationsFromGetFunc[0].user_id == applicationsFromGetFunc[1].user_id



def test_insert_application_func():
     
        block1 = BuildingBlock(label="label", data_type=BBType.STRING, required=True, constraintsJson={})
        form1 = Form(id=1, form_name="Yoyoyo", blocks= {"1":block1} )
        form1_json = form1.to_json()


        Form1 = OrmForm(form_name="Yoyoyo", created_at=date.today(), is_active=True, xoev=form1_json)

        with db.get_session() as session:
            form = formCrud.add_orm_form(session, Form1)

            applicationTableClass = dbActions.get_application_table_by_id(form.id)
            application = Application(user_id= 1, form_id= Form1.id, jsonPayload={"1":{"label": "label", "value": "Hiya"}})
            application2 = Application(user_id= 1, form_id= Form1.id, jsonPayload={"1":{"label": "label", "value": "Hiya"}})

            applicationOrm = appCrud.insert_application(session, application)
            assert len(appCrud.get_all_applications_of_type(session,form.id)) == 1
            applicationOrm2 = appCrud.insert_application(session, application2)
            assert len(appCrud.get_all_applications_of_type(session,form.id)) == 2

            applicationFromOrm = appCrud.rowToApplication(applicationOrm, applicationTableClass)
            applicationFromOrm2 = appCrud.rowToApplication(applicationOrm2, applicationTableClass)

            assert application.user_id == applicationFromOrm.user_id
            assert application.form_id == applicationFromOrm.form_id
            assert application.jsonPayload["1"]["value"] == applicationFromOrm.jsonPayload["1"]["value"]

            assert application2.user_id == applicationFromOrm2.user_id
            assert application2.form_id == applicationFromOrm2.form_id
            assert application2.jsonPayload["1"]["value"] == applicationFromOrm2.jsonPayload["1"]["value"]

            assert application.id == None
            assert applicationFromOrm.id == 1
            assert applicationFromOrm.id == applicationFromOrm.currentSnapshotID
            assert application2.id == None
            assert applicationFromOrm2.id == 2
            assert applicationFromOrm2.id == applicationFromOrm2.currentSnapshotID

def test_update_application():
     with db.get_session() as session:
        assert len(appCrud.get_all_applications(session)) == 5
        assert len(formCrud.get_all_forms(session)) == 3
        assert len(appCrud.get_all_applications_of_type(session, 3)) == 2

        appCrud.update_application(3, 1, {"1":{"label": "label", "value": "Hohoho"}}, session)
        newApp = appCrud.get_application_by_id(session, 3, 3)
        assert newApp.previousSnapshotID == 1
        assert newApp.jsonPayload["1"]["value"] == "Hohoho"
        assert appCrud.get_application_by_id(session, 3, 1).currentSnapshotID == 3
        


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

