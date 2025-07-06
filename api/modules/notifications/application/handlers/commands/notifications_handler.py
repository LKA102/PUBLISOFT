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
                message=command.message,
                type=command.type,
                user_emisor_id=command.user_emisor_id,
                user_receptor_id=command.user_receptor_id,
                leido=False
            )

            # Persist the notification entity
            uok.notification_repository.save(notification)
            uok.commit()
            
    @staticmethod
    def handle_update_notification(command: UpdateNotificationCommand, uok: SqlAlchemyUnitOfWork):
        with uok:
            # Retrieve the existing notification
            notification = uok.notification_repository.load(command.id)
            if not notification:
                raise ValueError(f"Notification with id {command.id} not found")
            
            # If title or message are provided, update them as well
            if command.title is not None:
                notification.title = command.title
            if command.message is not None:
                notification.message = command.message
            if command.type is not None:
                notification.type = command.type
            if command.leido is not None:
                notification.leido = command.leido
            

            # Persist the updated notification entity
            uok.notification_repository.update(notification)
            uok.commit()