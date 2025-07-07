from sqlalchemy import Column, Boolean, Integer, String, Enum, Float
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from modules.ranking.infrastructure.database.models.base_entity import BaseEntitySQLAlchemy
from common.session import Base

# This model does not inherit from BaseEntitySQLAlchemy because it does not need the created_at and updated_at fields.
class RankingSQLAlchemy(Base, BaseEntitySQLAlchemy):
    __tablename__ = 'ranking'
    __table_args__ = {'schema': 'custom_ranking'}
    
    period = Column(String(8), nullable=False)
    score = Column(Float, nullable=False)
    student_id = Column(UUID(as_uuid=True), nullable=False)
    year = Column(String(4), nullable=False)
    month = Column(String(10), nullable=False)