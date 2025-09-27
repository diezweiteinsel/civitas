from datetime import date
from typing import Any, Type

from sqlalchemy import Column, Date, Integer, String, Boolean, Enum
from sqlalchemy.orm import Session
from sqlalchemy.orm import DeclarativeBase

from backend.core import db
from backend.models.domain.user import User, UserType
from backend.models.domain.user import RoleAssignment as DomainRoleAssignment


# Any Ideas for filename? -ps






#This Base is temporary, just for schema creation.
class SchemaBase(DeclarativeBase):
   pass


def user_db_setup():
    from backend.crud import dbActions # avoid circular import


    # This ensures that we always know when the tables already exist


    Base = db.get_base(reload=True)
    Base.metadata.create_all(bind=db.engine)  # Creates tables from Base in db, does nothing to existing tables

    if "user_table" in Base.classes.keys() or "role_assignment" in Base.classes.keys() or "form_table" in Base.classes.keys():
        print("abort")
        return  # Tables already exist in db
    if "user_table" in Base.metadata.tables.keys() or "role_assignment" in Base.metadata.tables.keys() or "form_table" in Base.metadata.tables.keys():
        print("abort")
        return  # Tables already exist in metadata
    orm_user_columns = {
        "id": Column(Integer, primary_key=True),
        "user_name": Column(String, nullable=False),
        "creation_date": Column(Date, nullable=False),
        "email": Column(String, nullable=True),
        "password": Column(String, nullable=False),
        "is_active": Column(Boolean, nullable=False, default=1),  # 1 for active, 0 for inactive
        }
    role_assignment_columns = {
        "id": Column(Integer, primary_key=True),
        "user_id": Column(Integer, nullable=False),
        "assignment_date": Column(Date, nullable=False),
        "role": Column(Enum(UserType), nullable=False),
    }
    form_table_columns = {
        "id": Column(Integer, primary_key=True),
        "form_name": Column(String, nullable=False),
        "created_at": Column(Date, default=date.today()),
        "is_active": Column(Boolean, default=True),
        "xoev": Column(String, nullable=False),
    }

    # was gespeichert wurde: "UserType.ADMIN"
    # neu: "ADMIN" -> Enum(UserType)

    OrmUser = dbActions.createTableClass(
        "user_table", orm_user_columns)
    OrmRoleAssignment = dbActions.createTableClass(
        "role_assignment", role_assignment_columns)
    OrmFormTable = dbActions.createTableClass(
        "form_table", form_table_columns)

    Base = db.get_base(reload=True)

    print(Base.classes.keys())
    print(Base.metadata.tables.keys())


if __name__ == "__main__":
    user_db_setup()
    #user_db_setup()
    #user_db_setup()
    #user_db_setup()
