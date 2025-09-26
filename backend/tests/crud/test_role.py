from datetime import date
import os
from importlib import reload # for reloading modules

from testcontainers.postgres import PostgresContainer
import pytest

from backend import dbActions
from backend import db
from backend.core.ormUtil import user_db_setup
from backend.models.domain import user
from backend.crud import roleCrud
from backend.models.orm.roletable import OrmRoleAssignment

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

def test_add_role_assignment_func():
    Base = db.get_base(reload=True)  # Ensure we have the latest Base
    Base.metadata.drop_all(bind=db.engine)  # Clean up before test
    Base.metadata.create_all(bind=db.engine)  # Create tables

    with db.get_session() as session:


        domainRoleAssignment = user.RoleAssignment(user_id=1, assignment_date=date.today(), role=user.UserType.ADMIN) # Create a domain model instance of role ADMIN

        #  Add the role assignment to the database, should succeed and return the created ORM instance
        new_role_assignment = roleCrud.add_role_assignment(session, domainRoleAssignment)
         # Try to insert a RoleAssignment with identical user_id and role, should fail and return None
        new_role_assignment_secondInsert = roleCrud.add_role_assignment(session, domainRoleAssignment)
        assert new_role_assignment_secondInsert is None

        # Ensure the returned ORM instance matches the one in the database
        new_role_assignment_from_db = dbActions.getRowById(session,OrmRoleAssignment,1)
        assert new_role_assignment == new_role_assignment_from_db

        # Repeat the process for a different role assignment, same user_id but different role
        domainRoleAssignmentTwo = user.RoleAssignment(user_id=1, assignment_date=date.today(), role=user.UserType.REPORTER) # Create a domain model instance of role REPORTER
        new_role_assignmentTwo = roleCrud.add_role_assignment(session, domainRoleAssignmentTwo)
        new_role_assignmentTwo_secondInsert = roleCrud.add_role_assignment(session, domainRoleAssignmentTwo)
        assert new_role_assignmentTwo_secondInsert is None
        new_role_assignmentTwo_from_db = dbActions.getRowById(session,OrmRoleAssignment,2)
        assert new_role_assignmentTwo == new_role_assignmentTwo_from_db

        ormRoleAssignmentRows = dbActions.getRows(session, OrmRoleAssignment)


    # Verify the role assignment was added correctly
    assert new_role_assignment.id is not None
    assert ormRoleAssignmentRows[0].id == new_role_assignment.id
    assert ormRoleAssignmentRows[0].user_id == domainRoleAssignment.user_id
    assert ormRoleAssignmentRows[0].role == domainRoleAssignment.role

    # Verify the second role assignment was added correctly
    assert new_role_assignmentTwo.id is not None
    assert ormRoleAssignmentRows[1].id == new_role_assignmentTwo.id
    assert ormRoleAssignmentRows[1].user_id == domainRoleAssignmentTwo.user_id
    assert ormRoleAssignmentRows[1].role == domainRoleAssignmentTwo.role

    assert len(ormRoleAssignmentRows) == 2

def test_get_user_roles_func():

    with db.get_session() as session:

        user_roles = roleCrud.get_user_roles(session, 1)
        assert len(user_roles) == 2
        assert user_roles[0].user_id == 1
        assert user_roles[1].user_id == 1
        assert user_roles[0].role == "ADMIN"
        assert user_roles[1].role == "REPORTER"

def test_get_admin_roles_func():

    with db.get_session() as session:

        admin_roles = roleCrud.get_all_admin_roles(session)
        assert len(admin_roles) == 1
        assert admin_roles[0].role == "ADMIN"
        assert admin_roles[0].user_id == 1

def test_get_applicant_roles_func():

    with db.get_session() as session:

        applicant_roles = roleCrud.get_all_applicant_roles(session)
        assert len(applicant_roles) == 0
        assert applicant_roles == []

def test_get_reporter_roles_func():

    with db.get_session() as session:

        reporter_roles = roleCrud.get_all_reporter_roles(session)
        assert len(reporter_roles) == 1
        assert reporter_roles[0].role == "REPORTER"
        assert reporter_roles[0].user_id == 1