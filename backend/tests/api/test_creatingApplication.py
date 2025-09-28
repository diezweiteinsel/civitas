from fastapi.testclient import TestClient
from backend.api.endpoints.application import router
from backend.businesslogic.services.adminService import createUser
from fastapi import FastAPI
import pytest
from backend.businesslogic.services.mockups import _global_users_db, _global_applications_db, _global_forms_db

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
    assert response.json() is True  # Assuming the endpoint returns True on success


test_create_application_success()

def test_update_application_success():
    # First create an application to ensure one exists
    create_payload = {
        "form_id": 1,
        "user_id": 1,
        "json_payload": {"field1": "original", "field2": "original_value2"}
    }
    create_response = client.post("/api/v1/applications", json=create_payload)
    print(_global_applications_db)
    
    application_id = 1  # Assuming an application with ID 1 exists
    new_data = {
        "json_payload": {"field1": "Hello", "field2": "new_value2"}
    }
    
    response = client.put(f"/api/v1/applications/{application_id}", json=new_data)
    assert response.status_code == 200
    assert response.json() is not None  # Assuming the endpoint returns the updated application
    assert response.json().get("jsonPayload", {}).get("field1") == "Hello"
    assert response.json().get("jsonPayload", {}).get("field2") == "new_value2"

test_update_application_success()