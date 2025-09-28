import pytest
from backend.models import Application
from backend.models.domain.trigger import TriggerType, TriggerResultType, LogicTriggerType, StringTriggerType, IntTriggerType, DateTriggerType, FloatTriggerType
from backend.businesslogic.trigger import evaluateTrigger, evaluateTriggerLogicExpression, evaluateTriggerLogic, evaluateTriggerLogicDate, evaluateTriggerLogicFloat, evaluateTriggerLogicInt, evaluateTriggerLogicString, evaluateTriggerResult

application = Application(
	user_id=-1,
	form_id=-1,
	applicationID=-1,
	jsonPayload={
		"test_int_1": 1,
		"test_int_2": 2,
		"test_int_3": 3,
		"test_int_6": 6,
		"test_int_neg1": -1,
		"test_int_100": 100,
		"test_str_1": "hello world!",
		"test_str_2": "hello mars!",
		"test_str_3": "bye saturn!",
		"test_str_4": "the cake is a lie...",
		"test_str_5": "hello!",
	}
)

test_int_1 = {
	"type": TriggerType.FIELD,
	"body": "test_int_1",
}
test_int_2 = {
	"type": TriggerType.FIELD,
	"body": "test_int_2",
}
test_int_3 = {
	"type": TriggerType.FIELD,
	"body": "test_int_3",
}
test_int_6 = {
	"type": TriggerType.FIELD,
	"body": "test_int_6",
}
test_int_neg1 = {
	"type": TriggerType.FIELD,
	"body": "test_int_neg1",
}
test_int_100 = {
	"type": TriggerType.FIELD,
	"body": "test_int_100",
}

