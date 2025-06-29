from modules.auth.domain.entities.base_entity import BaseEntity
from modules.auth.domain.value_objects.vo import EmailVO, UserCodeVO, PasswordHashVO
from modules.auth.domain.events.user_events import UserCreatedEvent
from typing import List, Optional
import enum
import uuid
from datetime import datetime, timezone

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
        self.__email: EmailVO = kwargs.get('email', "")
        self.__hash_password: PasswordHashVO = kwargs.get('hash_password', "")
        self.__state: UserStateEnum = kwargs.get('state', UserStateEnum.ACTIVE)
        self.__user_code: UserCodeVO = kwargs.get('user_code', "")
        self.__role: UserRoleEnum = kwargs.get('role', UserRoleEnum.STUDENT)
        self.events = set()

    def __eq__(self, other):
        if not isinstance(other, User):
            return False
        return self.id == other.id
    
    def __hash__(self):
        return hash(self.id)

    # region GETTERS AND SETTERS

    @property
    def email(self) -> EmailVO:
        return self.__email
    
    @email.setter
    def email(self, value: EmailVO):
        if not isinstance(value, EmailVO):
            raise ValueError("Email must be an instance of EmailVO")
        self.__email = value

    @property
    def hash_password(self) -> PasswordHashVO:
        return self.__hash_password
    
    @hash_password.setter
    def hash_password(self, value: PasswordHashVO):
        if not isinstance(value, PasswordHashVO):
            raise ValueError("Hash password must be an instance of PasswordHashVO")
        self.__hash_password = value
    
    @property
    def state(self) -> UserStateEnum:
        return self.__state
    
    @state.setter
    def state(self, value: UserStateEnum):
        if not isinstance(value, UserStateEnum):
            raise ValueError("State must be an instance of UserStateEnum")
        self.__state = value
    
    @property
    def user_code(self) -> UserCodeVO:
        return self.__user_code
    
    @user_code.setter
    def user_code(self, value: UserCodeVO):
        if not isinstance(value, UserCodeVO):
            raise ValueError("User code must be an instance of UserCodeVO")
        self.__user_code = value
    
    @property
    def role(self) -> str:
        return self.__role
    
    @role.setter
    def role(self, value: UserRoleEnum):
        if not isinstance(value, UserRoleEnum):
            raise ValueError("Role must be an instance of UserRoleEnum")
        self.__role= value

    # endregion

    @classmethod
    def create(cls, email: EmailVO, hash_password: PasswordHashVO, user_code: UserCodeVO, 
               role: UserRoleEnum = UserRoleEnum.STUDENT, state: UserStateEnum = UserStateEnum.ACTIVE, **extra_data) -> 'User':
        
        # Validations
        if not EmailVO.is_valid_email(email.__str__()):
            raise ValueError(f"Invalid email: {email.email}")
        if not UserCodeVO.is_valid_user_code(user_code.__str__()):
            raise ValueError(f"Invalid user code: {user_code.user_code}")
        if not PasswordHashVO.is_valid_hash_password(hash_password.__str__()):
            raise ValueError("Invalid password hash")
        
        # Generate auto-generated fields
        user_id = uuid.uuid4()
        created_at = updated_at = datetime.now(timezone.utc)

        # Create the User instance
        user = cls(
            id=user_id,
            email=email,
            hash_password=hash_password,
            user_code=user_code,
            role=role,
            state=state,
            created_at=created_at,
            updated_at=updated_at,
        )

        # Emit UserCreated event
        user_create_event = UserCreatedEvent(
            user_id=user.id,
            name=extra_data.get('name'),
            last_name=extra_data.get('last_name')
        )
        user.events.add(user_create_event)

        # Return the created user instance
        return user
