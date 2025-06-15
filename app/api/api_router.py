"""
Here we will define the API routers for the application.
Example:

router = APIRouter()
router.include_router(auth_controller.router, prefix="/auth", tags=["auth"])

""" 
from fastapi import APIRouter
from modules.auth.endpoints.auth_controller import auth_router

router = APIRouter()
router.include_router(auth_router, prefix="/auth", tags=["auth"])