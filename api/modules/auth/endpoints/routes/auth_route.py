from fastapi import APIRouter, Depends, Response, HTTPException, status
from fastapi.responses import JSONResponse
from modules.auth.endpoints.schemas.requests import UserRegister, UserLogin
#from app.modules.auth.endpoints.schemas.responses import Something
from modules.auth.endpoints.dependencies import get_message_bus, get_unit_of_work
from modules.auth.infrastructure.unit_of_work import SqlAlchemyUnitOfWork
from modules.auth.application.message_bus import MessageBus
from modules.auth.domain.commands.user_commands import RegisterUserCommand, LoginUserCommand
from common.exceptions import APIHTTPException
import traceback

router = APIRouter()

@router.post("/register")
def register_user(
    register_data: UserRegister,
    uok: SqlAlchemyUnitOfWork = Depends(get_unit_of_work),
    message_bus: MessageBus = Depends(get_message_bus)
):
    try:
        # Crear el comando para registrar al usuario
        command = RegisterUserCommand(
            email=register_data.email,
            password=register_data.password,
            name=register_data.name,
            last_name=register_data.last_name
        )

        # Enviar el comando al MessageBus
        message_bus.handle(command, uok)

        # Respuesta exitosa
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={"message": "User registered successfully"}
        )
    except APIHTTPException as e:
        # Manejo de excepciones personalizadas
        print(f"APIHTTPException: {e}")
        return JSONResponse(
            status_code=e.status_code,
            content={"detail": e.detail}
        )
    except Exception as e:
        # Manejo de excepciones genéricas
        print(f"Unexpected error: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "An unexpected error occurred"}
        )

@router.post("/login")
def login_user(login_data: UserLogin, response: Response, uok: SqlAlchemyUnitOfWork = Depends(get_unit_of_work), message_bus: MessageBus = Depends(get_message_bus)):
    try:
        # Crear el comando para iniciar sesión
        command = LoginUserCommand(
            email=login_data.email,
            password=login_data.password
        )

        # Enviar el comando al MessageBus
        result = message_bus.handle(command, uok)
        accesstoken = result[0]

        # Generar cookie de sesión
        response.set_cookie(
            key="accesstoken",
            value=accesstoken,
            httponly=True,
            max_age= 10800, # 3 horas
            expires= 10800
        )

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": "Login successful", "accesstoken": accesstoken}
        )
        
    except APIHTTPException as e:
        # Manejo de excepciones personalizadas
        print(f"APIHTTPException: {e}")
        print(traceback.format_exc())
        return JSONResponse(
            status_code=e.status_code,
            content={"detail": e.detail}
        )
    except Exception as e:
        # Manejo de excepciones genéricas
        print(f"Unexpected error: {e}")
        print(traceback.format_exc())
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "An unexpected error occurred"}
        )
    
@router.post("/logout")
def logout(response: Response):
    response.delete_cookie("accesstoken")
    return {"msg": "Logout successful"}


  