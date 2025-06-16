from sqlalchemy import Column, ForeignKey, Enum, Integer, String, DateTime, UUID
from sqlalchemy.orm import relationship
from app.common.session import Base, Session
from app.modules.auth.domain.entities.user import User
from app.modules.auth.domain.entities.user import UserStateEnum
from app.modules.auth.infrastructure.database.models.base_entity import BaseEntitySQLAlchemy
from app.modules.auth.infrastructure.database.models.roles import RoleSQLAlchemy

class UserSQLAlchemy(Base, BaseEntitySQLAlchemy):
    __tablename__ = 'Users'
    __table_args__ = {'schema': 'custom_auth'}

    email = Column(String(255), unique=True, nullable=False)
    hash_password = Column(String(255), nullable=False)
    state = Column(Enum(UserStateEnum), nullable=False)
    role_id = Column(Integer, ForeignKey('custom_auth.Roles.id'), nullable=False)
    user_code = Column(String(255), unique=True, nullable=False)

    role = relationship("RoleSQLAlchemy", back_populates="users")  # Assuming RoleSQLAlchemy has a users relationship