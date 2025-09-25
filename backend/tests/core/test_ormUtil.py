import os
from importlib import reload # for reloading modules


import pytest
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import declarative_base
from testcontainers.postgres import PostgresContainer

from backend.core import db
from backend.core.ormUtil import user_db_setup

postgres = PostgresContainer("postgres:15-alpine")


@pytest.fixture(scope="module", autouse=True)
def setup(request):
    postgres.start()

    def remove_container():
        postgres.stop()

    request.addfinalizer(remove_container)
    os.environ["DB_CONN"] = str(postgres.get_connection_url())
    os.environ["DB_HOST"] = str(postgres.get_container_host_ip())
    os.environ["DB_PORT"] = str(postgres.get_exposed_port("5432"))
    os.environ["DB_USERNAME"] = str(postgres.username)
    os.environ["DB_PASSWORD"] = str(postgres.password)
    os.environ["DB_NAME"] = str(postgres.dbname)
    os.environ["DEV_SQLITE"] = "0"  # ensure not using sqlite for tests
    reload(db)


def test_user_db_setup():
    """
    Test the user_db_setup function to ensure it creates the user_table and role_assignment tables.
    """
    Base = db.get_base(reload=True)  # Ensure we have the latest Base
    # Drop all tables to ensure a clean slate
    Base.metadata.drop_all(bind=db.engine)

    # Call the user_db_setup function
    user_db_setup()

    # Use SQLAlchemy's inspector to check if the tables exist
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()

    # print the current engine URL for debugging
    print(f"Current engine URL: {db.engine.url}")

    # assert the engine URL is the testcontainer URL
    #assert db.engine.url == postgres.get_connection_url()

    # Assert that the tables were created
    assert "user_table" in tables, "user_table was not created"
    assert "role_assignment" in tables, "role_assignment table was not created"

    # Check the columns of the user_table
    user_table_columns = inspector.get_columns("user_table")
    user_table_column_names = {col["name"] for col in user_table_columns}
    assert user_table_column_names == {
        "id",
        "user_name",
        "creation_date",
        "email",
        "password",
        "is_active",
    }, "user_table schema is incorrect"

    # Check the columns of the role_assignment table
    role_assignment_columns = inspector.get_columns("role_assignment")
    role_assignment_column_names = {col["name"] for col in role_assignment_columns}
    assert role_assignment_column_names == {
        "id",
        "user_id",
        "assignment_date",
        "role",
    }, "role_assignment schema is incorrect"

    # cleanup
    Base.metadata.drop_all(bind=db.engine)




