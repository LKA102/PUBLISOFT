from typing import Set, Optional
from modules.notifications.domain.entities.notification import Notification
from modules.notifications.domain.repositories.interface_notification_repository import INotificationRepository
from modules.notifications.infrastructure.database.models.notification import NotificationSQLAlchemy
from modules.notifications.infrastructure.database.mappers.notification_mapper import NotificationMapper
from uuid import UUID

class NotificationRepositorySQLAlchemy(INotificationRepository):
    def __init__(self, session):
        super().__init__()
        self.session = session

    def _save(self, notification: Notification) -> Notification:
        notification_orm = NotificationMapper.to_orm(notification)
        self.session.add(notification_orm)
        return notification
    
    def _load(self, notification_id: int) -> Optional[Notification]:
        notification_orm = self.session.query(NotificationSQLAlchemy).filter_by(id=notification_id).first()
        if not notification_orm:
            return None
        return NotificationMapper.to_entity(notification_orm)
    
    def _load_all(self) -> Set[Notification]:
        notifications_orm = self.session.query(NotificationSQLAlchemy).all()
        return {NotificationMapper.to_entity(notification_orm) for notification_orm in notifications_orm}
    
    def _update(self, notification: Notification) -> Optional[Notification]:
        # Update directly in the database using session.query().update()
        update_data = {
            "user_emisor_id": notification.user_emisor_id,
            "user_receptor_id": notification.user_receptor_id,
            "title": notification.title,
            "message": notification.message,
            "type": notification.type,
            "leido": notification.leido
        }

        # Perform the update
        rows_updated = self.session.query(NotificationSQLAlchemy).filter_by(id=notification.id).update(update_data)

        # If at least one row was updated, return the updated entity
        if rows_updated:
            updated_notification_orm = self.session.query(NotificationSQLAlchemy).filter_by(id=notification.id).first()
            return NotificationMapper.to_entity(updated_notification_orm)
        else:
            return None