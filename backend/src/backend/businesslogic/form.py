from enum import Enum
from backend.models import Base
from backend.models import Form
# from backend.models.buildingblock import BuildingBlockDataType
from sqlalchemy import Column, Integer, String
from backend.crud import dbActions



# Helper function to convert python types to SQLAlchemy types
# def convertType(blockType: BuildingBlockDataType):

#     if blockType == BuildingBlockDataType.STRING:
#         return String
#     elif blockType == BuildingBlockDataType.INT:
#         return Integer


# Converts a form to a SQLAlchemy table class
def formToTable(form: Form):

    #use primary key for uniquely naming/identifying the corresponding tables in the db
    tableName = "form_" + str(form.formID)
    columns = {"id": Column(Integer, primary_key=True)}
    for block in form.structure:
        columns[block.name] = Column(convertType(block.data_type))
    return dbActions.createTableClass(tableName, columns)

def getAllFormTables():
    '''Returns all tables that represent forms in a list of tuples (tableName, class)'''
    tablesAll = Base.classes
    tablesForm: list[()] = []
    for tableName, cls in tablesAll.items():
        if tableName.startswith("form_"):
            tablesForm.append((tableName,cls))

    return tablesForm
