from fastapi import APIRouter, Depends, Response, HTTPException, status
from fastapi.responses import JSONResponse
from modules.auth.auth_service import AuthService
from domain.repositories.implementations.user_repo import UserRepository
from schemas.auth_schema import UserRegister, UserLogin
from sqlalchemy.orm import Session
from database.db import get_db
from shared.dependencies import getcurrentuser

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login")
def login(login_data: UserLogin, response: Response, db: Session = Depends(get_db)):
    user_repository = UserRepository(db)
    auth_service = AuthService(user_repository)
    try:
        data = auth_service.login_user(
            email=login_data.email,
            password=login_data.password
        )
        
        # Set JWT token for cookies
        # Note: Settings max-age should be used for remember-me functionality
        response.set_cookie(
            key="access_token",
            value=data["access_token"],
            httponly=True,
            max_age=data["expires_in"],
        )
        
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": "Login successful",
                "data": data
                }
            )
    except Exception as e:
        # Change this structure for errors
        print(e.with_traceback())
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )

@router.post("/logout")
def logout(response: Response):
    response.delete_cookie(key="access_token")
    return {"msg": "Logout successful"}

@router.get("/me")
def get_me(loginuser: dict = Depends(getcurrentuser())):
    return loginuser

@router.post("/register")
def register(register_data: UserRegister, db: Session = Depends(get_db)):
    user_repository = UserRepository(db)
    auth_service = AuthService(user_repository)
    
    try:
        user = auth_service.register_user(
            email=register_data.email,
            password=register_data.password,
            role=register_data.role.value
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
        print(e.with_traceback())
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
        