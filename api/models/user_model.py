from sqlalchemy import Column, Integer, String, DateTime
from database import Base
from datetime import datetime

class UserModel(Base):
    __tablename__ = 'User'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
     