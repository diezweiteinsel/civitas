"""Entrypoint for the container.

This script waits for Postgres to be available, calls the user_db_setup()
helper to create tables if needed, and finally execs uvicorn to run the app.
"""

import os
import time
import traceback
from typing import Callable


def _env_truthy(value: str | None, default: bool = True) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def create_demo_users() -> None:
    """Ensure demo users for every role exist."""
    from datetime import date

    from fastapi import HTTPException

    from backend.core import db as core_db
    from backend.core import security
    from backend.crud.user import add_user, get_user_by_name
    from backend.models.domain.user import RoleAssignment, User, UserType

    demo_definitions = [
        {
            "username": os.environ.get("DEMO_USERNAME", "demo"),
            "password": os.environ.get("DEMO_PASSWORD", "demo"),
            "roles": [UserType.APPLICANT],
            "email": os.environ.get("DEMO_EMAIL", "demo@example.com"),
        },
        {
            "username": os.environ.get("ADMIN_USERNAME", "admin"),
            "password": os.environ.get("ADMIN_PASSWORD", "admin"),
            "roles": [UserType.ADMIN],
            "email": os.environ.get("ADMIN_EMAIL", "admin@example.com"),
        },
        {
            "username": os.environ.get("REPORTER_USERNAME", "reporter"),
            "password": os.environ.get("REPORTER_PASSWORD", "reporter"),
            "roles": [UserType.REPORTER],
            "email": os.environ.get("REPORTER_EMAIL", "reporter@example.com"),
        },
    ]

    with core_db.get_session() as session:
        for definition in demo_definitions:
            username = definition["username"].strip()
            try:
                get_user_by_name(username, session)
                print(f"Demo user '{username}' already exists, skipping")
                continue
            except HTTPException as exc:
                if exc.status_code != 404:
                    print(f"Lookup for user '{username}' failed: {exc.detail}")
                    raise
            except Exception:
                traceback.print_exc()
                raise

            try:
                hashed_password = security.hash_password(definition["password"])
                roles = [
                    RoleAssignment(role=role, assignment_date=date.today())
                    for role in definition["roles"]
                ]
                new_user = User(
                    username=username,
                    date_created=date.today(),
                    hashed_password=hashed_password,
                    user_roles=roles,
                    email=definition["email"],
                )
                created = add_user(session, new_user)
                if created is None:
                    print(f"add_user returned None - could not create '{username}'")
                else:
                    print(f"Demo user '{username}' created with id={created.id}")
            except HTTPException as exc:
                if exc.status_code == 409:
                    print(f"User '{username}' already exists ({exc.detail}), skipping")
                    session.rollback()
                    continue
                raise


def create_demo_forms() -> None:
    """Ensure at least one rich demo form exists."""
    from backend.core import db
    from backend.crud import formCrud
    from backend.models.domain.buildingblock import BBType, BuildingBlock
    from backend.models.domain.form import Form

    demo_form_name = os.environ.get("DEMO_FORM_NAME", "Civic Service Request")

    with db.get_session() as session:
        existing_forms = formCrud.get_all_forms(session)
        if any(form.form_name == demo_form_name for form in existing_forms):
            print(f"Demo form '{demo_form_name}' already exists, skipping")
            return

        blocks = {
            "1": BuildingBlock(
                label="full_name",
                data_type=BBType.STRING,
                required=True,
                constraintsJson={"min_length": 3},
            ),
            "2": BuildingBlock(
                label="contact_email",
                data_type=BBType.EMAIL,
                required=False,
            ),
            "3": BuildingBlock(
                label="issue_description",
                data_type=BBType.TEXT,
                required=True,
                constraintsJson={"max_length": 500},
            ),
            "4": BuildingBlock(
                label="submission_date",
                data_type=BBType.DATE,
                required=True,
            ),
            "5": BuildingBlock(
                label="estimated_cost",
                data_type=BBType.FLOAT,
                required=False,
            ),
            "6": BuildingBlock(
                label="household_size",
                data_type=BBType.INTEGER,
                required=False,
            ),
        }

        form = Form(form_name=demo_form_name, blocks=blocks)
        created_form = formCrud.add_form(session, form)
        print(
            f"Demo form '{created_form.form_name}' created with id={created_form.id}"
        )


