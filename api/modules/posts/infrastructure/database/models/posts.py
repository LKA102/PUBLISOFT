from common.session import Base

from modules.auth.infrastructure.database.models.base_entity import (
    BaseEntitySQLAlchemy,
)

from sqlalchemy import Column, String, Float
from sqlalchemy.dialects.postgresql import JSONB


class PostSQLAlchemy(Base, BaseEntitySQLAlchemy):
    __tablename__ = "posts"
    __table_args__ = {"schema": "custom_posts"}

    title = Column(String, nullable=False)
    file_url = Column(String, nullable=False)
    category = Column(String, nullable=False)
    type = Column(String, nullable=False)
    scores = Column(JSONB, nullable=False, default=list)
    score_avg = Column(Float, nullable=False)
