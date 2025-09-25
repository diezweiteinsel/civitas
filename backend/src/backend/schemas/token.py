# backend/schemas/token.py
"""
Schemas for token responses and data.
"""

from pydantic import BaseModel
from typing import Optional

class TokenResponse(BaseModel):
    """
    access_token: The JWT access token (i.e. "ghuoshfdsgqwhudasodhgoihsaiqa") -> a string you need to store and send in the Authorization header
    token_type: The type of token, typically "bearer"
    roles: The roles assigned to the user (e.g. ["ADMIN", "USER"])
    """
    access_token: str
    token_type: str
    roles: list[str]

class TokenData(BaseModel):
    username: Optional[str] = None
