# Application model for managing application-related data and logic

from datetime import datetime # stdlib
from enum import Enum

from pydantic import BaseModel #3rdparty

from .form import Form #our stuff

class ApplicationStatus(Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    PUBLIC = "PUBLIC"
    REVISED = "REVISED"



class Application(BaseModel):
    """A class representing an application submitted by a user."""
    applicationID: int = -1
    userID: int = -1
    formID: int = -1
    status: ApplicationStatus = ApplicationStatus.PENDING
    createdAt: datetime = datetime.now()
    currentSnapshotID: int = -1  # Points to the latest snapshot of the application
    previousSnapshotID: int = -1  # Points to the previous snapshot of the application
    jsonPayload: dict = {}  # The actual data of the application

