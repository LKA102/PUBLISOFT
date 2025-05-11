from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from modules.auth.auth_service import AuthService
from domain.repositories.implementations.user_repo import UserRepository
from schemas.auth_schema import UserRegister
from sqlalchemy.orm import Session
from database.db import get_db

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login")
def login():
    pass

@router.post("/logout")
def logout():
    pass

@router.get("/me")
def get_me():
    pass

@router.post("/register")
def register(register_data: UserRegister, db: Session = Depends(get_db)):
    user_repository = UserRepository(db)
    auth_service = AuthService(user_repository)
    
    try:
        user = auth_service.register_user(
            email=register_data.email,
            password=register_data.password,
            role=register_data.role
        )
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "message": "User registered successfully",
                "user": {
                    "id_user": user.id_user,
                    "email": str(user.email),
                    "role": user.id_role,
                }
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
        