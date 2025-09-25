# auth.py


# imports

from datetime import datetime, timedelta
from typing import Annotated, Optional
from fastapi import Depends, HTTPException, APIRouter
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from argon2 import PasswordHasher
import os
from dotenv import load_dotenv


from backend.models import User, UserType

ph = PasswordHasher()




#----- Password Hashing -----

def hash_password(password: str) -> str:
    """
    Hashes a plain text password.

    This function takes a plain text password as input and returns a hashed version
    of the password using a secure hashing algorithm.

    Args:
        password (str): The plain text password to be hashed.

    Returns:
        str: The hashed password.
    """
    return ph.hash(password)

def verify_password(hashed_password: str, plain_password: str) -> bool:
    """
    Verify a plain password against a hashed password.

    Args:
        plain_password (str): The plain text password to verify.
        hashed_password (str): The hashed password to compare against.

    Returns:
        bool: True if the plain password matches the hashed password, False otherwise.
    """
    return ph.verify(hashed_password, plain_password)



#---- API authentication with JWT ----

router = APIRouter(
    prefix="/auth",
    tags=["auth"])

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY") # it is a quite silly one right now, PLEASE CHANGE
ALGORITHM = os.getenv("ALGORITHM")

if not SECRET_KEY or not ALGORITHM:
    raise RuntimeError("SECRET_KEY and ALGORITHM must be set in the .env file")

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="token")

class CreateUserRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str


#----- Example Usage ----
def example_usage():
    secret_password = "mysecretpassword"
    hashed = hash_password(secret_password)
    print(f"Plain Password: {secret_password}")
    print(f"Hashed Password: {hashed}")
    is_valid = verify_password(hashed, secret_password)
    print(f"Password is valid: {is_valid}")


if __name__ == "__main__":
    print("This module is not intended to be run directly.")
    print("Here is an example usage of the functions:")
    example_usage()
