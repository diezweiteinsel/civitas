from backend.models import (
	User,
	UserType,
)

# --- New authService.py below ---

# backend/businesslogic/services/authService.py

from sqlalchemy.orm import Session
from typing import Optional

from backend.core.security import verify_password
from backend.crud import user as user_crud
from backend.models.orm.usertable import User as OrmUser

def authenticate_user(session: Session, username: str, password: str) -> Optional[OrmUser]:
    """
    Authenticates a user by checking their username and password.

    Args:
        session (Session): The database session.
        username (str): The user's username.
        password (str): The user's plain-text password.

    Returns:
        Optional[OrmUser]: The ORM user object if authentication is successful, otherwise None.
    """
    # 1. Find the user in the database using the CRUD layer
    user = user_crud.get_user_by_name(username=username, session=session)
    if not user:
        return None # User not found

    # 2. Verify the provided password against the stored hash using the security utility
    if not verify_password(password, user.hashed_password):
        return None # Password incorrect

    # 3. If both checks pass, return the user object
    return user
















# --- Remnants of old authService.py below ---

def authenticate(username: str, password: str):
	""" Authenticates a user and returns a token."""
	# Logic to authenticate the user and generate a token is not defined yet
	pass


def createAccount(username: str, password: str):
	""" Creates a new account for a user."""
	# Logic to create a new account is not defined yet
	pass


def changePassword(user: User, old_password: str, new_password: str):
	""" Changes the password for a user's account."""
	# Logic to change the password is not defined yet
	pass


def deactivateAccount(user: User):
	""" Deactivates a user's account."""
	# Logic to deactivate the account is not defined yet
	pass


def assignRole(user: User, account: User, new_role: UserType):
	""" Assigns a new role to a user. Only admins can change roles."""
	if user.usertype != UserType.ADMIN:
		raise PermissionError("Only admins can change user roles.")
	account.usertype = new_role
	# Save the updated account to the database
	pass
