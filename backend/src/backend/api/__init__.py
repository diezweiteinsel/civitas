"""
Endpoint definitions for the API.

This module sets up the main API router and includes sub-routers for different
functional areas such as user management and form handling.

Attributes:
    api_router (APIRouter): The main API router that includes all sub-routers.
    router (APIRouter): The individual routers in each sub-module.

Modules:
    user: Endpoints related to user management.
    form: Endpoints related to form handling (currently commented out).
    application: Endpoints related to application processing (to be implemented).

Functions:
    api_root: Base endpoint for Civitas API v1, providing a welcome message.

"""

from fastapi import APIRouter
from backend.api.endpoints import form, user, application, auth, revision
from backend.api.deps import get_current_user_payload, RoleChecker
from backend.api.health import router as health_router

api_router = APIRouter()

@api_router.get("/api/v1", tags=["root"])
async def api_root():
    """
    Base endpoint for API v1.
    """
    return {"message": "Welcome to Civitas API v1"}



api_router.include_router(user.router)
api_router.include_router(form.router)
api_router.include_router(application.router)
api_router.include_router(auth.router)
api_router.include_router(revision.router)
api_router.include_router(health_router)


# expose deps for testing
from backend.api import deps

__all__ = ["api_router", "deps",
           "get_current_user_payload", "RoleChecker"]