
from sqlalchemy.orm import Session
from backend.models import User
from backend.models.orm.usertable import OrmUser, to_domain_model, to_orm_model
from backend.models.orm.roletable import to_domain_model as role_to_domain_model
import backend.crud.dbActions as dbActions
from .role import add_role_assignment

def get_all_users(session: Session) -> list[User]:
    """
    Retrieve all users in the system.
    """
    orm_users = dbActions.getRows(session, OrmUser)
    users = []
    for orm_user in orm_users:
        users.append(to_domain_model(orm_user))
    return users

def add_user(session: Session, user: User):
    """
    Create a new user in the system.
    Returns None if user couldn't be created otherwise returns OrmUser instance
    """
    existing_user = session.query(OrmUser).filter_by(user_name=user.username).first()
    if existing_user:
        return None # username already in use
    existing_user = session.query(OrmUser).filter_by(email=user.email).first()
    if existing_user:
        return None # email already in use
    created_ormuser = dbActions.insertRow(session, OrmUser, to_orm_model(user))
    created_user = to_domain_model(created_ormuser)

    for role in user.user_roles:
        role.user_id = created_user.id

    # If the user has roles to be assigned, assign them and create them in the db
    if len(user.user_roles) > 0:
        created_orm_role_assignments = []
        for role_assignment in user.user_roles:
            created_orm_role_assignments.append(add_role_assignment(session, role_assignment))
        created_role_assignments = []
        for orm_role_assignment in created_orm_role_assignments:
            created_role_assignments.append(role_to_domain_model(orm_role_assignment))
        created_user.user_roles = created_role_assignments
    return created_user


def get_user_by_id(user_id: int, session: Session) -> User | None:
    orm_user = dbActions.getRowById(session, OrmUser, user_id)
    if orm_user:
        return to_domain_model(orm_user)
    return None

def get_user_by_name(username: str, session: Session) -> User | None:
    # Use a more descriptive variable name like 'results'
    results = dbActions.getRowsByFilter(session, OrmUser, {"user_name": username})

    # Check if a list was returned and that it contains exactly one user
    if results and len(results) == 1:
        # Pass the first element of the list ([0]) to the function
        return to_domain_model(results[0])

    # Return None if no user or multiple users are found
    return None

def get_user_by_email(email: str, session:Session) -> User | None:
    orm_user = dbActions.getRowsByFilter(session, OrmUser, {"email": email})
    if orm_user:
        return to_domain_model(orm_user)
    return None
