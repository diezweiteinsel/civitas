import os
from importlib import reload # for reloading modules


from testcontainers.postgres import PostgresContainer
from backend.api.endpoints.user import router
from fastapi import FastAPI
import pytest


from backend import dbActions
from backend import db
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
    os.environ["DB_PORT"] = str(postgres.get_exposed_port(5432))
    os.environ["DB_USERNAME"] = str(postgres.username)
    os.environ["DB_PASSWORD"] = str(postgres.password)
    os.environ["DB_NAME"] = str(postgres.dbname)
    os.environ["DEV_SQLITE"] = "0" # ensure not using sqlite for tests
    reload(db)
    reload(dbActions)
    user_db_setup()  # Ensure tables are created before tests run

app = FastAPI()
app.include_router(router)

client = TestClient(app)

def test_create_user_success():
    payload = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "securepassword",
        "role": "APPLICANT"
    }
    response = client.post("/users", json=payload)
    assert response.status_code == 201
    assert "id" in response.json()