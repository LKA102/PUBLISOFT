from pydantic import BaseModel
from fastapi import Form
from uuid import UUID


class PostCreate(BaseModel):
    title: str
    category: str
    post_type: str
    author_id: UUID


class PostCreateForm:
    def __init__(
        self,
        title: str = Form(...),
        category: str = Form(...),
        post_type: str = Form(...),
        author_id: UUID = Form(...),
    ):
        self.title = title
        self.category = category
        self.post_type = post_type
        self.author_id = author_id


class PostUpdate(BaseModel):
    post_id: str
    title: str
    file_url: str
    category: str
    type: str


class PostScore(BaseModel):
    post_id: str
    score: int
    student_id: str
