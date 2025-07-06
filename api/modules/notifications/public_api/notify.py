from modules.notifications.domain.commands.notification_commands import CreateNotificationCommand
from modules.notifications.infrastructure.unit_of_work import SqlAlchemyUnitOfWork
from modules.notifications.application.message_bus import MessageBus
from common.session import SessionLocal

class NotificationPublicAPI:
    
    def __init__(self):
        self.__uow = SqlAlchemyUnitOfWork(session_factory=SessionLocal)
        self.__message_bus = MessageBus()

    def create_notification(self, notification_data):
        command = CreateNotificationCommand(
            title=notification_data.get("title"),
            message=notification_data.get("message"),
            type=notification_data.get("type"),
            user_emisor_id=notification_data.get("user_emisor_id"),
            user_receptor_id=notification_data.get("user_receptor_id")
        )
        return self.__message_bus.handle(command, uok=self.__uow)
