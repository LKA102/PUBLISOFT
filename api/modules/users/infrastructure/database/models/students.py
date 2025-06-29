from sqlalchemy import Column, String
from common.session import Base
from modules.users.infrastructure.database.models.base_entity import BaseEntitySQLAlchemy

class StudentSQLAlchemy(Base, BaseEntitySQLAlchemy):
    __tablename__ = "Students"
    __table_args__ = {"schema": "custom_users"}

    name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    profile_image_path = Column(String(255), nullable=True)
    career = Column(String(255), nullable=True)
    faculty = Column(String(255), nullable=True)
    
    