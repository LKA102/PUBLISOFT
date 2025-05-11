from sqlalchemy import Column, Integer, String, DateTime
from database.db import Base
from datetime import datetime

class StudentModel(Base):
    __tablename__ = 'Student'
    
    id_student = Column(Integer, primary_key=True, autoincrement=True)
    id_user = Column(Integer, unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)