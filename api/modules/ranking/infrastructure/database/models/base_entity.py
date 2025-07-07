from modules.ranking.domain.entities.base_entity import BaseEntity
from sqlalchemy import Column, DateTime
from sqlalchemy.dialects.postgresql import INTEGER
import uuid

class BaseEntitySQLAlchemy:
    """
    Base class for all entities in the application.
    This class provides a common interface for all entities.
    It can be extended by other entity classes to add common functionality.
    """

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, nullable=False)

    @staticmethod
    def base_entity_to_orm(entity: BaseEntity, entity_orm: 'BaseEntitySQLAlchemy'):
        if entity.id is not None:
            entity_orm.id = entity.id
        entity_orm.created_at = entity.created_at

    @staticmethod
    def orm_to_base_entity(entity_orm):
        return {
            'id': getattr(entity_orm, 'id', None),
            'created_at': getattr(entity_orm, 'created_at', None)
        }