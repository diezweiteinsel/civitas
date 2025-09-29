from typing import Type

from backend.models.orm import usertable
from sqlalchemy import Column, Date, Enum, Integer, String
from sqlalchemy.orm import Session

from backend.core.ormUtil import SchemaBase
from backend.crud import dbActions
from backend.models.domain.user import RoleAssignment as DomainRoleAssignment, UserType


# A user has roleAssignments, each roleAssignment has a role


class OrmRoleAssignment(SchemaBase):
    """
    This class is purely for export to other files and used to create instances, the actual tableclass will be dynamically created.
    """

    __tablename__ = "role_assignment"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    assignment_date = Column(Date, nullable=False)
    role = Column(Enum(UserType), nullable=False)


def to_orm_model(domain_role_assignment: DomainRoleAssignment) -> OrmRoleAssignment:
    return OrmRoleAssignment(
        user_id=domain_role_assignment.user_id,
        assignment_date=domain_role_assignment.assignment_date,
        # Ensure role is stored as plain string in DB (enum -> value)
        role=domain_role_assignment.role,
    )


def to_domain_model(orm_role_assignment: OrmRoleAssignment) -> DomainRoleAssignment:
    return DomainRoleAssignment(
        user_id=orm_role_assignment.user_id,
        assignment_date=orm_role_assignment.assignment_date,
        role=UserType[orm_role_assignment.role]
    )



def get_user_roles(orm_user: Type, session: Session) -> list[DomainRoleAssignment]:
    integerthing = orm_user.id
    role_assignments = dbActions.getRowsByFilter(
        session, OrmRoleAssignment, {"user_id": integerthing}
    )

    return role_assignments


def get_user_roles_by_id(user_id: int, session:Session):
    from backend.crud import userCrud
    user = userCrud.get_user_by_id(user_id, session)
    ormUser = usertable.to_orm_model(user)
    return get_user_roles(ormUser)