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
from uuid import UUID

router = APIRouter()

@router.get("/admins")
def get_students(uok: SqlAlchemyUnitOfWork = Depends(get_unit_of_work)):
    pass

@router.get("/admins/{admin_id}")
def get_student(admin_id: UUID, uok: SqlAlchemyUnitOfWork = Depends(get_unit_of_work)):
    pass

@router.post("/admins")
def create_student(uok: SqlAlchemyUnitOfWork = Depends(get_unit_of_work), message_bus: MessageBus = Depends(get_message_bus)):
    pass

@router.put("/admins/{admin_id}")
def update_student(admin_id: UUID, uok: SqlAlchemyUnitOfWork = Depends(get_unit_of_work), message_bus: MessageBus = Depends(get_message_bus)):
    pass

@router.delete("/admins/{admin_id}")
def delete_student(admin_id: UUID, uok: SqlAlchemyUnitOfWork = Depends(get_unit_of_work), message_bus: MessageBus = Depends(get_message_bus)):
    pass