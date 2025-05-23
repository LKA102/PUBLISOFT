from domain.value_objects.email_vo import EmailVO
from enums.role_enum import RoleEnum
from uuid import UUID

class UserEntity:
    def __init__(self, id_user: UUID, email: EmailVO, id_state: int, id_role: int, user_code: str):
        self.id_user = id_user
        self.email = email
        self.id_role = id_role
        self.user_code = user_code
        self.id_state = id_state

    def __str__(self):
        return f"UserEntity(id_user={self.id_user}, email={self.email}, id_state={self.id_state}, id_role={self.id_role}, user_code={self.user_code})"

    def isStudent(self) -> bool:
        return self.id_role == RoleEnum.STUDENT.value
    
    def isAdmin(self) -> bool:
        return self.id_role == RoleEnum.ADMIN.value