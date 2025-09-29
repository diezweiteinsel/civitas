# Application model for managing application-related data and logic

from datetime import datetime # stdlib
from enum import StrEnum

from pydantic import BaseModel, Field #3rdparty

from .form import Form #our stuff

class ApplicationStatus(StrEnum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    PUBLIC = "PUBLIC"
    REVISED = "REVISED"



class Application(BaseModel):
    """A class representing an application submitted by a user."""
    id: int | None = None
    user_id: int
    form_id: int
    status: ApplicationStatus = ApplicationStatus.PENDING
    created_at: datetime = Field(default_factory=datetime.now)
    currentSnapshotID: int = -1  # Points to the latest snapshot of the application
    previousSnapshotID: int = -1  # Points to the previous snapshot of the application
    jsonPayload: dict = {}  # The actual data of the application


class ApplicationID(BaseModel):
    id: int


class ApplicationFillout(BaseModel):
    form_id: int
    jsonPayload: dict