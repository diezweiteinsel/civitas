from backend.models import (
	User,
	UserType,

)

def authenticate(username: str, password: str):
	""" Authenticates a user and returns a token."""
	# Logic to authenticate the user and generate a token is not defined yet
	pass


def creatAccount(username: str, password: str):
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

