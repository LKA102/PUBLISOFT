from typing import Set, Optional
from modules.auth.domain.entities.user import User
from modules.auth.domain.repositories.interface_user_repository import IUserRepository
from modules.auth.infrastructure.database.models.users import UserSQLAlchemy
from modules.auth.infrastructure.database.mappers.user_mapper import UserMapper
from uuid import UUID

class UserRepositorySQLAlchemy(IUserRepository):
    def __init__(self, session):
        super().__init__()
        self.session = session

    def _save(self, user: User) -> User:
        user_orm = UserMapper.to_orm(user, self.session)
        self.session.add(user_orm)
        return user
    
    def _load(self, user_id: UUID) -> Optional[User]:
        user_orm = self.session.query(UserSQLAlchemy).filter_by(id=user_id).first()
        if not user_orm:
            return None
        return UserMapper.to_entity(user_orm)

    def _load_all(self) -> Set[User]:
        users_orm = self.session.query(UserSQLAlchemy).all()
        return {UserMapper.to_entity(user_orm) for user_orm in users_orm}
    
    def _update(self, user: User) -> Optional[User]:
        user_orm = UserMapper.to_orm(user, self.session)
        existing_user_orm = self.session.query(UserSQLAlchemy).filter_by(id=user.id).first()
        if existing_user_orm:
            existing_user_orm.email = user_orm.email
            existing_user_orm.hash_password = user_orm.hash_password
            existing_user_orm.state = user_orm.state
            existing_user_orm.user_code = user_orm.user_code
            existing_user_orm.role = user_orm.role
            UserSQLAlchemy.base_entity_to_orm(user, existing_user_orm)
            return UserMapper.to_entity(existing_user_orm) # Maybe find a better way to return the updated entity
        else:
            return None
        
    # Here we create extra methods to operate with users.
    def load_by_email(self, email: str) -> Optional[User]:
        user_orm = self.session.query(UserSQLAlchemy).filter_by(email=email).first()
        if not user_orm:
            return None
        user = UserMapper.to_entity(user_orm)
        self.seen.add(user)
        return user