from fastapi.testclient import TestClient
from fastapi import FastAPI
from backend.api.endpoints.health import router


app = FastAPI()
app.include_router(router)

client = TestClient(app)


def test_health_endpoint_status_ok():
	response = client.get("/health")
	assert response.status_code == 200


def test_health_endpoint_payload():
	response = client.get("/health")
	assert response.json() == {"status": "ok"}
