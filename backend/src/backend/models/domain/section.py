from pydantic import BaseModel

from backend.models.domain.buildingblock import BuildingBlock


class Section(BaseModel):
    id: int = -1
    name: str = ""
    order: int = -1
    blocks: list[BuildingBlock] = []