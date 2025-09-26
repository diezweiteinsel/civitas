from enum import Enum
from fastapi import FastAPI, Request, Response
from fastapi import APIRouter
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict # to read from .env file
# from core.db import Base, engine
from backend.api import api_router
import backend.core.security as security
import backend.api.endpoints.auth as auth

# Base.metadata.create_all(bind=engine)

# 1. Define a Settings class to hold your configuration variables
class Settings(BaseSettings):
    # This variable will be loaded from the .env file.
    # A default value is provided as a fallback.
    ALLOWED_ORIGINS: str = "http://localhost"

    # Specify the .env file to load
    model_config = SettingsConfigDict(env_file=".env")

# 2. Create instance of the Settings class
settings = Settings()

app = FastAPI(
    title="Civitas API",
    version="0.0.1",
    description="API for Civitas Application Management System",
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc",
    openapi_url="/api/v1/openapi.json"
)

# List of origins that are allowed to make requests
origins = settings.ALLOWED_ORIGINS.split(",")


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Allows all methods
    allow_headers=["*"], # Allows all headers
)

@app.middleware("http")
async def clacks(request: Request, call_next):
    resp: Response = await call_next(request)
    resp.headers.setdefault("X-Clacks-Overhead", "GNU Terry Pratchett")
    return resp

app.include_router(
    api_router,
    prefix="/api/v1"
)

app.include_router(
    auth.router,
    prefix="/api/v1"
)

# engine, Base, session = initialize_session()

