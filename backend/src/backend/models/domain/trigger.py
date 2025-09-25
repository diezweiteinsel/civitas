from pydantic import BaseModel, ConfigDict
from enum import IntEnum, auto

class TriggerType(IntEnum):
    NONE = 0
    #String enum reserved up to 100
    STRING_CONTAINS = 1
    STRING_CONTAINS_NOT = auto()
    STRING_LENGTH_BIGGER_THAN = auto()
    STRING_LENGTH_SMALLER_THAN = auto()
    #int enum reserved up to 200
    INT_SMALLER_THAN = 101
    INT_BIGGER_THAN = auto()
    INT_EQUALS = auto()
    #Date enum reserved up to 300
    DATE_IS_BEFORE = 201
    #Float enum reserved up to 400
    FLOAT_SMALLER_THAN = 301
    FLOAT_BIGGER_THAN = auto()
    FLOAT_EQUALS = auto()

class TriggerResultType(IntEnum):
    NONE = 0
    RAISE_FLAG = auto()
    AUTO_REJECT = auto()
    ISSUE_MESSAGE = auto()
    RAISE_ERROR = auto()
    RAISE_ALARM = auto()


class Trigger(BaseModel):
    '''A Trigger for BuildingBlocks that specifies certain actions to be taken when an application is submitted/filled out.'''
    id: int = -1
    name: str = ""
    triggerType: TriggerType = TriggerType.NONE

    # could contain any type
    triggerArgs: str = ""

    triggerResultType: TriggerResultType = TriggerResultType.NONE
    # contains one or more error messages
    triggerResultArgs: str = ""

    active: bool = True


if __name__ == "__main__":
    pass
