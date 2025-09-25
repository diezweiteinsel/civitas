from datetime import date
from backend.models import Base
from backend.crud import dbActions
from sqlalchemy import Column, Integer, String, Boolean, Date


def getMainTable():
    if Base.classes.main_table is not None:
        return Base.classes.main_table
    else:
        return createMainTable()


def createMainTable():
    
    columns = {"table_id": Column(Integer, primary_key=True)}  # Corresponding to the "form_table_id" table
    columns["name"] = Column(String)  # Name of the form
    columns["createdAt"] = Column(Date) # Creation date of the form
    columns["isActive"] = Column(Boolean)  # Status of the form
    #columns["Xoev"] = Column( string / TypeDecorator+ElementTree / SQLAlchemy UserDefinedType)
    # TypeDecorator+ElementTree saves as string in DB but automically returns as ElementTree object in Python
    # SQLAlchemy UserDefinedType saves as xml in DB and Python

    return dbActions.createTableClass("main_table", columns)

