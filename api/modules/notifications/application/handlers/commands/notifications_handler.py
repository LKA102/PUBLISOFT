from modules.notifications.domain.commands.notification_commands import *
from modules.notifications.domain.entities.notification import Notification
from modules.notifications.infrastructure.unit_of_work import SqlAlchemyUnitOfWork
from config.settings import settings

class NotificationCommandHandler:

    @staticmethod
    def handle_create_notification(command: CreateNotificationCommand, uok: SqlAlchemyUnitOfWork):
        with uok:
            # Create the notification entity
            notification = Notification.create(
                title=command.title,
                content=command.content,
                recipient=command.recipient,
                type=command.type,
                status=command.status
            )

            # Persist the notification entity
            uok.notification_repository.save(notification)
            uok.commit()