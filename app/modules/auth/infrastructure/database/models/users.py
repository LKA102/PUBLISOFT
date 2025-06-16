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

    user_id = Column(UUID, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    hash_password = Column(String(255), nullable=False)
    state = Column(Enum(UserStateEnum), nullable=False)
    role_id = Column(Integer, ForeignKey('custom_auth.Roles.role_id'), nullable=False)
    user_code = Column(String(255), unique=True, nullable=False)

    role = relationship("RoleSQLAlchemy", back_populates="users")  # Assuming RoleSQLAlchemy has a users relationship

    @classmethod
    def entity_to_orm(cls, user: User, session: Session):
        role = session.query(RoleSQLAlchemy).filter_by(name=user.role).first()
        
        user_orm = cls()
        user_orm.user_id = user.user_id
        user_orm.email = user.email.__str__()
        user_orm.hash_password = user.hash_password.__str__()
        user_orm.state = user.state
        user_orm.user_code = user.user_code
        user_orm.role = role

        cls.base_entity_to_orm(user, user_orm)
        return user_orm