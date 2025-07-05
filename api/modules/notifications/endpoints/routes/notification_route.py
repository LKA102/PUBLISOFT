from fastapi import APIRouter, Depends, Response, HTTPException, status
from fastapi.responses import JSONResponse
from modules.notifications.application.views.notifications_view import NotificationsView
from modules.notifications.endpoints.dependencies import get_message_bus, get_unit_of_work
from modules.notifications.infrastructure.unit_of_work import SqlAlchemyUnitOfWork
from modules.notifications.application.message_bus import MessageBus
from common.exceptions import APIHTTPException
from common.session import SessionLocal
import traceback

router = APIRouter()
# End points GET:
# Definir endpoints para las notificaciones
# Traer todas las notificaciones (leidas + no leidas)
# Traer notificaciones de un usuario
# Traer notificaciones no leidas
# Traer notificaciones leidas

# Endpoints
@router.get("")
def get_all_notifications(uok: SqlAlchemyUnitOfWork = Depends(get_unit_of_work)):
    try:
        with uok:
            notifications_view = NotificationsView(uok.session)
            notifications = notifications_view.get_all_notifications()
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content=notifications
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
    
@router.get("/user/{user_id}")
def get_user_notifications(user_id: str, uok: SqlAlchemyUnitOfWork = Depends(get_unit_of_work)):
    try:
        with uok:
            notifications_view = NotificationsView(uok.session)
            notifications = notifications_view.get_user_notifications(user_id)
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content=notifications
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
    
@router.get("/unread/{user_id}")
def get_unread_notifications(user_id: str, uok: SqlAlchemyUnitOfWork = Depends(get_unit_of_work)):
    try:
        with uok:
            notifications_view = NotificationsView(uok.session)
            notifications = notifications_view.get_unread_notifications(user_id)
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content=notifications
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
    
@router.get("/read/{user_id}")
def get_read_notifications(user_id: str, uok: SqlAlchemyUnitOfWork = Depends(get_unit_of_work)):
    try:
        with uok:
            notifications_view = NotificationsView(uok.session)
            notifications = notifications_view.get_read_notifications(user_id)
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content=notifications
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