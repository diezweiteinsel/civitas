from datetime import datetime
from pydantic import BaseModel, ConfigDict
from backend.models.domain.buildingblock import BuildingBlock, BBType
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
	version: str = "1.0"
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

	def to_xml(self) -> str:
		result = '''<x{name}Export xmlns="urn:xoev:x{name}:{version}" version="{version}">
	<!-- Formular-Definition -->
	<formDefinition id="{id}" name="{name}">
		<attributes>'''
		for b in self.blocks.keys():
			result += "\n\t\t\t" + self.blocks.get(b).to_xml()
		result += '''
		</attributes>
	</formDefinition>
</x{name}Export>'''
		return result.format(id=str(self.id), name=self.form_name, version=self.version)

blocks = {
	1: BuildingBlock(label="helpme",data_type=BBType.STRING,required=True,constraintsJson={})
}
example_form = Form(form_name="example",id=-1,blocks=blocks,version="6.9")
print(example_form.to_xml())