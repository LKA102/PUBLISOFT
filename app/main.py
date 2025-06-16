# Entrypoint of the whole application
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.modules.auth.endpoints.routes import auth_route
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


app.include_router(auth_route.router, prefix="/auth", tags=["auth"])