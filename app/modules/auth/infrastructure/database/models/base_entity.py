from app.modules.auth.domain.entities.base_entity import BaseEntity
from sqlalchemy import Column, DateTime

class BaseEntitySQLAlchemy:
    """
    Base class for all entities in the application.
    This class provides a common interface for all entities.
    It can be extended by other entity classes to add common functionality.
    """

    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    @staticmethod
    def base_entity_to_orm(entity: BaseEntity, entity_orm):
        entity_orm.created_at = entity.created_at
        entity_orm.updated_at = entity.updated_at