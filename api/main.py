# Entrypoint of the whole application
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from modules.auth.endpoints.routes import auth_route
from common.session import engine, Base

app = FastAPI()

# Create tables if it does not exist
Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


app.include_router(auth_route.router, prefix="/auth", tags=["auth"])