from datetime import datetime
from pydantic import BaseModel, ConfigDict
from .buildingblock import BuildingBlock
from .section import Section
from backend.models.orm.formtable import OrmForm


class FormCreate(BaseModel):
    form_name : str = ""
    blocks: dict[int, BuildingBlock] = {} # key is the order of the block in the form

    def toForm(self):
        form = Form(id = None, form_name=self.form_name, blocks=self.blocks)
        return form

class Form(BaseModel):
    '''A form represents a specific version of a form, with a name and a list of building blocks.'''



    id: int | None = None
    form_name : str = ""
    blocks: dict[int, BuildingBlock] = {} # key is the order of the block in the form
    #triggers: dict[int, Trigger] = {} # key is the order of the trigger in the form

    # These are unnecessary not implemented fields for now
    #code: str = "", createdAt: datetime = datetime.now(), isActive: bool = True

    
    def to_json(self) -> str:
        return self.model_dump_json(indent=2)

    @classmethod
    def from_json(cls, json_str: str) -> "Form":
        return cls.model_validate_json(json_str)
    
    

    @classmethod
    def from_orm_model(cls, orm_model: OrmForm) -> "Form":
        form = cls.from_json(orm_model.xoev)
        if orm_model.id is not None:
            form.id = orm_model.id
        if orm_model.form_name:
            form.form_name = orm_model.form_name
        return form
    
    def to_orm_model(self) -> OrmForm:
        ormForm = OrmForm(
            form_name =self.form_name,
            xoev = self.to_json()
        )
        return ormForm