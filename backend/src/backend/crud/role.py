from sqlalchemy.orm import Session

import backend.crud.dbActions as dbActions
from backend.models.domain import user
from backend.models.orm.roletable import (
    OrmRoleAssignment,
    to_domain_model,
    to_orm_model,
)


def add_role_assignment(
    session, domain_role_assignment: user.RoleAssignment
) -> OrmRoleAssignment | None:
    role_value = domain_role_assignment.role
    existing_assignment = (
        session.query(OrmRoleAssignment)
        .filter_by(user_id=domain_role_assignment.user_id, role=role_value)
        .first()
    )
    if existing_assignment:
        return None  # User is already assigned that role

    return dbActions.insertRow(
        session, OrmRoleAssignment, to_orm_model(domain_role_assignment)
    )


def get_user_roles(session: Session, user_id: int) -> list[user.RoleAssignment]:
    """
    Returns a list of RoleAssignment domain models for the given user_id.
    """
    orm_role_assignments = dbActions.getRowsByFilter(
        session, OrmRoleAssignment, {"user_id": user_id}
    )
    domain_role_assignments = []
    for orm_role_assignment in orm_role_assignments:
        domain_role_assignments.append(to_domain_model(orm_role_assignment))
    return domain_role_assignments
