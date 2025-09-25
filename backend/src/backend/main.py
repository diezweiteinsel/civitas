from enum import Enum
from fastapi import FastAPI, Request, Response
from fastapi import APIRouter
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
# from core.db import Base, engine
from backend.api import api_router
import backend.core.security as security
import backend.api.endpoints.auth as auth

# Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Civitas API",
    version="0.0.1",
    description="API for Civitas Application Management System",
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc",
    openapi_url="/api/v1/openapi.json"
)

# List of origins that are allowed to make requests
origins = [
    "http://localhost",
    "http://localhost:3000", # Assuming your React app runs on port 3000
    # Add the production frontend URL here as well
]

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

