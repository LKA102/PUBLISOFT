from modules.posts.domain.entities.base_entity import BaseEntity
from sqlalchemy import Column, DateTime
from sqlalchemy.dialects.postgresql import UUID
import uuid


class BaseEntitySQLAlchemy:
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    @staticmethod
    def base_entity_to_orm(
        entity: BaseEntity, entity_orm: "BaseEntitySQLAlchemy"
    ):
        entity_orm.id = entity.id
        entity_orm.created_at = entity.created_at
        entity_orm.updated_at = entity.updated_at

    @staticmethod
    def orm_to_base_entity(entity_orm):
        return {
            "id": getattr(entity_orm, "id", None),
            "created_at": getattr(entity_orm, "created_at", None),
            "updated_at": getattr(entity_orm, "updated_at", None),
        }
