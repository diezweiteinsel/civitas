from typing import List, Optional

from pydantic import Field, field_validator
from pydantic_xml import BaseXmlModel, element, attr

"""
<xbiikebrennenExport xmlns="urn:xoev:xbiikebrennen:1.0" version="1.0">



  <!-- Formular-Definition -->

  <formDefinition id="form-biikebrennen-v1" name="Anzeige Biikebrennen">

    <attributes>

      <attribute name="datum" type="date" required="true"/>

      <attribute name="ort" type="string" required="true"/>

      <attribute name="erwartetePersonenzahl" type="number"/>

    </attributes>

  </formDefinition>



</xbiikebrennenExport>
"""

class Attribute(BaseXmlModel, tag="attribute"):
    name: str = attr()
    type: str = attr()
    required: bool = Field(default=False, alias="required")
    visible: Optional[bool] = attr(default=False)

class Attributes(BaseXmlModel, tag="attributes"):
    attributes: List[Attribute] = element(tag="attribute", default=[])

class FormDefinition(BaseXmlModel, tag="formDefinition"):
    id: str = attr()
    name: str = attr()
    attributes: Attributes = element()


