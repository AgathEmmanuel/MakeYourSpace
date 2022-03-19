from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class PostMain(BaseModel):
    title: str
    description: Optional[str]=None
    content: Optional[str]=None


class PostCreate(PostMain):
    user_id: int
    post_id: int
    class Config:
        orm_mode = True

class PostCreateResponse(BaseModel):
    user_id: int
    post_status: bool
    post_id: int
    creation_time: datetime
    class Config:
        orm_mode = True


class PostGetResponse(PostMain):
    post_id: int
    class Config:
        orm_mode = True

class PostUpdate(PostMain):
    user_id: int
    post_id: int
    class Config:
        orm_mode = True


class PostUpdateResponse(PostMain):
    post_id: int
    class Config:
        orm_mode = True

