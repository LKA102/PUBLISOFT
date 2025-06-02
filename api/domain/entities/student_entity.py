from domain.entities.user_entity import UserEntity
from domain.value_objects.email_vo import EmailVO
from enums.role_enum import RoleEnum
from uuid import UUID


class StudentEntity(UserEntity):
    def __init__(self, id_user: UUID, email: EmailVO, id_state: int, user_code: str):
        super().__init__(id_user, email, id_state, RoleEnum.STUDENT.value, user_code)

    def __str__(self):
        return f"StudentEntity(id_user={self.id_user}, email={self.email}, id_state={self.id_state}, user_code={self.user_code})"
