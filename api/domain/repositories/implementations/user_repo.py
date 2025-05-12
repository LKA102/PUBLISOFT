from sqlalchemy.orm import Session
from models.user_model import UserModel
from domain.entities.user_entity import UserEntity
from domain.value_objects.email_vo import EmailVO
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
        
    def get_by_email(self, email: str) -> UserEntity:
        user_model = self.db.query(UserModel).filter(UserModel.email == email).first()
        if user_model:
            return UserEntity(
                id_user=user_model.id_user,
                email=EmailVO(user_model.email),
                id_role=user_model.id_role,
                user_code=user_model.user_code,
                id_state=user_model.id_state
            )
        return None