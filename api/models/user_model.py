from sqlalchemy import Column, Integer, String, DateTime
from database import Base
from datetime import datetime

class UserModel(Base):
    __tablename__ = 'User'
    
    id_user = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(datetime.timezone.utc))
    email = Column(String(255), unique=True, nullable=False)
    id_state = Column(Integer, nullable=False)
    id_role = Column(Integer, nullable=False)
    user_code = Column(String(255), unique=True, nullable=False)