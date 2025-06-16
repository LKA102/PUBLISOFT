from typing import Set
from app.modules.auth.domain.entities.user import User
from app.modules.auth.domain.repositories.interface_user_repository import IUserRepository
from app.modules.auth.infrastructure.database.models.users import UserSQLAlchemy
from uuid import UUID

class UserRepositorySQLAlchemy(IUserRepository):
    def __init__(self, session):
        super().__init__()
        self.session = session

    def _save(self, user: User) -> User:
        user_orm = UserSQLAlchemy.entity_to_orm(user, self.session)
        self.session.add(user_orm)
        return user
    
    def _load(self, user_id: UUID) -> User:
        user_orm = self.session.query(UserSQLAlchemy).filter_by(user_id=user_id).first()
        if user_orm:
            return User.from_orm(user_orm)
        return None