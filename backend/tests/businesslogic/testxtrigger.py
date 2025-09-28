from backend.models.domain.trigger import TriggerType, TriggerResultType, LogicTriggerType, StringTriggerType, IntTriggerType, DateTriggerType, FloatTriggerType
from backend.businesslogic.trigger import evaluateTrigger, evaluateTriggerLogicExpression, evaluateTriggerLogic, evaluateTriggerLogicDate, evaluateTriggerLogicFloat, evaluateTriggerLogicInt, evaluateTriggerLogicString, evaluateTriggerResult

example_int_block = {
	"type": TriggerType.INT,
	"intType": IntTriggerType.SMALLER_THAN,
	"body": [
		{
			"type": TriggerType.FIELD,
			"body": "NAME OF FIELD / BLOCK_ID AS INT MAYBE?",
		},
		5,
	],
}

example_dict = {
	"type": TriggerType.IF,
	"header": {
		"type": TriggerType.LOGIC,
		"logicType": LogicTriggerType.AND,
		"body": [
			example_int_block
		],
	}
}

def test_evaluateTrigger():
	pass

def test_evaluateTriggerLogicExpression():
	pass

def test_evaluateTriggerLogic():
	pass

def test_evaluateTriggerLogicDate():
	pass

def test_evaluateTriggerLogicInt():
	pass

def test_evaluateTriggerLogicFloat():
	pass

def test_evaluateTriggerLogicString():
	pass