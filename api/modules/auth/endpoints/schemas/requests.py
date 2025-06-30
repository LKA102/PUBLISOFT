from pydantic import BaseModel

class UserRegister(BaseModel):
    email: str
    password: str
    name: str
    last_name: str
    role: int = 0 # Default role is Student (0)
    
class UserLogin(BaseModel):
    email:  str
    password: str 