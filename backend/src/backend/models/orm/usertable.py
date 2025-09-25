from typing import Any, Type

from sqlalchemy import Column, Date, Integer, String, Boolean



from backend.models.domain.user import User
from backend.core.ormUtil import SchemaBase



class OrmUser(SchemaBase):
    """
    This class is purely for export to other files and used to create instances, the actual tableclass will be dynamically created.
    """
    __tablename__ = "user_table"
    id = Column(Integer, primary_key=True)
    user_name = Column(String, nullable=False)
    creation_date = Column(Date, nullable=False)
    email = Column(String, nullable=True)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False, default=1)  # 1 for active, 0 for inactive

#TODO: change user role stuff
def to_orm_model(user: User) -> OrmUser:
    return OrmUser(
        user_name=user.username,
        creation_date=user.date_created,
        email=user.email,
        password=user.hashed_password,  #  TODO Password handling should be done securely elsewhere
        is_active=user.is_active
    )


def to_domain_model(orm_user: OrmUser) -> User:
    return User(
        id=orm_user.id,
        username=orm_user.user_name,
        user_roles=[],
        date_created=orm_user.creation_date,
        email=orm_user.email,
        hashed_password=orm_user.password,
        is_active=True,  # Assuming active by default; adjust as needed
        )





