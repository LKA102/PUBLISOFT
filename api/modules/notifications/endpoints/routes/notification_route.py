from fastapi import APIRouter, Depends, Response, HTTPException, status
from fastapi.responses import JSONResponse
from modules.notifications.application.views.notifications_view import NotificationsView
from modules.notifications.endpoints.dependencies import get_message_bus, get_unit_of_work
from modules.notifications.infrastructure.unit_of_work import SqlAlchemyUnitOfWork
from modules.notifications.application.message_bus import MessageBus
from common.exceptions import APIHTTPException
from modules.notifications.endpoints.schemas.requests import NotificationCreate, NotificationUpdateLeido
from modules.notifications.domain.commands.notification_commands import CreateNotificationCommand, UpdateNotificationCommand
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
        
@router.post("/create")
def create_notification(notification: NotificationCreate, uok: SqlAlchemyUnitOfWork = Depends(get_unit_of_work), message_bus: MessageBus = Depends(get_message_bus)):
    try:
        with uok:
            # Create the command to create a notification
            command = CreateNotificationCommand(
                user_emisor_id=notification.emisor_id,
                user_receptor_id=notification.receptor_id,
                title=notification.title,
                message=notification.message,
                type_=notification.notification_type
            )
            
            message_bus.handle(command, uok)
            
            return JSONResponse(
                status_code=status.HTTP_201_CREATED,
                content={"detail": "Notification created successfully"}
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

@router.put("/{notification_id}")
def update_notification_leido_status(notification_id: str, notification: NotificationUpdateLeido, uok: SqlAlchemyUnitOfWork = Depends(get_unit_of_work), message_bus: MessageBus = Depends(get_message_bus)):
    try:
        with uok:
            command = UpdateNotificationCommand(
                id=notification_id,
                leido=notification.leido,
                title=None,
                message=None,
                type_=None
            )
            message_bus.handle(command, uok)
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={"detail": "Notification updated successfully"}
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