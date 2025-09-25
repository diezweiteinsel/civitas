from datetime import datetime
from pydantic import BaseModel, ConfigDict
from .buildingblock import BuildingBlock
from .section import Section

class Form(BaseModel):
    '''A form represents a specific version of a form, with a name and a list of building blocks.'''
    formID: int = -1
    code: str = ""
    title : str = ""
    createdAt: datetime = datetime.now()
    isActive: bool = True
    # json of sections
    sections: list[Section] = [] # might then be unnecessary when having json

