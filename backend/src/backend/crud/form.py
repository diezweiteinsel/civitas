from backend.models.orm.base import Base
from sqlalchemy import Table
from backend.crud import dbActions

# Is this business logic or crud?
'''
Returns all tables that represent forms
def getAllFormTables():
    tablesAll: dict = Base.classes
    tablesForm: list[()] = []
    for table in tablesAll.keys():
        if table.startswith("form_"):
            tablesForm.append((table,tablesAll[table]))

    return tablesForm
'''
