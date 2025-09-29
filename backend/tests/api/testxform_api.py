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


def test_create_form_api():
    pass