from sqlalchemy import Column, Integer, String, DateTime
from database.db import Base
from datetime import datetime
from enums.state_enum import StateEnum

class UserModel(Base):
    __tablename__ = 'User'
    
    id_user = Column(Integer, primary_key=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(datetime.timezone.utc))
    email = Column(String(255), unique=True, nullable=False)
    id_state = Column(Integer, default=StateEnum.ACTIVO.value, nullable=False)
    id_role = Column(Integer, nullable=False)
    user_code = Column(String(255), unique=True, nullable=False)