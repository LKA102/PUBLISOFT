from sqlalchemy import Column, Integer, String, DateTime
from database import Base
from datetime import datetime

class RoleModel(Base):
    __tablename__ = 'Role'
    
    id_role = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String(255), unique=True, nullable=False)