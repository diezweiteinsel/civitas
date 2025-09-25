from backend.models import Base
from sqlalchemy import Table

from sqlalchemy import Column, Integer, String #, Bool
from backend.models import BuildingBlock
from backend.businesslogic.trigger import createTriggerFromDictionary, createDictionaryFromTrigger

def createBuildingBlockFromDictionary(dictionary: dict) -> BuildingBlock:
    block = BuildingBlock()
    block.id = dictionary["id"]
    block.key = dictionary["key"]
    block.label = dictionary["label"]
    block.dataType = dictionary["dataType"]
    block.required = dictionary["required"]
    block.order = dictionary["order"]
    block.constraintsJson = dictionary["constraintsJson"]
    block.triggers = [createTriggerFromDictionary(t) for t in dictionary["triggers"]]
    return block

def createDictionaryFromBuildingBlock(block: BuildingBlock) -> dict:
    dictionary = {}
    dictionary["id"] = block.id
    dictionary["key"] = block.key
    dictionary["label"] = block.label
    dictionary["dataType"] = block.dataType
    dictionary["required"] = block.required
    dictionary["order"] = block.order
    dictionary["constraintsJson"] = block.constraintsJson
    dictionary["triggers"] = [createDictionaryFromTrigger(t) for t in block.triggers]
    return dictionary
