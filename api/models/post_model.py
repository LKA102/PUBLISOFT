from sqlalchemy import Column, Float, Integer, String, DateTime, UUID
from database.db import Base
from datetime import datetime, timezone

class PostModel(Base):
    __tablename__ = 'Post'
    
    id_post = Column(Integer, primary_key=True, autoincrement=True)
    id_owner = Column(UUID, unique=True, nullable=False)
    title = Column(String(255), nullable=True)
    post_url = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    description = Column(String(255), nullable=True)
    id_category = Column(Integer, unique=True, nullable=True)
    score = Column(Float, nullable=False)