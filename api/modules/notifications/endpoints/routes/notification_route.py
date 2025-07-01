from fastapi import APIRouter, Depends, Response, HTTPException, status
from fastapi.responses import JSONResponse
from api.modules.notifications.application.views.notifications_view import NotificationsView
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


@router.get("/")
def get_all_notifications(
    response: Response
):
    try:
        session = SessionLocal()
        notifications_view = NotificationsView(session)
        result = notifications_view.get_all_notifications()
        session.close()
        return JSONResponse(content=result)
    except Exception as e:
        traceback.print_exc()
        raise APIHTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))