def _sample_value_for_block(block) -> object:
    from datetime import date

    from backend.models.domain.buildingblock import BBType

    data_type = block.data_type
    if isinstance(data_type, str):
        try:
            data_type = BBType(data_type)
        except ValueError:
            data_type = BBType.STRING

    if data_type == BBType.STRING or data_type == BBType.TEXT:
        return "Sample text for " + block.label.replace("_", " ")
    if data_type == BBType.EMAIL:
        return "civic.user@example.com"
    if data_type == BBType.INTEGER:
        return 3
    if data_type == BBType.DATE:
        return date.today()
    if data_type == BBType.FLOAT:
        return 42.5
    return "N/A"


def create_demo_applications() -> None:
    """Ensure demo applications exist for the demo form."""
    from typing import Optional

    from fastapi import HTTPException

    from backend.core import db
    from backend.crud import applicationCrud, dbActions, formCrud
    from backend.crud.user import get_user_by_name
    from backend.models.domain.application import Application, ApplicationStatus
    from backend.models.domain.form import Form

    with db.get_session() as session:
        existing_apps = applicationCrud.get_all_applications(session)
        if existing_apps:
            print("Demo applications already exist, skipping")
            return

        forms = formCrud.get_all_forms(session)
        if not forms:
            print("No forms available; skipping demo application creation")
            return

        demo_form_name = os.environ.get("DEMO_FORM_NAME", "Civic Service Request")
        target_form_orm = next(
            (form for form in forms if form.form_name == demo_form_name),
            forms[0],
        )
        target_form = Form.from_orm_model(target_form_orm)

        def _get_user(username: str) -> Optional[int]:
            try:
                user = get_user_by_name(username, session)
                return user.id
            except HTTPException as exc:
                if exc.status_code == 404:
                    return None
                raise

        applicant_username = os.environ.get("DEMO_USERNAME", "demo")
        applicant_id = _get_user(applicant_username)
        if applicant_id is None:
            print(
                f"Applicant user '{applicant_username}' not found; skipping demo applications"
            )
            return

        admin_username = os.environ.get("ADMIN_USERNAME", "admin")
        admin_id = _get_user(admin_username)

        from copy import deepcopy

        payload = {
            block.label: {
                "label": block.label,
                "value": _sample_value_for_block(block),
            }
            for block in target_form.blocks.values()
        }

        def _with_override(source: dict[str, dict[str, object]], label: str, value: object):
            clone = deepcopy(source)
            if label not in clone:
                clone[label] = {"label": label, "value": value}
            else:
                clone[label]["value"] = value
            return clone

        demo_applications = [
            Application(
                user_id=applicant_id,
                form_id=target_form_orm.id,
                admin_id=admin_id,
                status=ApplicationStatus.PENDING,
                jsonPayload=payload,
            ),
            Application(
                user_id=applicant_id,
                form_id=target_form_orm.id,
                admin_id=admin_id,
                status=ApplicationStatus.APPROVED,
                jsonPayload=_with_override(
                    payload, "description", "Approved request"
                ),
                is_public=True,
            ),
            Application(
                user_id=applicant_id,
                form_id=target_form_orm.id,
                admin_id=admin_id,
                status=ApplicationStatus.REJECTED,
                jsonPayload=_with_override(
                    payload, "issue_description", "Rejected request"
                ),
            ),
            Application(
                user_id=applicant_id,
                form_id=target_form_orm.id,
                admin_id=admin_id,
                status=ApplicationStatus.APPROVED,
                jsonPayload=_with_override(
                    payload, "issue_description", "Approved request"
                ),
            ),
        ]

        table_class = dbActions.get_application_table_by_id(target_form_orm.id)

        for index, application in enumerate(demo_applications, start=1):
            inserted = applicationCrud.insert_application(session, application)
            status = application.status.value
            # if index == 2:
            #     dbActions.updateRow(
            #         session,
            #         table_class,
            #         {"id": inserted.id, "is_public": True},
            #     )
            print(
                f"Demo application #{index} created with id={inserted.id} (status={status})"
            )


