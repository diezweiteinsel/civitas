
from sqlalchemy import Column, Integer, String, Date, Boolean

from backend.models.orm.usertable import SchemaBase




class OrmForm(SchemaBase):
    __tablename__ = "form_table"
    table_id = Column(Integer, primary_key=True)
    table_name = Column(String, nullable=False)
    created_at = Column(Date, nullable=False)
    is_active = Column(Boolean, default=True)
    xoev = Column(String, nullable=False)
