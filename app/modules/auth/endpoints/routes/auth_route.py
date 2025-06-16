from fastapi import APIRouter, Depends, Response, HTTPException, status
from fastapi.responses import JSONResponse
from app.modules.auth.endpoints.schemas.requests import UserRegister, UserLogin
#from app.modules.auth.endpoints.schemas.responses import Something
from app.modules.auth.endpoints.dependencies import get_message_bus, get_unit_of_work
from app.modules.auth.infrastructure.unit_of_work import SqlAlchemyUnitOfWork
from app.modules.auth.application.message_bus import MessageBus
from app.common.exceptions import APIHTTPException

router = APIRouter()

@router.post("/register")
def register_user(register_data: UserRegister, response: Response, uok: SqlAlchemyUnitOfWork = Depends(get_unit_of_work), message_bus: MessageBus = Depends(get_message_bus)):
    

@router.post("/login")
def login_user(login_data: UserLogin, response: Response, uok: SqlAlchemyUnitOfWork = Depends(get_unit_of_work), message_bus: MessageBus = Depends(get_message_bus)):
    pass

  