from backend.businesslogic.buildingblock import createDictionaryFromBuildingBlock, createBuildingBlockFromDictionary
from backend.models import Section

def createSectionFromDictionary(dictionary: dict) -> Section:
    section = Section()
    section.id = dictionary["id"]
    section.name = dictionary["name"]
    section.order = dictionary["order"]
    section.blocks = [createBuildingBlockFromDictionary(b) for b in dictionary["blocks"]]
    return section

def createDictionaryFromSection(section: Section) -> dict:
    return {
        "id": section.id,
        "name": section.name,
        "order": section.order,
        "blocks": [createDictionaryFromBuildingBlock(b) for b in section.blocks]
    }