from pydantic import BaseModel, EmailStr, Field
from typing import Optional


# region Student requests schemas
class UpdateStudentRequest(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=50)
    last_name: Optional[str] = Field(None, min_length=1, max_length=50)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=1)
    faculty: Optional[str] = Field(None, min_length=1, max_length=50)
    career: Optional[str] = Field(None, min_length=1, max_length=50)


# endregion

# region Admin requests schemas
class UpdateAdminRequest(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=50)
    last_name: Optional[str] = Field(None, min_length=1, max_length=50)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=1)
    faculty: Optional[str] = Field(None, min_length=1, max_length=50)

# endregion