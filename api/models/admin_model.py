from sqlalchemy import Column, Integer, String, DateTime
from database.db import Base
from datetime import datetime

class AdminModel(Base):
    __tablename__ = 'Administrator'
    
    id_admin = Column(Integer, primary_key=True, autoincrement=True)
    id_user = Column(Integer, unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)