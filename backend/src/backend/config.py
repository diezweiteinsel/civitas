import os
from dotenv import load_dotenv

load_dotenv() # Loads variables from .env file

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

if not SECRET_KEY:
    raise ValueError("No SECRET_KEY set in .env file")