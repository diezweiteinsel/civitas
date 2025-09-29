from pydantic import BaseModel
from enum import IntEnum, auto, StrEnum
# backend.models.domain.trigger import Trigger

class BBType(StrEnum):
    NULL = "NULL"
    STRING = "STRING"
    TEXT = "TEXT"
    EMAIL = "EMAIL"
    INTEGER = "INTEGER"
    DATE = "DATE"
    FLOAT = "FLOAT"
    LONG = "LONG"

class BuildingBlock(BaseModel):
    '''A building block represents a single field in a form, with a name and a data type.'''
    #id: int = -1
    # sorting purpose
    #key: str = ""

    # label shown in frontend
    label: str = ""
    data_type: BBType = BBType.NULL
    required: bool = False
    #order: int = 0
    constraintsJson: dict = {}
    

