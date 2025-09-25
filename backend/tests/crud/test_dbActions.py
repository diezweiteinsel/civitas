import pytest
import os
from importlib import reload # for reloading modules

from testcontainers.postgres import PostgresContainer
from sqlalchemy import Column, Integer, String, select

from backend import dbActions
from backend import db


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


def test_createTableClass():
    tableName = "create_table_test"
    columns = {"id": Column(Integer, primary_key=True), "name": Column(String)}

    TableClass = dbActions.createTableClass(tableName, columns) # create the class
    TableClass.metadata.create_all(db.engine)  # Create the table in the DB
    Base = db.get_base( reload=True) # reload to reflect new table
    assert TableClass.__tablename__ == tableName
    assert hasattr(TableClass, "id")
    assert hasattr(TableClass, "name")
    assert isinstance(TableClass.id.type, Integer)
    assert isinstance(TableClass.name.type, String)

def test_insertRow():
    # Ensure the table class is created and table exists in DB
    tableName = "test_table"
    columns = {"id": Column(Integer, primary_key=True), "name": Column(String)}

    TableClass = dbActions.createTableClass(tableName, columns) # create the class
    TableClass.metadata.create_all(db.engine)  # Create the table in the DB

    # Reflect the table using automap
    Base = db.get_base(reload=True)
    tableClassFromBase = Base.classes.get(tableName)
    assert tableClassFromBase is not None, f"Table class {tableName} not found in Base.classes"

    # Insert a row
    rowData = {"name": "Test Name"}
    with db.get_session() as session:
        dbActions.insertRow(session, tableClassFromBase, rowData)

    # Query to verify the row was inserted
    with db.engine.connect() as conn:
        result = conn.execute(select(tableClassFromBase)).fetchall()
    assert len(result) == 1
    assert result[0].name == "Test Name"

def test_updateRow():

    Base = db.get_base(reload=True)
    tableClassFromBase = Base.classes.get("test_table")
    assert tableClassFromBase is not None, f"Table class {"test_table"} not found in Base.classes"

    # Insert a row and update it
    rowData = {"name": "Jane"}
    with db.get_session() as session:
        dbActions.insertRow(session, tableClassFromBase, rowData)

        dbActions.updateRow(session, tableClassFromBase, {"id": 2, "name": "Remover"})

    # Query to verify the row was inserted and updated
    with db.engine.connect() as conn:
        result = conn.execute(select(tableClassFromBase)).fetchall()
    assert len(result) == 2
    assert result[1].name == "Remover"

def test_removeRow():

    Base = db.get_base(reload=True)
    tableClassFromBase = Base.classes.get("test_table")
    assert tableClassFromBase is not None, f"Table class {"test_table"} not found in Base.classes"

    # Delete a row
    id = 2
    with db.get_session() as session:
        dbActions.removeRow(session, tableClassFromBase, id)

    # Query to verify the row was deleted
    with db.engine.connect() as conn:
        result = conn.execute(select(tableClassFromBase)).fetchall()
    assert len(result) == 1
    with pytest.raises(IndexError):
        result[1] == None

def test_getRowById():
    Base = db.get_base(reload=True)
    tableClassFromBase = Base.classes.get("test_table")
    assert tableClassFromBase is not None, f"Table class {"test_table"} not found in Base.classes"

    # Get a row by ID
    id = 1
    with db.get_session() as session:
        obj = dbActions.getRowById(session, tableClassFromBase, id)
    assert obj is not None
    assert obj.id == 1
    assert obj.name == "Test Name"

def test_getRows():
    Base = db.get_base(reload=True)
    Base.metadata.drop_all(bind=db.engine)  # Clean up before test
    Base.metadata.create_all(bind=db.engine)  # Create tables
    tableClassFromBase = Base.classes.get("test_table")
    assert tableClassFromBase is not None, f"Table class {"test_table"} not found in Base.classes"

    # Add more rows
    with db.get_session() as session:
        dbActions.insertRow(session, tableClassFromBase, {"name": "Spongebob"})
        dbActions.insertRow(session, tableClassFromBase, {"name": "Patrick"})
        dbActions.insertRow(session, tableClassFromBase, {"name": "Mr. Krabs"})
        dbActions.insertRow(session, tableClassFromBase, {"name": "Gary"})

    # Get all rows
    with db.get_session() as session:
        objs = dbActions.getRows(session, tableClassFromBase)
    assert len(objs) == 4
    assert objs[0].id == 1
    assert objs[0].name == "Spongebob"
    assert objs[1].id == 2
    assert objs[1].name == "Patrick"

def test_getRowsByFilter():
    Base = db.get_base(reload=True)
    tableClassFromBase = Base.classes.get("test_table")
    assert tableClassFromBase is not None, f"Table class {"test_table"} not found in Base.classes"

    # Get rows by filter
    filterDict = {"name": "Gary"}
    with db.get_session() as session:
        objs = dbActions.getRowsByFilter(session, tableClassFromBase, filterDict)
    assert len(objs) == 1
    assert objs[0].id == 4
    assert objs[0].name == "Gary"



if __name__ == "__main__":
    # test_createTableClass()
    test_insertRow()
    test_updateRow()
    test_removeRow()
    test_getRowById()
    test_getRows()
    test_getRowsByFilter()
