from datetime import date
import os
from importlib import reload # for reloading modules
import xmltodict
import re


from backend.models.orm.formtable import OrmForm
import pytest
from testcontainers.postgres import PostgresContainer




from backend import dbActions
from backend import db
from backend.core.ormUtil import user_db_setup
from backend.models.domain.form import Form
from backend.models.domain.buildingblock import BBType, BuildingBlock
from backend.crud import form as formCrud


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




def test_form_json_conversion():

    block1 = BuildingBlock(label="label", data_type=BBType.STRING, required=True, constraintsJson={})

    form1 = Form(id=None, form_name="formname", blocks= {"1":block1} )

    form1_json = form1.to_json()

    form1_from_json = Form.from_json(form1_json)

    print(form1_json)

    assert form1 == form1_from_json

def test_form_xlm_conversion():
	blocks = {
		1: BuildingBlock(label="helpme", data_type=BBType.STRING, required=True, constraintsJson={}),
		2: BuildingBlock(label="helpme1", data_type=BBType.INTEGER, required=True, constraintsJson={}),
		3: BuildingBlock(label="helpme2", data_type=BBType.DATE, required=True, constraintsJson={}),
	}
	example_form = Form(form_name="example", blocks=blocks, version="6.9")
	xml: str = example_form.to_xml()

	#match = re.search(r'(<formDefinition (.*?)</formDefinition>)', xml, re.DOTALL)
	#print(xml)
	#print(xmltodict.parse(xml))
	#print(match)
	#print("XML TESTING: " + str(xmltodict.parse(match[0])))

	assert(xml == Form.from_xml(xml).to_xml())


def test_form_to_orm():

    block1 = BuildingBlock(label="label", data_type=BBType.STRING, required=True, constraintsJson={})

    form1 = Form(id=1, form_name="formname", blocks= {"1":block1} )

    ormForm1 = form1.to_orm_model()

    form1_from_orm = Form.from_orm_model(ormForm1)

    assert form1.form_name == form1_from_orm.form_name
    assert form1.blocks == form1_from_orm.blocks


def test_form_to_db():

    Base = db.get_base(True)
    Base.metadata.drop_all(bind=db.engine)   # alle Tabellen löschen in db
    Base.metadata.clear()  # löscht alle Tabellen, die bisher registriert wurden, in memory not db
    user_db_setup()

    block1 = BuildingBlock(label="label", data_type=BBType.STRING, required=True, constraintsJson={})

    form1 = Form(form_name="formname", blocks= {"1":block1} )

    ormForm1 = form1.to_orm_model()

    with db.get_session() as session:

        assert len(dbActions.getRows(session, OrmForm)) == 0

        Base = db.get_base(True)
        assert len(Base.metadata.tables) == 3

        form1_from_DB = formCrud.add_form(session, form1)

        ormForm1_from_DB = formCrud.get_form_by_id(session, 1)

        allOrm_from_DB = formCrud.get_all_forms(session)

    assert len(allOrm_from_DB) == 1

    assert form1.form_name == form1_from_DB.form_name
    assert form1.blocks == form1_from_DB.blocks
    assert form1_from_DB.id == 1

    assert ormForm1.form_name == ormForm1_from_DB.form_name
    assert ormForm1_from_DB.xoev == form1_from_DB.to_json()
    assert ormForm1_from_DB.created_at == date.today()
    assert Form.from_orm_model(ormForm1_from_DB) == form1_from_DB





# Execute this file directly to see how the json looks
if __name__ == "__main__":

    block1 = BuildingBlock(label="label", data_type=BBType.STRING, required=True, constraintsJson={})
    form1 = Form(id=1, form_name="formname", blocks= {"1":block1} )
    form1_json = form1.to_json()

    print(form1_json)

    test_form_xlm_conversion()