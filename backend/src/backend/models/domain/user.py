from datetime import date
from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserType(str, Enum):
    """
    Enum representing different user types in the system.
    Attributes:
        APPLICANT (str): Represents a user who is an applicant.
        ADMIN (str): Represents a user with administrative privileges.
        REPORTER (str): Represents a user who reports issues or provides feedback.
    """

    APPLICANT = "APPLICANT"  # User is an applicant, citizen who submits applications for registering purposes
    ADMIN = "ADMIN"  # User is an admin, has elevated privileges to process applications, manage users, etc.
    REPORTER = "REPORTER"  # User is a reporter, can view all applications, but cannot process them


class RoleAssignment(BaseModel):
    """
    Represents a role assignment for a user.
    Attributes:
        user_id (int): The unique identifier for the user.
        role (UserType): The role assigned to the user.
        assignment_date (date): The date the role was assigned to the user.
    """

    role: UserType
    assignment_date: date
    user_id: Optional[int] = None


class AccountStatus(str, Enum):
    """
    An enumeration representing the various statuses an account can have.
    Attributes:
        ACTIVE (str): Indicates that the user is active and can log in.
        INACTIVE (str): Indicates that the user has deactivated their account or has been deactivated by an admin.
        REGISTERED (str): Indicates that the user has registered but has not yet activated their account or logged in.
        DEREGISTERED (str): Indicates that the user is effectively deleted but retained for record-keeping purposes.
    """

    ACTIVE = "ACTIVE"  # User is active and can log in
    INACTIVE = (
        "INACTIVE"  # User has deactivated their account or been deactivated by an admin
    )
    REGISTERED = "REGISTERED"  # User has registered but not yet activated their account / logged in
    DEREGISTERED = (
        "DEREGISTERED"  # User is all but deleted, kept for record-keeping purposes
    )

class UserCreatePayload(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: UserType = UserType.APPLICANT

class UserID(BaseModel):
    """Response model containing just the user's ID."""
    id: int

class User(BaseModel):
    """
    Represents a user in the system.
    Attributes:
        id (int): The unique identifier for the user.
        username (str): The username of the user.
        user_type (UserType): The type of the user, indicating their role or permissions.
        date_created (datetime): The timestamp when the user was created.
    """

    id: int | None = None
    username: str
    user_roles: list [RoleAssignment] = []
    date_created: date
    email: EmailStr | None = None
    hashed_password: str
    is_active: bool = True
    # account_status: AccountStatus = AccountStatus.ACTIVE


class UserCreate(User):
    """
    Model for creating a new user, including password validation.
    Attributes:
        password (str): The password for the new user, must be between 8 and 40 characters.
    """

    password: str = Field(min_length=8, max_length=40)


#     "UserCreate",
# "UserRegister",
# "UserUpdate",
# "UpdatePassword"


class UserRegister(BaseModel):
    """
    Model for user registration, including email and password validation.
    Attributes:
        username (str): The desired username for the new user, must be between 3 and 22 characters.
        email (EmailStr): The email address of the new user.
        password (str): The password for the new user, must be between 8 and 40 characters.
    """

    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=40)
    username: str | None = Field(default=None, max_length=255)
    role: UserType = UserType.APPLICANT


class UserUpdate(User):
    email: Optional[EmailStr] = None
    username: Optional[str] = None


class UpdatePassword(BaseModel):
    password: str = Field(min_length=8, max_length=40)
    new_password: str = Field(min_length=8, max_length=40)
    password: str = Field(min_length=8, max_length=40)
    new_password: str = Field(min_length=8, max_length=40)
