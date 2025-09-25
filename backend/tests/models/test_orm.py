
import pytest
import os
from datetime import date

from testcontainers.postgres import PostgresContainer
from sqlalchemy import Column, Integer, String, select, inspect

from backend import dbActions
from backend import db
from backend.models.orm.base import Base
from backend.models.orm.usertable import OrmUser
from backend.models.orm import usertable
from backend.core import ormUtil
from backend.models.domain import user
from backend.crud import userCrud

# this file might be obsolete now -ps

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
    os.environ["DEV_SQLITE"] = "0" # ensure not using sqlite for tests







