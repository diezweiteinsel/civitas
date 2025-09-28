
from importlib import reload
import pytest
import os
from datetime import datetime, timedelta
from backend.core.config import settings
from jose import jwt
from testcontainers.postgres import PostgresContainer

from backend.crud import dbActions

from backend.core import db

from backend.core.ormUtil import user_db_setup

from backend.api import deps



try:

    SECRET_KEY = getattr(settings, "SECRET_KEY", os.environ.get("SECRET_KEY", "testsecret"))
    ALGORITHM = getattr(settings, "ALGORITHM", os.environ.get("ALGORITHM", "HS256"))
    EXPIRE_MINUTES = int(getattr(settings, "ACCESS_TOKEN_EXPIRE_MINUTES", os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", 30)))
except Exception:
    SECRET_KEY = os.environ.get("SECRET_KEY", "testsecret")
    ALGORITHM = os.environ.get("ALGORITHM", "HS256")
    EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

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
    os.environ["ECHO_SQL"] = "0" # turn off THE NOISE AAAH THE NOISE
    reload(db)
    reload(dbActions)
    user_db_setup()


@pytest.fixture
def valid_jwt_token():
    now = datetime.utcnow()
    payload = {
        "sub": "test_user",
        "roles": ["ADMIN", "APPLICANT"],
        "exp": int((now + timedelta(minutes=EXPIRE_MINUTES)).timestamp()),
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    if isinstance(token, bytes):
        token = token.decode("utf-8")
    return token


def test_post_form(valid_jwt_token):
    from fastapi.testclient import TestClient
    from backend.api.endpoints.form import router
    from fastapi import FastAPI
    import pytest
    import os
    from datetime import datetime, timedelta
    from backend.core.config import settings
    from jose import jwt

    app = FastAPI()
    app.include_router(router, prefix="/api/v1")
    app.dependency_overrides[deps.get_current_user_payload] = lambda: {"sub": "test_user", "roles": ["ADMIN", "APPLICANT"]}
    client = TestClient(app)

    # Define a sample form creation payload
    form_payload = {
        "form_name": "Test Form",
        "blocks": {
            "1":{
                "data_type": "TEXT",
                "label": "What is your name?"
            },
            "2":
            {
                "data_type": "NUMBER",
                "label": "How old are you?"
            }
        }
    }
    token = valid_jwt_token
    # Send a POST request to create a new form
    response = client.post("/api/v1/forms", json=form_payload, headers={"Authorization": f"Bearer {token}"})

    # Check the response status code and content
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["success"] is True
    assert response_data["message"] == "Form created successfully"