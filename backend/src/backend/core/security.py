# backend/core/security.py

import os
from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import jwt
from argon2 import PasswordHasher

from backend.config import SECRET_KEY, ALGORITHM

# --- Configuration & Setup ---

ACCESS_TOKEN_EXPIRE_MINUTES = 180 # 3 hours minus the difference that our app thinks its stuck in london
ph = PasswordHasher()

# --- Security Functions ---
def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return ph.verify(hashed_password, plain_password)
    except Exception:
        return False

def hash_password(password: str) -> str:
    return ph.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
