from pydantic import BaseModel, ConfigDict
from enum import IntEnum, auto


class TriggerType(IntEnum):
	NONE = 0
	RESULT = auto()
	IF = auto()
	LOGIC = auto()
	STRING = auto()
	INT = auto()
	DATE = auto()
	FLOAT = auto()

class LogicTriggerType(IntEnum):
	NONE = 0
	AND = auto()
	NAND = auto()
	OR = auto()
	NOR = auto()
	NOT = auto()
	XOR = auto()
	EQUALS = auto()

class StringTriggerType(IntEnum):
	NONE = 0
	CONTAINS = 1
	CONTAINS_NOT = auto()
	STARTS_WITH = auto()
	ENDS_WITH = auto()
	LENGTH_BIGGER_THAN = auto()
	LENGTH_SMALLER_THAN = auto()

class IntTriggerType(IntEnum):
	NONE = 0
	SMALLER_THAN = 1
	BIGGER_THAN = auto()
	EQUALS = auto()

class DateTriggerType(IntEnum):
	NONE = 0
	IS_BEFORE = 1

class FloatTriggerType(IntEnum):
	NONE = 0
	SMALLER_THAN = 1
	BIGGER_THAN = auto()
	EQUALS = auto()

class TriggerResultType(IntEnum):
	NONE = 0
	RAISE_FLAG = auto()
	AUTO_REJECT = auto()
	ISSUE_MESSAGE = auto()
	RAISE_ERROR = auto()
	RAISE_ALARM = auto()

if __name__ == "__main__":
	pass
