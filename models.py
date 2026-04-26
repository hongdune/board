from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class PostCreate(BaseModel):
    title: str
    content: str
    author_id: str
    author_password: str


class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    author_id: str
    image_url: Optional[str] = None
    created_at: datetime

    model_config = {"from_attributes": True}


class CommentCreate(BaseModel):
    content: str
    author_id: str
    author_password: str


class CommentResponse(BaseModel):
    id: int
    post_id: int
    content: str
    author_id: str
    created_at: datetime

    model_config = {"from_attributes": True}