test_str_1 = {
	"type": TriggerType.FIELD,
	"body": "test_str_1",
}
test_str_2 = {
	"type": TriggerType.FIELD,
	"body": "test_str_2",
}
test_str_5 = {
	"type": TriggerType.FIELD,
	"body": "test_str_5",
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

	tests = [
		{
			"intType": IntTriggerType.SMALLER_THAN,
			"body": [0, 1],
			"result": True,
		},
		{
			"intType": IntTriggerType.SMALLER_THAN,
			"body": [1, 0],
			"result": False,
		},
		{
			"intType": IntTriggerType.SMALLER_THAN,
			"body": [0, test_int_1],
			"result": True,
		},
		{
			"intType": IntTriggerType.SMALLER_THAN,
			"body": [test_int_1, test_int_2],
			"result": True,
		},
		{
			"intType": IntTriggerType.SMALLER_OR_EQUALS,
			"body": [test_int_1, test_int_2],
			"result": True,
		},
		{
			"intType": IntTriggerType.SMALLER_OR_EQUALS,
			"body": [test_int_1, 1],
			"result": True,
		},
		{
			"intType": IntTriggerType.SMALLER_OR_EQUALS,
			"body": [test_int_2, test_int_1],
			"result": False,
		},

		{
			"intType": IntTriggerType.BIGGER_THAN,
			"body": [0, 1],
			"result": False,
		},
		{
			"intType": IntTriggerType.BIGGER_THAN,
			"body": [1, 0],
			"result": True,
		},
		{
			"intType": IntTriggerType.BIGGER_THAN,
			"body": [0, test_int_1],
			"result": False,
		},
		{
			"intType": IntTriggerType.BIGGER_THAN,
			"body": [test_int_1, test_int_2],
			"result": False,
		},
		{
			"intType": IntTriggerType.BIGGER_OR_EQUALS,
			"body": [test_int_1, test_int_2],
			"result": False,
		},
		{
			"intType": IntTriggerType.BIGGER_OR_EQUALS,
			"body": [test_int_1, 1],
			"result": True,
		},
		{
			"intType": IntTriggerType.BIGGER_OR_EQUALS,
			"body": [test_int_2, test_int_1],
			"result": True,
		},
		{
			"intType": IntTriggerType.EQUALS,
			"body": [test_int_2, test_int_1],
			"result": False,
		},
		{
			"intType": IntTriggerType.EQUALS,
			"body": [test_int_1, 1],
			"result": True,
		},
		{
			"intType": IntTriggerType.NOT_EQUALS,
			"body": [test_int_2, test_int_1],
			"result": True,
		},
		{
			"intType": IntTriggerType.NOT_EQUALS,
			"body": [test_int_1, 1],
			"result": False,
		},
		{
			"intType": IntTriggerType.IN_RANGE_INCLUSIVE,
			"body": [test_int_1, 0, 2],
			"result": True,
		},
		{
			"intType": IntTriggerType.IN_RANGE_INCLUSIVE,
			"body": [test_int_1, 1, 2],
			"result": True,
		},
		{
			"intType": IntTriggerType.IN_RANGE_INCLUSIVE,
			"body": [test_int_1, 2, 0],
			"result": False,
		},
		{
			"intType": IntTriggerType.IN_RANGE_INCLUSIVE,
			"body": [test_int_1, 2, 1],
			"result": False,
		},
		{
			"intType": IntTriggerType.NOT_IN_RANGE_INCLUSIVE,
			"body": [test_int_1, 0, 2],
			"result": False,
		},
		{
			"intType": IntTriggerType.NOT_IN_RANGE_INCLUSIVE,
			"body": [test_int_1, 1, 2],
			"result": False,
		},
		{
			"intType": IntTriggerType.NOT_IN_RANGE_INCLUSIVE,
			"body": [test_int_1, 2, 0],
			"result": True,
		},
		{
			"intType": IntTriggerType.NOT_IN_RANGE_INCLUSIVE,
			"body": [test_int_1, 2, 1],
			"result": True,
		},
		{
			"intType": IntTriggerType.IN_RANGE_EXCLUSIVE,
			"body": [test_int_1, 0, 2],
			"result": True,
		},
		{
			"intType": IntTriggerType.IN_RANGE_EXCLUSIVE,
			"body": [test_int_1, 1, 2],
			"result": False,
		},
		{
			"intType": IntTriggerType.IN_RANGE_EXCLUSIVE,
			"body": [test_int_1, 2, 0],
			"result": False,
		},
		{
			"intType": IntTriggerType.IN_RANGE_EXCLUSIVE,
			"body": [test_int_1, 2, 1],
			"result": False,
		},
		{
			"intType": IntTriggerType.NOT_IN_RANGE_EXCLUSIVE,
			"body": [test_int_1, 0, 2],
			"result": False,
		},
		{
			"intType": IntTriggerType.NOT_IN_RANGE_EXCLUSIVE,
			"body": [test_int_1, 1, 2],
			"result": True,
		},
		{
			"intType": IntTriggerType.NOT_IN_RANGE_EXCLUSIVE,
			"body": [test_int_1, 2, 0],
			"result": True,
		},
		{
			"intType": IntTriggerType.NOT_IN_RANGE_EXCLUSIVE,
			"body": [test_int_1, 2, 1],
			"result": True,
		},
		{
			"intType": IntTriggerType.DIVISIBLE_BY,
			"body": [test_int_3, 3],
			"result": True,
		},
		{
			"intType": IntTriggerType.DIVISIBLE_BY,
			"body": [test_int_3, 2],
			"result": False,
		},
		{
			"intType": IntTriggerType.NOT_DIVISIBLE_BY,
			"body": [test_int_3, 3],
			"result": False,
		},
		{
			"intType": IntTriggerType.NOT_DIVISIBLE_BY,
			"body": [test_int_3, 2],
			"result": True,
		},
		{
			"intType": IntTriggerType.POSITIVE,
			"body": [test_int_3],
			"result": True,
		},
		{
			"intType": IntTriggerType.POSITIVE,
			"body": [1],
			"result": True,
		},
		{
			"intType": IntTriggerType.POSITIVE,
			"body": [0],
			"result": False,
		},
		{
			"intType": IntTriggerType.POSITIVE,
			"body": [-20],
			"result": False,
		},
		{
			"intType": IntTriggerType.NEGATIVE,
			"body": [test_int_neg1],
			"result": True,
		},
		{
			"intType": IntTriggerType.NEGATIVE,
			"body": [-21],
			"result": True,
		},
		{
			"intType": IntTriggerType.NEGATIVE,
			"body": [0],
			"result": False,
		},
		{
			"intType": IntTriggerType.NEGATIVE,
			"body": [1],
			"result": False,
		},
	]

	for t in tests:
		assert t["result"] == evaluateTriggerLogicInt(
			{
				"type": TriggerType.INT,
				"intType": t["intType"],
				"body": t["body"],
			},
			application
		)

def test_evaluateTriggerLogicFloat():
	pass

def test_evaluateTriggerLogicString():
	tests = [
		{
			"stringType": StringTriggerType.CONTAINS,
			"body": [test_str_1, "hello"],
			"result": True,
		},
		{
			"stringType": StringTriggerType.CONTAINS,
			"body": [test_str_1, "bye"],
			"result": False,
		},
		{
			"stringType": StringTriggerType.CONTAINS_NOT,
			"body": [test_str_1, "hello"],
			"result": False,
		},
		{
			"stringType": StringTriggerType.CONTAINS_NOT,
			"body": [test_str_1, "bye"],
			"result": True,
		},
		{
			"stringType": StringTriggerType.STARTS_WITH,
			"body": [test_str_1, "hello"],
			"result": True,
		},
		{
			"stringType": StringTriggerType.STARTS_WITH,
			"body": [test_str_1, "bye"],
			"result": False,
		},
		{
			"stringType": StringTriggerType.ENDS_WITH,
			"body": [test_str_1, "world!"],
			"result": True,
		},
		{
			"stringType": StringTriggerType.ENDS_WITH,
			"body": [test_str_1, "bye"],
			"result": False,
		},
		{
			"stringType": StringTriggerType.LENGTH_BIGGER_THAN_INT,
			"body": [test_str_1, "1"],
			"result": True,
		},
		{
			"stringType": StringTriggerType.LENGTH_BIGGER_THAN_INT,
			"body": [test_str_1, "100"],
			"result": False,
		},
		{
			"stringType": StringTriggerType.LENGTH_BIGGER_THAN_INT,
			"body": [test_str_1, test_int_1],
			"result": True,
		},
		{
			"stringType": StringTriggerType.LENGTH_BIGGER_THAN_INT,
			"body": [test_str_1, test_int_100],
			"result": False,
		},
		{
			"stringType": StringTriggerType.LENGTH_EQUALS_INT,
			"body": [test_str_5, "6"],
			"result": True,
		},
		{
			"stringType": StringTriggerType.LENGTH_EQUALS_INT,
			"body": [test_str_5, "1"],
			"result": False,
		},
		{
			"stringType": StringTriggerType.LENGTH_EQUALS_INT,
			"body": [test_str_5, test_int_6],
			"result": True,
		},
		{
			"stringType": StringTriggerType.LENGTH_EQUALS_INT,
			"body": [test_str_5, test_int_1],
			"result": False,
		},
		{
			"stringType": StringTriggerType.LENGTH_BIGGER_THAN_STRING,
			"body": [test_str_1, test_str_5],
			"result": True,
		},
		{
			"stringType": StringTriggerType.LENGTH_BIGGER_THAN_STRING,
			"body": [test_str_5, test_str_1],
			"result": False,
		},
		{
			"stringType": StringTriggerType.LENGTH_BIGGER_THAN_STRING,
			"body": ["hello", "bye"],
			"result": True,
		},
		{
			"stringType": StringTriggerType.LENGTH_BIGGER_THAN_STRING,
			"body": ["bye", "hello"],
			"result": False,
		},
		{
			"stringType": StringTriggerType.LENGTH_SMALLER_THAN_STRING,
			"body": [test_str_1, test_str_5],
			"result": False,
		},
		{
			"stringType": StringTriggerType.LENGTH_SMALLER_THAN_STRING,
			"body": [test_str_5, test_str_1],
			"result": True,
		},
		{
			"stringType": StringTriggerType.LENGTH_SMALLER_THAN_STRING,
			"body": ["hello", "bye"],
			"result": False,
		},
		{
			"stringType": StringTriggerType.LENGTH_SMALLER_THAN_STRING,
			"body": ["bye", "hello"],
			"result": True,
		},
		{
			"stringType": StringTriggerType.LENGTH_EQUALS_STRING,
			"body": ["bye", "123"],
			"result": True,
		},
		{
			"stringType": StringTriggerType.LENGTH_EQUALS_STRING,
			"body": ["bye", "1234"],
			"result": False,
		},
		{
			"stringType": StringTriggerType.LENGTH_EQUALS_STRING,
			"body": [test_str_1, "hello world."],
			"result": True,
		},
		{
			"stringType": StringTriggerType.LENGTH_EQUALS_STRING,
			"body": [test_str_1, test_str_2],
			"result": False,
		},
	]

	for t in tests:
		assert t["result"] == evaluateTriggerLogicString(
			{
				"type": TriggerType.STRING,
				"stringType": t["stringType"],
				"body": t["body"],
			},
			application
		)