from sqlalchemy.orm import Session
from models.user_model import UserModel
from domain.entities.user_entity import UserEntity
from domain.repositories.interfaces.user_interface_repo import UserRepositoryInterface

class UserRepository(UserRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    def save(self, user: UserEntity) -> None:
        user_model = UserModel(
            id_user=user.id_user,
            email=str(user.email),
            id_role=user.id_role,
            user_code=user.user_code,
        )
        self.db.add(user_model)
        self.db.commit()