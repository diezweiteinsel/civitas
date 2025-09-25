from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String, Boolean
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from backend.models import Base

class FormNew(Base):
    __tablename__: str = "forms"

    formID: Mapped[int] = mapped_column(primary_key = True)
    name: Mapped[str] = mapped_column(String(30))
    active: Mapped[bool] = mapped_column()

class TriggerNew(Base):
    __tablename__: str = "triggers"

    triggerID: Mapped[int] = mapped_column(primary_key = True)
    blockID: Mapped[int]
    name: Mapped[str] = mapped_column(String(30))
    active: Mapped[bool] = mapped_column()
    triggerType: Mapped[int] = mapped_column()
    triggerResultType: Mapped[int] = mapped_column()
    triggerResultArgs: Mapped[str] = mapped_column()
'''
class TriggerNew(Base):
    __tablename__: str = "triggers"

    triggerID: Mapped[int] = mapped_column(primary_key = True)
    name: Mapped[str] = mapped_column(String(30))
    active: Mapped[bool] = mapped_column()
    triggerType: Mapped[int] = mapped_column()
    triggerResultType: Mapped[int] = mapped_column()
    triggerResultArgs: Mapped[str] = mapped_column()
'''