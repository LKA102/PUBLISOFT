from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID


class PostResponse(BaseModel):
    id: str
    title: str
    file_url: str
    original_filename: str
    category: str
    type: str
    score_avg: float
    author_id: str
    created_at: Optional[str]
    updated_at: Optional[str]


class CreatePostResponse(BaseModel):
    message: str
    post: PostResponse


class UpdatePostResponse(BaseModel):
    message: str
    post: PostResponse


class DeletePostResponse(BaseModel):
    message: str


class ScorePostResponse(BaseModel):
    message: str
