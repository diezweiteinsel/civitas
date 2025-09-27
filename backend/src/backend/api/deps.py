# backend/api/deps.py

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from typing import List

from backend.core.security import SECRET_KEY, ALGORITHM
from backend.schemas.token import TokenData

# This should point to your login endpoint
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")

async def get_current_user_payload(token: str = Depends(oauth2_scheme)) -> dict:
    """Decodes the JWT token and returns its payload."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        return payload
    except JWTError:
        raise credentials_exception

class RoleChecker:
    """
    A dependency class that checks if the current user has the required roles.
    Usage:
    
        @app.get("/some-endpoint")
        async def some_endpoint(role_check: None = Depends(RoleChecker(["admin", "user"]))):
            return {"message": "You have access to this endpoint."}
    
    :param allowed_roles: List of roles that are allowed to access the endpoint.
    """
    def __init__(self, allowed_roles: List[str]):
        self.allowed_roles = allowed_roles

    def __call__(self, payload: dict = Depends(get_current_user_payload)):
        roles = payload.get("roles", [])
        
        # Check if there is any overlap between user's roles and allowed roles
        if not set(roles) & set(self.allowed_roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to perform this action."
            )
