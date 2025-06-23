from pydantic import BaseModel

class UserRegister(BaseModel):
    email: str
    password: str
    name: str
    last_name: str
    
class UserLogin(BaseModel):
    email:  str
    password: str 