def populate_db_with_demo_data() -> None:
    if not _env_truthy(os.environ.get("SEED_DEMO_DATA", "1")):
        print("Skipping demo data population (SEED_DEMO_DATA disabled)")
        return

    try:
        create_demo_users()
        create_demo_forms()
        create_demo_applications()
    except Exception:
        print("Demo data population failed:")
        traceback.print_exc()

def wait_for_db(
    connect_fn: Callable[[], object], retries: int = 30, delay: float = 1.0
):
    """Wait until the provided connect_fn succeeds or raise after retries."""
    last_exc = None
    for attempt in range(1, retries + 1):
        try:
            conn = connect_fn()
            try:
                # some connection objects need close()
                conn.close()
            except Exception:
                pass
            print(f"DB reachable after {attempt} attempt(s)")
            return
        except Exception as e:
            last_exc = e
            print(f"DB not ready (attempt {attempt}/{retries}): {e}")
            time.sleep(delay)
    print("DB did not become ready in time")
    if last_exc:
        traceback.print_exception(type(last_exc), last_exc, last_exc.__traceback__)
    raise RuntimeError("DB not ready")


def main():
    # Import here so module-level imports don't run before env is ready
    try:
        from backend.core import db as core_db
        from backend.core.ormUtil import user_db_setup
    except Exception:
        traceback.print_exc()
        raise

    # Wait for DB reachable
    db_host = os.environ.get("DB_HOST", "db")
    db_port = os.environ.get("DB_PORT", "5432")
    print(f"Waiting for DB at {db_host}:{db_port}...")
    wait_for_db(core_db.get_psycopg_connection, retries=60, delay=1.0)

    # Run the schema setup (idempotent-ish)
    try:
        print("Running user_db_setup() to ensure user tables exist...")
        user_db_setup()
        print("user_db_setup() finished")
    except Exception:
        print("user_db_setup() failed:")
        traceback.print_exc()
    
    try:
        populate_db_with_demo_data()
    except Exception:
        print("populate_db_with_demo_data() failed:")
        traceback.print_exc()


    # --- seed an initial admin user if no users exist ---
    # try:
    #     print("Checking for existing users to decide about admin seeding...")
    #     # local imports to avoid circular import issues at module import time
    #     from datetime import date

    #     from backend.core import db as core_db
    #     from backend.crud.role import add_role_assignment
    #     from backend.crud.user import add_user, get_all_users
    #     from backend.models.domain.user import RoleAssignment, User, UserType

    #     admin_username = os.environ.get("ADMIN_USERNAME", "admin")
    #     admin_password = os.environ.get("ADMIN_PASSWORD", "admin")

    #     with core_db.get_session() as s:
    #         users = get_all_users(s)
    #         if not users:
    #             print(
    #                 f"No users found. Creating initial admin user '{admin_username}' (password from ADMIN_PASSWORD env)"
    #             )
    #             new_user = User(
    #                 username=admin_username,
    #                 date_created=date.today(),
    #                 hashed_password=admin_password,
    #                 user_roles=[],
    #             )
    #             created = add_user(s, new_user)
    #             if created is None:
    #                 print(
    #                     "add_user returned None - admin user creation failed or user already exists"
    #                 )
    #             else:
    #                 try:
    #                     if created.id is None:
    #                         raise RuntimeError("created user has no id")
    #                     ra = RoleAssignment(
    #                         role=UserType.ADMIN,
    #                         assignment_date=date.today(),
    #                     )
    #                     res = add_role_assignment(s, ra)
    #                     print(
    #                         "Admin user created, role assignment result:",
    #                         None if res is None else f"id={res.id}",
    #                     )
    #                 except Exception:
    #                     print("Role assignment failed:")
    #                     traceback.print_exc()
    #         else:
    #             print(f"{len(users)} existing user(s) found; skipping admin seed")
    # except Exception:
    #     print("Admin seeding failed:")
    #     traceback.print_exc()

    # Exec uvicorn to run the app (replaces this process)
    uvicorn_cmd = [
        "uvicorn",
        "backend.main:app",
        "--host",
        "0.0.0.0",
        "--port",
        os.environ.get("PORT", "8000"),
    ]
    print("Starting uvicorn:", " ".join(uvicorn_cmd))
    os.execvp(uvicorn_cmd[0], uvicorn_cmd)


if __name__ == "__main__":
    main()
