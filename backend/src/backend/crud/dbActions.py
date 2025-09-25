from typing import Type

from sqlalchemy import delete
from sqlalchemy.orm import Session

# from backend.models.orm import Base
from backend.core import db

"""
Usage API:
    func(session: Session = Depends(get_session_dep), ...)
Usage non-API:
    with db.get_session() as session:
        func(session, ...)

"""

def createTableClass(tablename: str, columns: dict) -> type:
    Base = db.get_base(reload=True)
    attrs = {"__tablename__": tablename}
    attrs.update(columns)  # add the column definitions
    tableclass = type(tablename, (Base,), attrs)
    Base.metadata.create_all(bind=db.engine)  # Creates tables from Base in db, does nothing to existing tables
    return tableclass


#TODO: implement explicit table class creation for User and Form
# @paul ? @jonathan ?
# don't think it's necessary since User and Form tables will be defined as ORM classes -ps

def createTable():
    pass


def insertRow(session: Session, tableClass: type, rowData: dict | type) -> type:
    """
    Insert a row into the table represented by tableClass using SQLAlchemy ORM.
    Uses get_session_dep() for session management.
    """
    # Can easily be adapted for fastapi use by making session a dependency
    if type(rowData) == dict:
        obj = tableClass(**rowData) # create instance of the ORM class
    else:
        obj = rowData
    

    session.add(obj)
    session.flush()       # push to DB so defaults (like IDs) are available
    session.refresh(obj)  # refresh to get DB-generated values
    return obj




def updateRow(session: Session, tableClass: type, rowData: dict):
    """
    rowData must include the primary key 'id' to identify which row to update.
    Attributes which are not included in rowData will remain unchanged.

    Returns updated row object.

    Update a row in the table represented by tableClass using SQLAlchemy ORM.
    Uses get_session_dep() for session management.
    """
    # Can easily be adapted for fastapi use by making session a dependency
    if "id" not in rowData:
        raise ValueError("rowData must include 'id'")

    obj = session.get(tableClass, rowData["id"]) # get existing object by primary key
    if not obj:
        raise ValueError("Object not found")
    for key, value in rowData.items():
        if key != "id":
            setattr(obj, key, value)
    session.flush()       # push to DB
    session.refresh(obj)  # refresh to get DB-generated values
    return obj


def removeRow(session: Session, tableClass: type, id: int):
    """
    Give id of row/object to be deleted as arg.

    Delete a row from the table represented by tableClass using SQLAlchemy ORM.
    Uses get_session_dep() for session management.
    """

    # Can easily be adapted for fastapi use by making session a dependency
    stmt = delete(tableClass).where(tableClass.id == id)


    session.execute(stmt) # add to session
    session.flush()       # push to DB


def getRowById(session: Session, tableClass: type, id: int):
    """
    Get a row from the table represented by tableClass by primary key id using SQLAlchemy ORM.
    Uses get_session_dep() for session management.
    """
    # Can easily be adapted for fastapi use by making session a dependency
    obj = session.get(tableClass, id) # get existing object by primary key
    return obj

def getRows(session: Session, tableClass: type):
    """
    Get all rows from the table represented by tableClass using SQLAlchemy ORM.
    Uses get_session_dep() for session management.
    """
    # Can easily be adapted for fastapi use by making session a dependency
    objs = session.query(tableClass).all() # get all objects
    return objs

def getRowsByFilter(session: Session, tableClass: type, filterDict: dict):
    """
    Returns all rows from the table that match ALL filters in filterDict.
    A filter is a key-value pair where the key is the column name and the value is the value to filter by.

    Get rows from the table represented by tableClass using SQLAlchemy ORM that match the filterDict.
    Uses get_session_dep() for session management.
    """
    # Can easily be adapted for fastapi use by making session a dependency
    query = session.query(tableClass)
    for key, value in filterDict.items():
        query = query.filter(getattr(tableClass, key) == value)
    objs = query.all()
    return objs



if __name__ == "__main__":
    # print(createTableClass("test", {"id2": String}))
    pass
