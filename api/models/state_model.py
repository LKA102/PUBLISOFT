from sqlalchemy import Column, Integer, String, DateTime
from database import Base
from datetime import datetime

class StateModel(Base):
    __tablename__ = 'State'
    
    id_state = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String(255), unique=True, nullable=False)