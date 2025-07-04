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
        # Actualizar directamente en la base de datos usando session.query().update()
        update_data = {
            "email": user.email.value,  # Usar el valor primitivo del VO
            "hash_password": user.hash_password.value,  # Usar el valor primitivo del VO
            "state": user.state.value,  # Enum -> valor primitivo
            "user_code": user.user_code.value,  # Usar el valor primitivo del VO
            "role_id": self.session.query(RoleSQLAlchemy).filter_by(name=user.role.value).first().id if user.role else None
        }

        # Realizar la actualización
        rows_updated = self.session.query(UserSQLAlchemy).filter_by(id=user.id).update(update_data)

        # Confirmar los cambios
        self.session.commit()

        # Si se actualizó al menos una fila, retornar la entidad actualizada
        if rows_updated:
            updated_user_orm = self.session.query(UserSQLAlchemy).filter_by(id=user.id).first()
            return UserMapper.to_entity(updated_user_orm)
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