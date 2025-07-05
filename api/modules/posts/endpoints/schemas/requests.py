from pydantic import BaseModel


class PostCreate(BaseModel):
    title: str
    file_url: str
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
