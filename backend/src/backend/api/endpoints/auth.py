# backend/api/endpoints/auth.py

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from backend.core import db
from backend.schemas.token import TokenResponse
from backend.businesslogic.services import authService
from backend.core.security import create_access_token

router = APIRouter()

@router.post("/auth/token", response_model=TokenResponse, tags=["Auth"])
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(db.get_session_dep)
):
    # This calls the business logic to authenticate the user
    user = authService.authenticate_user(
        session, form_data.username, form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    roles = [role.role.value for role in user.user_roles]
    # If authentication is successful, create the JWT
    token_data = {"sub": user.username, "roles": roles}
    access_token = create_access_token(data=token_data)

    return {"access_token": access_token, "token_type": "bearer", "roles": roles}
