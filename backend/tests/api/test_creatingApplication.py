from importlib import reload # for reloading modules
import os
from backend.api.endpoints import auth
from backend.core import db
from backend.core.ormUtil import user_db_setup
from backend.crud import dbActions
from backend.models.domain.buildingblock import BuildingBlock
from fastapi.testclient import TestClient
from backend.api.endpoints.application import router
from backend.businesslogic.services.adminService import createUser
from fastapi import FastAPI
import pytest
from backend.businesslogic.services.mockups import _global_users_db, _global_applications_db, _global_forms_db
from testcontainers.postgres import PostgresContainer

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
app.include_router(router, prefix="/api/v1")
app.include_router(auth.router, prefix="/api/v1")

client = TestClient(app)

def test_create_application_success():
    user_id = 1  # Assuming a user with ID 1 exists
    form_id = 1  # Assuming a form with ID 1 exists
    #bb = BuildingBlock(label="Name", data_type="STRING")
    payload = {
        "form_id": form_id,
        "user_id": user_id,
        "json_payload": {"1": {"Name": "Sample Application"}}
    }
    response = client.post("/api/v1/applications",json=payload)
    assert response.status_code == 200
    assert response.json() is True  # Assuming the endpoint returns True on success

#     payload = {
#         "form_id": form_id,
#         "user_id": user_id,
#         "json_payload": {"field1": "value1", "field2": "value2"}
#     }
#     response = client.post("/api/v1/applications",json=payload)
#     assert response.status_code == 200
#     assert response.json() is True  # Assuming the endpoint returns True on success


# test_create_application_success()
# TODO: This test currently fails because the application doesnt exist - fix this.

# def test_update_application_success():
#     # First create an application to ensure one exists
#     create_payload = {
#         "form_id": 1,
#         "user_id": 1,
#         "json_payload": {"field1": "original", "field2": "original_value2"}
#     }
#     create_response = client.post("/api/v1/applications", json=create_payload)
#     print(_global_applications_db)
    
#     application_id = 1  # Assuming an application with ID 1 exists
#     new_data = {
#         "json_payload": {"field1": "Hello", "field2": "new_value2"}
#     }
    
#     response = client.put(f"/api/v1/applications/{application_id}", json=new_data)
#     assert response.status_code == 200
#     assert response.json() is not None  # Assuming the endpoint returns the updated application
#     assert response.json().get("jsonPayload", {}).get("field1") == "Hello"
#     assert response.json().get("jsonPayload", {}).get("field2") == "new_value2"

# #test_update_application_success()


def test_get_application_by_id_success():
    
    application_id = 1  # Assuming an application with ID 1 exists
    form_id = 1  # Assuming a form with ID 1 exists
    
    response = client.get(f"/api/v1/applications/{application_id}?form_id={form_id}")
    assert response.status_code == 200
    assert response.json() is not None  # Assuming the endpoint returns the application
    assert response.json().get("id") == application_id
    assert response.json().get("form_id") == form_id


if __name__ == "__main__":
    test_create_application_success()
    #test_update_application_success()
