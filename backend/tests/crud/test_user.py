from datetime import date
from importlib import reload # for reloading modules
import os

import pytest
from testcontainers.postgres import PostgresContainer
from fastapi.exceptions import HTTPException

from backend import dbActions
from backend import db
from backend.models.orm.base import Base
from backend.models.orm.usertable import OrmUser
from backend.models.orm.roletable import OrmRoleAssignment
from backend.models.domain import user
from backend.crud import userCrud

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
    from backend.core.ormUtil import user_db_setup
    
    user_db_setup()  # Ensure tables are created before tests run


def test_add_user_func():
    Base = db.get_base(reload=True)  # Ensure we have the latest Base
    Base.metadata.drop_all(bind=db.engine)  # Clean up before test
    Base.metadata.create_all(bind=db.engine)  # Create tables

    with db.get_session() as session:
        # Create table if not exists
        # OrmUser.__table__.create(bind=session.get_bind(), checkfirst=True)

        roleAssignment = user.RoleAssignment(user_id=1, assignment_date=date.today(), role="ADMIN")

        # Insert a user
        domainUser = user.User(username="name", date_created=date.today(), hashed_password="adsd", user_roles=[roleAssignment])
        new_user: user.User = userCrud.add_user(session, domainUser)
        ormUserRows = dbActions.getRows(session, OrmUser)
        assert len(ormUserRows) == 1

        # Try to insert a user with identical username

        with pytest.raises(HTTPException) as exc_info:
            userCrud.add_user(session, domainUser)
        ormUserRows = dbActions.getRows(session, OrmUser)
        assert exc_info.value.status_code == 409
        assert str(exc_info.value.detail) == "Username already in use"
        assert len(ormUserRows) == 1

        new_user_from_db = dbActions.getRowById(session,OrmUser,1)



        ormRoleAssignmentRows = dbActions.getRows(session, OrmRoleAssignment)


    # Verify the user was added
    assert new_user.id is not None
    assert new_user.username == "name"
    assert new_user.email is None
    assert new_user.hashed_password == "adsd"
    assert new_user.user_roles == [roleAssignment]
    assert new_user_from_db.id == new_user.id
    assert new_user_from_db.user_name == new_user.username
    assert new_user_from_db.email == new_user.email
    assert new_user_from_db.password == new_user.hashed_password

    # Verify the role assignment was added
    assert len(ormRoleAssignmentRows) == 1
    assert ormRoleAssignmentRows[0].user_id == new_user.id
    assert ormRoleAssignmentRows[0].role == "ADMIN"
