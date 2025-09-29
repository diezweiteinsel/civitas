from datetime import date, datetime
import json
from typing import Type

from fastapi import HTTPException
from sqlalchemy import Boolean, Column, Date, Float, Integer, String, delete, DateTime, text
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
    """
    ATTENTION: You most likely DON'T want to call this directly!\n
    Creates an Orm table class from a dict of columns
    """
    Base = db.get_base(reload=True)
    attrs = {"__tablename__": tablename}
    attrs.update(columns)  # add the column definitions
    tableclass = type(tablename, (Base,), attrs)
    Base.metadata.create_all(bind=db.engine)  # Creates tables from Base in db, does nothing to existing tables
    return tableclass



def matchType(blockType: str):
    match blockType:
        case "NULL":
            raise Exception # Why does this exist?
        case "STRING" | "TEXT" | "EMAIL":
            return Column(String, nullable=True)
        case "INTEGER":
            return Column(Integer, nullable=True)
        case "DATE":
            return Column(Date, nullable=True)
        case "DATETIME":
            return Column(DateTime, nullable=True)
        case "FLOAT":
            return Column(Float, nullable=True)
        case "LONG":
            raise Exception # Does long even exist in Python?
    


#TODO: implement explicit table class creation for User and Form
# @paul ? @jonathan ?
# don't think it's necessary since User and Form tables will be defined as ORM classes -ps

def createFormTable(id: int, xoev: str):
    """
    Takes:\n
    The form's id\n
    The form's xoev\n
    Does:\n
    Creates a tableClass for the given form's (as xoev) applications
    """
    tablename = "form_" + str(id)
    # TODO we need to ensure that created buildingblocks do not have a label conflicting with these existing columns
    columns = { "id": Column(Integer, primary_key=True),
                "user_id": Column(Integer, nullable=False),
                "form_id": Column(Integer, nullable=False),
                "admin_id": Column(Integer, nullable=True),
                "status": Column(String, server_default=text("'PENDING'"), nullable=False),
                "created_at": Column(DateTime, server_default=text("CURRENT_TIMESTAMP"), nullable=False),
                "current_snapshot_id": Column(Integer, server_default=text("-1")),
                "previous_snapshot_id": Column(Integer, server_default=text("-1")),
                "is_public": Column(Boolean, server_default=text("false"), nullable=False)
                }
    if xoev == "":
        raise Exception("xoev is empty")
    xoevDict = json.loads(xoev)
    if "blocks" not in xoevDict or not xoevDict["blocks"]:
        raise Exception("blocks can't be empty or missing")

    for block in xoevDict["blocks"].values():
        columns[block["label"]] = matchType(block["data_type"])
    try:
        return createTableClass(tablename=tablename, columns=columns)
    except Exception as e:
        raise Exception("Something went wrong", e)


def insertRow(session: Session, tableClass: type, rowData: dict | type) -> type:
    """
    Takes an object of tableClass or a dict of tableClass' columns\n
    Inserts a row into the table represented by tableClass\n
    Returns the updated/created row object or raises an error
    """
    # Can easily be adapted for fastapi use by making session a dependency
    if type(rowData) == dict:
        obj = tableClass(**rowData) # create instance of the ORM class
    else:
        obj = rowData
    
    try:
        session.add(obj)
        session.flush()       # push to DB so defaults (like IDs) are available
        session.refresh(obj)  # refresh to get DB-generated values
        return obj
    except Exception as e:
        session.rollback()
        print(f"Error inserting row: {e}")
        raise HTTPException(status_code=500, detail="Error inserting row")




def updateRow(session: Session, tableClass: type, rowData: dict):
    """
    rowData MUST include the primary key 'id' to identify which row to update
    Attributes which are not included in rowData will remain unchanged

    Returns updated row object.

    Update a row in the table represented by tableClass
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
    """

    # Can easily be adapted for fastapi use by making session a dependency
    stmt = delete(tableClass).where(tableClass.id == id)


    session.execute(stmt) # add to session
    session.flush()       # push to DB


def getRowById(session: Session, tableClass: type, id: int) -> type | None:
    """
    Get a row from the table represented by tableClass by primary key id using SQLAlchemy ORM.
    Returns None when not found
    """
    # Can easily be adapted for fastapi use by making session a dependency
    obj = session.get(tableClass, id) # get existing object by primary key
    return obj

def getRows(session: Session, tableClass: type) -> list:
    """
    Get all rows from the table represented by tableClass, returns empty list when tableClass is empty\n
    """
    # Can easily be adapted for fastapi use by making session a dependency
    objs = session.query(tableClass).all() # get all objects
    return objs

def getRowsByFilter(session: Session, tableClass: type, filterDict: dict):
    """
    Returns all rows from the table that match ALL filters in filterDict.
    A filter is a key-value pair where the key is the column name and the value is the value to filter by.

    Returns all rows as a list or an empty list if no matches are found.
    """
    # Can easily be adapted for fastapi use by making session a dependency
    query = session.query(tableClass)
    for key, value in filterDict.items():
        query = query.filter(getattr(tableClass, key) == value)
    objs = query.all()
    return objs

def get_application_table_by_id(id: int):
    try:
        Base = db.get_base(True)
        tableName = "form_" + str(id)
        return Base.classes[tableName]
    except KeyError as k:
        raise k
    except Exception as e:
        raise e

if __name__ == "__main__":
    # print(createTableClass("test", {"id2": String}))
    pass
