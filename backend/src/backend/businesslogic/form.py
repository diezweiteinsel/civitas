from backend.models import Base, BBType
from backend.models import Form
from sqlalchemy import BigInteger, Column, Date, Float, Integer, Numeric, String, Text
from backend.crud import dbActions


_BB_TYPE_MAP = {
    BBType.STRING: String,
    BBType.TEXT: Text,
    BBType.EMAIL: String,
    BBType.INTEGER: Integer,
    BBType.DATE: Date,
    BBType.FLOAT: Float,
    BBType.LONG: BigInteger,
    BBType.NUMBER: Numeric,
}


def convertType(blockType: BBType):
    return _BB_TYPE_MAP.get(blockType, String)


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
