"""Entrypoint for the container.

This script waits for Postgres to be available, calls the user_db_setup()
helper to create tables if needed, and finally execs uvicorn to run the app.
"""

import os
import time
import traceback
from typing import Callable


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
        # we insert a demo user for easier testing
        from backend.core import security
        from backend.core import db as core_db
        from backend.crud.user import add_user, get_user_by_name
        from backend.models.domain.user import RoleAssignment, User, UserType
        from datetime import date
        demo_username = os.environ.get("DEMO_USERNAME", "demo")
        demo_password = os.environ.get("DEMO_PASSWORD", "demo")
        with core_db.get_session() as s:
            try:
                existing = get_user_by_name(demo_username, s)
                print(f"Demo user '{demo_username}' already exists, skipping demo user creation")
            except Exception:
                print(f"Creating demo user '{demo_username}' (password from DEMO_PASSWORD env)")
                new_user = User(
                    username=demo_username,
                    date_created=date.today(),
                    hashed_password=security.hash_password(demo_password),
                    user_roles=[
                        RoleAssignment(
                            role=UserType.APPLICANT,
                            assignment_date=date.today(),
                        ),
                    ],
                    email="demo@example.com"
                )
                created = add_user(s, new_user)
                if created is None:
                    print("add_user returned None - demo user creation failed or user already exists")
                else:
                    print(f"Demo user '{demo_username}' created with id={created.id}")
    except Exception:
        print("Demo user creation failed:")
        traceback.print_exc()

    try:
        # we insert a demo admin user for easier testing
        from backend.core import security
        from backend.core import db as core_db
        from backend.crud.user import add_user, get_user_by_name
        from backend.models.domain.user import RoleAssignment, User, UserType
        from datetime import date
        with core_db.get_session() as s:
            try:
                existing = get_user_by_name("admin", s)
                print(f"Demo user 'admin' already exists, skipping demo admin creation")
            except Exception:
                print(f"Creating demo admin 'admin' (password from DEMO_PASSWORD env)")
                new_admin = User(
                    username="admin",
                    date_created=date.today(),
                    hashed_password=security.hash_password("admin"),
                    user_roles=[
                        RoleAssignment(
                            role=UserType.ADMIN,
                            assignment_date=date.today(),
                        )
                    ],
                    email="admin@example.com"
                )
                created = add_user(s, new_admin)
                if created is None:
                    print("add_user returned None - demo admin creation failed or user already exists")
                else:
                    print(f"Demo admin 'admin' created with id={created.id}")
        traceback.print_exc()
    except Exception:
        print("Demo admin creation failed:")
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
