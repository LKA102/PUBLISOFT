from app.modules.auth.domain.entities.base_entity import BaseEntity
from typing import List, Optional
from app.modules.auth.domain.value_objects.vo import EmailVO, UserCodeVO, PasswordHashVO
import enum

class UserStateEnum(str, enum.Enum):
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"
    DELETED = "DELETED"

class UserRoleEnum(str, enum.Enum):
    ADMIN = "ADMIN"
    STUDENT = "STUDENT"


class User(BaseEntity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__email: EmailVO = kwargs.get('email')
        self.__hash_password: PasswordHashVO = kwargs.get('hash_password')
        self.__state: UserStateEnum = kwargs.get('state', UserStateEnum.ACTIVE)
        self.__user_code: UserCodeVO = kwargs.get('user_code')
        self.__role: UserRoleEnum = kwargs.get('role', UserRoleEnum.STUDENT)
        self.events = set()

    def __eq__(self, other):
        if not isinstance(other, User):
            return False
        return self.id == other.id
    
    def __hash__(self):
        return hash(self.id)

    @property
    def email(self) -> EmailVO:
        return self.__email
    
    @email.setter
    def email(self, value: EmailVO):
        if not isinstance(value, EmailVO):
            raise ValueError("Email must be an instance of EmailVO")
        self.__email = value
        self._update()  # Update the entity when email changes  

    @property
    def hash_password(self) -> PasswordHashVO:
        return self.__hash_password
    
    @hash_password.setter
    def hash_password(self, value: PasswordHashVO):
        if not isinstance(value, PasswordHashVO):
            raise ValueError("Hash password must be an instance of PasswordHashVO")
        self.__hash_password = value
        self._update()
    
    @property
    def state(self) -> UserStateEnum:
        return self.__state
    
    @state.setter
    def state(self, value: UserStateEnum):
        if not isinstance(value, UserStateEnum):
            raise ValueError("State must be an instance of UserStateEnum")
        self.__state = value
        self._update()
    
    @property
    def user_code(self) -> UserCodeVO:
        return self.__user_code
    
    @user_code.setter
    def user_code(self, value: UserCodeVO):
        if not isinstance(value, UserCodeVO):
            raise ValueError("User code must be an instance of UserCodeVO")
        self.__user_code = value
        self._update()
    
    @property
    def role(self) -> str:
        return self.__role
    
    @role.setter
    def role(self, value: UserRoleEnum):
        if not isinstance(value, UserRoleEnum):
            raise ValueError("Role must be an instance of UserRoleEnum")
        self.__role= value
        self._update()
