from app.modules.auth.domain.entities.user import User, UserStateEnum, UserRoleEnum
from app.modules.auth.domain.value_objects.vo import EmailVO, UserCodeVO, PasswordHashVO
from app.modules.auth.infrastructure.database.models.users import UserSQLAlchemy
from app.modules.auth.infrastructure.database.models.roles import RoleSQLAlchemy
from app.modules.auth.infrastructure.database.models.base_entity import BaseEntitySQLAlchemy

class UserMapper:
    @staticmethod
    def to_entity(user_orm: UserSQLAlchemy) -> User:
        # Convierte el modelo ORM a la entidad de dominio
        base_kwargs = BaseEntitySQLAlchemy.orm_to_base_entity(user_orm)
        return User(
            email=EmailVO(user_orm.email),
            hash_password=PasswordHashVO(user_orm.hash_password),
            state=UserStateEnum(user_orm.state),
            user_code=UserCodeVO(user_orm.user_code),
            role=UserRoleEnum(user_orm.role) if user_orm.role else None,
            **base_kwargs
        )

    @staticmethod
    def to_orm(user: User, session) -> UserSQLAlchemy:
        role = session.query(RoleSQLAlchemy).filter_by(name=user.role).first()
        user_orm = UserSQLAlchemy()
        user_orm.email = str(user.email)
        user_orm.hash_password = str(user.hash_password)
        user_orm.state = user.state
        user_orm.user_code = str(user.user_code)
        user_orm.role = role
        UserSQLAlchemy.base_entity_to_orm(user, user_orm)
        return user_orm