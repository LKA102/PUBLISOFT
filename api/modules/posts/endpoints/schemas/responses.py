from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID


class PostResponse(BaseModel):
    id: UUID
    title: str
    file_url: str
    original_filename: str
    category: str
    type: str
    score_avg: float
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


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
