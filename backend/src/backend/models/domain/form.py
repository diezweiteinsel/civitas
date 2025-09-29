import re

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
	is_active: bool = True
	version: str = "1.0"

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
			form.form_name = orm_model.form_name
			form.is_active = orm_model.is_active
		return form
    
	def to_orm_model(self) -> OrmForm:
		ormForm = OrmForm(
			form_name =self.form_name,
			is_active = self.is_active,
			xoev = self.to_json()
		)
		return ormForm

	@classmethod
	def from_xml(cls, xml: str) -> "Form":
		form = Form()

		#id_match = re.search(r'id="([^"]+)"', xml)
		#form.id = int(id_match.group(1)) if id_match else -1

		version_match = re.search(r'version="([^"]+)"', xml)
		form.version = str(version_match.group(1)) if version_match else "1.0"

		name_match = re.search(r'name="([^"]+)"', xml)
		form.form_name = str(name_match.group(1)) if name_match else "UnknownForm"

		all_blocks_match = re.findall(r'<attribute name="(?P<name>[^"]+)" type="(?P<type>[^"]+)" required="(?P<required>[^"]+)"/>', xml)
		counter: int = 0
		for match in all_blocks_match:
			block = BuildingBlock()
			block.label = match[0]
			block.data_type = str(match[1]).upper()
			block.required = bool(match[2])
			form.blocks[counter] = block
			counter += 1

		return form

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

#blocks = {
#	1: BuildingBlock(label="helpme",data_type=BBType.STRING,required=True,constraintsJson={})
#}
#example_form = Form(form_name="example",id=-1,blocks=blocks,version="6.9")
#print(example_form.to_xml())
#print("again")
#print(Form.from_xml(example_form.to_xml()).to_xml())

