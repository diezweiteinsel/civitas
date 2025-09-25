from pydantic import BaseModel
from enum import IntEnum, auto
from backend.models.domain.trigger import Trigger

class BBType(IntEnum):
    NULL = 0
    STRING = auto()
    INTEGER = auto()
    DATE = auto()
    FLOAT = auto()
    LONG = auto()

class BuildingBlock(BaseModel):
    '''A building block represents a single field in a form, with a name and a data type.'''
    id: int = -1
    # sorting purpose
    key: str = ""
    # label shown in frontend
    label: str = ""
    dataType: BBType = BBType.NULL
    required: bool = False
    order: int = 0
    constraintsJson: dict = {}
    triggers: list[Trigger] = []


