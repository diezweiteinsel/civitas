from backend.models import Base
from sqlalchemy import Table

from backend.models import Trigger
from sqlalchemy import Column, Integer, String #, Bool #TODO: this doesnt seem to exist. Check



def createTriggerFromDictionary(dictionary: dict) -> Trigger:
    trigger = Trigger()
    trigger.id = dictionary["id"]
    trigger.name = dictionary["name"]
    trigger.triggerType = dictionary["triggerType"]
    trigger.triggerArgs = dictionary["triggerArgs"]
    trigger.triggerResultType = dictionary["triggerResultType"]
    trigger.triggerResultArgs = dictionary["triggerResultArgs"]
    trigger.active = dictionary["active"]

    return trigger

def createDictionaryFromTrigger(trigger: Trigger) -> dict:
    return {
        "id": trigger.id,
        "name": trigger.name,
        "triggerType": trigger.triggerType,
        "triggerArgs": trigger.triggerArgs,
        "triggerResultType": trigger.triggerResultType,
        "triggerResultArgs": trigger.triggerResultArgs,
        "active": trigger.active
    }
