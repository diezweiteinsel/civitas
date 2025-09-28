from backend.models import Base, Application
from sqlalchemy import Table

from backend.models.domain.trigger import TriggerType, LogicTriggerType, StringTriggerType, IntTriggerType, DateTriggerType, FloatTriggerType, TriggerResultType
from sqlalchemy import Column, Integer, String #, Bool #TODO: this doesnt seem to exist. Check

def evaluateTrigger(dictionary: dict, application: Application):

	match(dictionary["type"]):
		case TriggerType.NONE:
			pass

		case TriggerType.RESULT:
			return evaluateTriggerResult(dictionary, application)

		case TriggerType.IF:
			if evaluateTriggerLogic(dictionary["header"], application):
				for b in dictionary["body"]:
					evaluateTrigger(b, application)
			else:
				for b in dictionary["else"]:
					evaluateTrigger(b, application)

		case _:
			pass
			## TODO implement error case handling for incorrect input into evaluateTrigger. Maybe a verify method?
	return None

def evaluateTriggerResult(dictionary: dict, application: Application) -> bool:
	match (dictionary["resultType"]):
		case TriggerResultType.NONE:
			return False
		case _:
			return False

def evaluateTriggerLogic(dictionary: dict, application: Application) -> bool:
	match(dictionary["type"]):
		case TriggerType.LOGIC:
			return evaluateTriggerLogicExpression(dictionary, application)
		case TriggerType.STRING:
			return evaluateTriggerLogicString(dictionary, application)
		case TriggerType.INT:
			return evaluateTriggerLogicInt(dictionary, application)
		case TriggerType.DATE:
			return evaluateTriggerLogicDate(dictionary, application)
		case TriggerType.FLOAT:
			return evaluateTriggerLogicFloat(dictionary, application)
		case _:
			return False

def evaluateTriggerLogicExpression(dictionary: dict, application: Application) -> bool:
	match(dictionary["logicType"]):
		case LogicTriggerType.AND:
			for b in dictionary["body"]:
				if not evaluateTriggerLogic(b, application):
					return False
				return True
		case LogicTriggerType.NAND:
			for b in dictionary["body"]:
				if evaluateTriggerLogic(b, application):
					return False
				return True
		case LogicTriggerType.OR:
			for b in dictionary["body"]:
				if evaluateTriggerLogic(b, application):
					return True
			return False
		case LogicTriggerType.NOR:
			for b in dictionary["body"]:
				if not evaluateTriggerLogic(b, application):
					return True
			return False
		case LogicTriggerType.NOT:
			return not evaluateTriggerLogic(dictionary["body"], application)
		case LogicTriggerType.XOR:
			return not (evaluateTriggerLogic(dictionary["body"][0], application) == evaluateTriggerLogic(dictionary["body"][1], application))
		case LogicTriggerType.EQUALS:
			return evaluateTriggerLogic(dictionary["body"][0], application) == evaluateTriggerLogic(dictionary["body"][1], application)
	return False

def evaluateTriggerLogicString(dictionary: dict, application: Application) -> bool:
	match(dictionary["stringType"]):
		case _:
			return False

def getIntValue(var, application: Application) -> int:
	if isinstance(var, int):
		return var
	elif var["type"] == TriggerType.FIELD:
		# TODO get actual data from application via block name / id
		blockIDorName = var["body"]
		return -1
	return -1

def evaluateTriggerLogicInt(dictionary: dict, application: Application) -> bool:

	values: list[int] = [getIntValue(b, application) for b in dictionary["body"]]

	match(dictionary["intType"]):
		case IntTriggerType.SMALLER_THAN:
			return values[0] < values[1]
		case IntTriggerType.SMALLER_OR_EQUALS:
			return values[0] <= values[1]
		case IntTriggerType.BIGGER_THAN:
			return values[0] > values[1]
		case IntTriggerType.BIGGER_OR_EQUALS:
			return values[0] >= values[1]
		case IntTriggerType.EQUALS:
			return values[0] == values[1]
		case IntTriggerType.NOT_EQUALS:
			return values[0] != values[1]
		case IntTriggerType.IN_RANGE_INCLUSIVE:
			return values[1] <= values[0] <= values[2]
		case IntTriggerType.NOT_IN_RANGE_INCLUSIVE:
			return not (values[1] <= values[0] <= values[2])
		case IntTriggerType.IN_RANGE_EXCLUSIVE:
			return values[1] < values[0] < values[2]
		case IntTriggerType.NOT_IN_RANGE_EXCLUSIVE:
			return not (values[1] < values[0] < values[2])
		case IntTriggerType.DIVISIBLE_BY:
			return (values[0] % values[1]) == 0
		case IntTriggerType.NOT_DIVISIBLE_BY:
			return (values[0] % values[1]) != 0
		case IntTriggerType.POSITIVE:
			return values[0] > 0
		case IntTriggerType.NEGATIVE:
			return values[0] < 0
		case _:
			return False

def evaluateTriggerLogicDate(dictionary: dict, application: Application) -> bool:
	match(dictionary["dateType"]):
		case _:
			return False

def evaluateTriggerLogicFloat(dictionary: dict, application: Application) -> bool:
	match(dictionary["floatType"]):
		case _:
			return False


# 1) neue branch auf Civitas
# 2) alle relikte entfernen, damits keine importerrors gibt
# 3) für die existierenden triggertypen / logiken tests schreiben
# 4) ganz wichtig: tests schreiben und zum PYTEST laufen bekommen.
# -> docstrings & kommentare schreiben!
