from modules.notifications.domain.entities.notification import Notification, NotificationTypeEnum
from modules.notifications.infrastructure.database.models.notification import NotificationSQLAlchemy
from modules.notifications.infrastructure.database.models.base_entity import BaseEntitySQLAlchemy


class NotificationMapper:
    @staticmethod
    def to_entity(notification_orm: NotificationSQLAlchemy) -> Notification:
        # Convert the ORM model to the domain entity
        base_kwargs = BaseEntitySQLAlchemy.orm_to_base_entity(notification_orm)
        return Notification(
            user_emisor_id=notification_orm.user_emisor_id,
            user_receptor_id=notification_orm.user_receptor_id,
            title=notification_orm.title,
            message=notification_orm.message,
            type=NotificationTypeEnum(notification_orm.type) if notification_orm.type else None,
            leido=notification_orm.leido,
            **base_kwargs
        )

    @staticmethod
    def to_orm(notification: Notification) -> NotificationSQLAlchemy:
        # Convert the domain entity to the ORM model
        notification_orm = NotificationSQLAlchemy()
        notification_orm.user_emisor_id = notification.user_emisor_id
        notification_orm.user_receptor_id = notification.user_receptor_id
        notification_orm.title = notification.title
        notification_orm.message = notification.message
        notification_orm.type = notification.type
        notification_orm.leido = notification.leido
        BaseEntitySQLAlchemy.base_entity_to_orm(notification, notification_orm)
        return notification_orm