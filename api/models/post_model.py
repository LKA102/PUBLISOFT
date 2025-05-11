from sqlalchemy import Column, Float, Integer, String, DateTime
from database import Base
from datetime import datetime

class PostModel(Base):
    __tablename__ = 'Post'
    
    id_post = Column(Integer, primary_key=True, autoincrement=True)
    id_owner = Column(Integer, unique=True, nullable=False)
    title = Column(String(255), nullable=True)
    post_url = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(datetime.timezone.utc))
    description = Column(String(255), nullable=True)
    id_category = Column(Integer, unique=True, nullable=True)
    score = Column(Float, nullable=False)