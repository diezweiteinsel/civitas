from testcontainers.postgres import PostgresContainer
from fastapi.testclient import TestClient
from backend.api.endpoints.application import router
from backend.businesslogic.services.adminService import createUser
from fastapi import FastAPI
import pytest

app = FastAPI()
app.include_router(router, prefix="/api/v1")
# app.include_router(auth.router, prefix="/api/v1")

client = TestClient(app)

def test_create_application_success():
    user_id = 1  # Assuming a user with ID 1 exists
    form_id = 1  # Assuming a form with ID 1 exists

    payload = {
        "form_id": form_id,
        "user_id": user_id,
        "json_payload": {"field1": "value1", "field2": "value2"}
    }
    response = client.post("/api/v1/applications",json=payload)
    assert response.status_code == 200
    assert response.json()["formID"] == form_id
    assert response.json()["userID"] == user_id
    assert response.json()["jsonPayload"] == payload["json_payload"]


test_create_application_success()