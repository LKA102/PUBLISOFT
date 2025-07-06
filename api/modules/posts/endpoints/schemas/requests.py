from pydantic import BaseModel
from fastapi import UploadFile


class PostCreate(BaseModel):
    title: str
    file: UploadFile
    category: str
    type: str


class PostUpdate(BaseModel):
    title: str
    file_url: str
    category: str
    type: str


class PostScore(BaseModel):
    post_id: str
    score: int
    student_id: str
