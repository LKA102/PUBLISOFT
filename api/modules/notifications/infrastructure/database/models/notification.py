from sqlalchemy import Column, Boolean, Integer, String, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from modules.notifications.infrastructure.database.models.base_entity import BaseEntitySQLAlchemy
from modules.notifications.domain.entities.notification import NotificationTypeEnum
from common.session import Base

# This model does not inherit from BaseEntitySQLAlchemy because it does not need the created_at and updated_at fields.
class NotificationSQLAlchemy(Base, BaseEntitySQLAlchemy):
    __tablename__ = 'notificaciones'
    __table_args__ = {'schema': 'custom_notification'}

    user_emisor_id = Column(UUID(as_uuid=True), nullable=False)
    user_receptor_id = Column(UUID(as_uuid=True), nullable=False)
    title = Column(String(255), nullable=True)
    message = Column(String(255), nullable=True)
    type = Column(Enum(NotificationTypeEnum), nullable=True)
    leido = Column(Boolean, nullable=True)



