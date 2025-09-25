""" Handles self-registration of users(Applicants). """
from datetime import date
from backend import db
from backend.models import User, UserType
from backend.auth import hash_password
from backend.businesslogic.user import assign_role

all_Users = []

def register_Applicant(username: str, password: str) -> User:
    id=get_possible_id()
    """ Registers a new user as an Applicant and returns the user ID. """
    new_user = User(id=id,username=username, hashed_password=hash_password(password), date_created=date.today()) 
    assign_role(new_user, UserType.APPLICANT)
    #db.session.add(new_user) # will be activated when integrating with the rest of the app
    #db.session.commit()
    all_Users.append(new_user) # for testing purposes, will be removed later
    return new_user


def get_possible_id() -> int: # current implementation. Needs to be changed when it integrates with the db
    """ Returns a possible user ID for the new user. """
    if not all_Users:
        return 1
    return max(user.id for user in all_Users) + 1 