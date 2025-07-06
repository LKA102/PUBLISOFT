from pydantic import BaseModel
from fastapi import Form


class PostCreate(BaseModel):
    title: str
    category: str
    post_type: str


class PostCreateForm:
    def __init__(
        self,
        title: str = Form(...),
        category: str = Form(...),
        post_type: str = Form(...),
    ):
        self.title = title
        self.category = category
        self.post_type = post_type


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
