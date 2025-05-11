from pydantic import BaseModel
from enums.role_enum import RoleEnum

class UserRegister(BaseModel):
    email: str
    password: str
    role: RoleEnum