from fastapi import APIRouter, Depends, Response, HTTPException, status
from fastapi.responses import JSONResponse
from modules.users.endpoints.schemas.requests import UpdateStudentRequest
#from app.modules.auth.endpoints.schemas.responses import Something
from modules.users.endpoints.dependencies import get_message_bus, get_unit_of_work
from modules.users.infrastructure.unit_of_work import SqlAlchemyUnitOfWork
from modules.users.application.message_bus import MessageBus
from modules.users.domain.commands.student_commands import UpdateStudentCommand, DisableStudentCommand
from common.exceptions import APIHTTPException
from uuid import UUID
import traceback

router = APIRouter()

@router.get("/")
def get_students(uok: SqlAlchemyUnitOfWork = Depends(get_unit_of_work)):
    pass

@router.get("/{student_id}")
def get_student(student_id: UUID, uok: SqlAlchemyUnitOfWork = Depends(get_unit_of_work)):
    pass

@router.put("/{student_id}")
def update_student(student_id: UUID, request_data: UpdateStudentRequest, uok: SqlAlchemyUnitOfWork = Depends(get_unit_of_work), message_bus: MessageBus = Depends(get_message_bus)):
    try:
        command = UpdateStudentCommand(id=student_id, **request_data.model_dump())
        message_bus.handle(command, uok=uok)
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
    except APIHTTPException as e:
        return JSONResponse(
            status_code=e.status_code,
            content={"detail": e.detail}
        )
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Internal Server Error"}
        )

@router.delete("/{student_id}")
def delete_student(student_id: UUID, uok: SqlAlchemyUnitOfWork = Depends(get_unit_of_work), message_bus: MessageBus = Depends(get_message_bus)):
    try:
        command = DisableStudentCommand(id=student_id)
        message_bus.handle(command, uok=uok)
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
    except APIHTTPException as e:
        return JSONResponse(
            status_code=e.status_code,
            content={"detail": e.detail}
        )
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Internal Server Error"}
        )