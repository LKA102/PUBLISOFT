from fastapi import APIRouter, Depends, Response, HTTPException, status
from fastapi.responses import JSONResponse
from modules.users.endpoints.schemas.requests import UpdateAdminRequest
from modules.users.application.views.admin_view import AdminView
#from app.modules.auth.endpoints.schemas.responses import Something
from modules.users.endpoints.dependencies import get_message_bus, get_unit_of_work
from modules.users.infrastructure.unit_of_work import SqlAlchemyUnitOfWork
from modules.users.application.message_bus import MessageBus
from modules.users.domain.commands.admin_commands import UpdateAdminCommand, DisableAdminCommand, DisableStudentAccountCommand
from common.exceptions import APIHTTPException
from common.dependencies import getcurrentuser
import traceback
from uuid import UUID

router = APIRouter()

@router.get("")
def get_admins(uok: SqlAlchemyUnitOfWork = Depends(get_unit_of_work)):
    try:
        with uok:
            admin_view = AdminView(uok.session)
            admins = admin_view.get_all_admins()
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content=admins
            )
    except APIHTTPException as e:
        print(f"APIHTTPException: {e}")
        print(traceback.format_exc())
        return JSONResponse(
            status_code=e.status_code,
            content={"detail": e.detail}
        )
    except Exception as e:
        print(f"Unexpected error: {e}")
        print(traceback.format_exc())
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Internal Server Error"}
        )

@router.get("/{admin_id}")
def get_admin(admin_id: UUID, uok: SqlAlchemyUnitOfWork = Depends(get_unit_of_work)):
    try:
        with uok:
            admin_view = AdminView(uok.session)
            admin = admin_view.get_admin_by_id(admin_id)
            if not admin:
                raise APIHTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Admin not found")
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content=admin
            )
    except APIHTTPException as e:
        print(f"APIHTTPException: {e}")
        print(traceback.format_exc())
        return JSONResponse(
            status_code=e.status_code,
            content={"detail": e.detail}
        )
    except Exception as e:
        print(f"Unexpected error: {e}")
        print(traceback.format_exc())
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Internal Server Error"}
        )

@router.put("/{admin_id}")
def update_admin(admin_id: UUID, request_data: UpdateAdminRequest, uok: SqlAlchemyUnitOfWork = Depends(get_unit_of_work), message_bus: MessageBus = Depends(get_message_bus)):
    try:
        command = UpdateAdminCommand(id=admin_id, **request_data.model_dump())
        message_bus.handle(command, uok=uok)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except APIHTTPException as e:
        print(f"APIHTTPException: {e}")
        print(traceback.format_exc())
        return JSONResponse(
            status_code=e.status_code,
            content={"detail": e.detail}
        )
    except Exception as e:
        print(f"Unexpected error: {e}")
        print(traceback.format_exc())
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Internal Server Error"}
        )

@router.delete("/{admin_id}")
def delete_admin(admin_id: UUID, uok: SqlAlchemyUnitOfWork = Depends(get_unit_of_work), message_bus: MessageBus = Depends(get_message_bus)):
    try:
        command = DisableAdminCommand(id=admin_id)
        message_bus.handle(command, uok=uok)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except APIHTTPException as e:
        print(f"APIHTTPException: {e}")
        print(traceback.format_exc())
        return JSONResponse(
            status_code=e.status_code,
            content={"detail": e.detail}
        )
    except Exception as e:
        print(f"Unexpected error: {e}")
        print(traceback.format_exc())
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Internal Server Error"}
        )

@router.delete("/delete-student/{student_id}")
def delete_student(student_id: UUID, admin_id: UUID, uok: SqlAlchemyUnitOfWork = Depends(get_unit_of_work), message_bus: MessageBus = Depends(get_message_bus)):
    try:
        command = DisableStudentAccountCommand(admin_id=admin_id, student_id=student_id)
        message_bus.handle(command, uok=uok)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except APIHTTPException as e:
        print(f"APIHTTPException: {e}")
        print(traceback.format_exc())
        return JSONResponse(
            status_code=e.status_code,
            content={"detail": e.detail}
        )
    except Exception as e:
        print(f"Unexpected error: {e}")
        print(traceback.format_exc())
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Internal Server Error"}
        )