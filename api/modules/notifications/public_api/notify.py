from modules.notification.domain.commands.notification_commands import CreateNotificationCommand
from modules.notification.infrastructure.unit_of_work import SqlAlchemyUnitOfWork
from modules.notification.application.message_bus import MessageBus
from common.session import SessionLocal

class NotificationPublicAPI:
    
    def __init__(self):
        self.__uow = SqlAlchemyUnitOfWork(session_factory=SessionLocal)
        self.__message_bus = MessageBus()

    def create_notification(self, title, message, type_, user_emisor_id, user_receptor_id):
        command = CreateNotificationCommand(
            title=title,
            message=message,
            type=type_,
            user_emisor_id=user_emisor_id,
            user_receptor_id=user_receptor_id
        )
        return self.__message_bus.handle(command, uok=self.__uow)
