
from sqlalchemy.orm import Session
from fastapi import HTTPException

from backend.models import User
from backend.models.orm.usertable import OrmUser, to_domain_model, to_orm_model
from backend.models.orm.roletable import to_domain_model as role_to_domain_model
import backend.crud.dbActions as dbActions
from . import role as roleCrud

def get_all_users(session: Session) -> list[User]:
    """
    Retrieve all users in the system.
    """
    orm_users = dbActions.getRows(session, OrmUser)
    users = []
    for orm_user in orm_users:
        users.append(to_domain_model(session, orm_user))
    return users

def add_user(session: Session, user: User):
    """
    Create a new user in the system.
    Returns None if user couldn't be created otherwise returns OrmUser instance
    """
    existing_user = session.query(OrmUser).filter_by(user_name=user.username).first()
    if existing_user:
        raise HTTPException(status_code=409, detail="Username already in use") # username already in use
    existing_user = session.query(OrmUser).filter_by(email=user.email).first()
    if existing_user:
        raise HTTPException(status_code=409, detail="Email already in use") # email already in use
    created_ormuser = dbActions.insertRow(session, OrmUser, to_orm_model(user))
    created_user = to_domain_model(session, created_ormuser)

    for role in user.user_roles:
        role.user_id = created_user.id

    # If the user has roles to be assigned, assign them and create them in the db
    if len(user.user_roles) > 0:
        created_orm_role_assignments = []
        for role_assignment in user.user_roles:
            created_orm_role_assignments.append(roleCrud.add_role_assignment(session, role_assignment))
        created_role_assignments = []
        for orm_role_assignment in created_orm_role_assignments:
            created_role_assignments.append(role_to_domain_model(orm_role_assignment))
        created_user.user_roles = created_role_assignments
    return created_user



def get_user_by_id(user_id: int, session: Session) -> User | None:
    results = dbActions.getRowsByFilter(session, OrmUser, {"id": user_id})
    if results:
        orm_user = results[0]
        return to_domain_model(session, orm_user)
    raise HTTPException(status_code=404, detail="User not found")



def get_user_by_name(username: str, session:Session) -> User | None:
    results = dbActions.getRowsByFilter(session, OrmUser, {"user_name": username})
    if results:
        orm_user = results[0]
        return to_domain_model(session, orm_user)
    raise HTTPException(status_code=404, detail="User not found")



def get_user_by_email(email: str, session:Session) -> User | None:
    results = dbActions.getRowsByFilter(session, OrmUser, {"email": email})
    if results:
        orm_user = results[0]
        return to_domain_model(session, orm_user)
    raise HTTPException(status_code=404, detail="User not found")

def get_all_admins(session: Session) -> list[User]:
    """
    Retrieve all users with the 'ADMIN' role.
    """
    admin_user_roles = roleCrud.get_all_admin_roles(session)
    admin_user_ids = [role.user_id for role in admin_user_roles]
    users = []
    for admin_user_id in admin_user_ids:
        users.append(get_user_by_id(admin_user_id, session))
    return users

def get_all_applicants(session: Session) -> list[User]:
    """
    Retrieve all users with the 'APPLICANT' role.
    """
    applicant_user_roles = roleCrud.get_all_applicant_roles(session)
    applicant_user_ids = [role.user_id for role in applicant_user_roles]
    users = []
    for applicant_user_id in applicant_user_ids:
        users.append(get_user_by_id(applicant_user_id, session))
    return users

def get_all_reporters(session: Session) -> list[User]:
    """
    Retrieve all users with the 'REPORTER' role.
    """
    reporter_user_roles = roleCrud.get_all_reporter_roles(session)
    reporter_user_ids = [role.user_id for role in reporter_user_roles]
    users = []
    for reporter_user_id in reporter_user_ids:
        users.append(get_user_by_id(reporter_user_id, session))
    return users
