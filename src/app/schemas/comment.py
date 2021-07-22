from typing import Optional, List
from datetime import datetime

from pydantic import BaseModel


'''
basic novel tags schema class
'''


# Shared properties
class CommentBase(BaseModel):
    content: str
    image_url: Optional[str] = None


# Properties to Create via API
class CommentCreate(CommentBase):
    user_id: int
    series_id: Optional[int] = None


# Properties to Update via API
class CommentUpdate(CommentBase):
    user_id: int
    like_count: int


# Properties for API response
class Comment(CommentBase):
    user_id: int
    series_id: int
    like_count: int
    created_at: datetime

    class Config:
        orm_mode = True


# 리더기 > 개별 댓글 정보
class CommentDetail(CommentBase):
    id: int
    nickname: str
    profile_url: str
    like_count: int
    created_at: datetime

    class Config:
        orm_mode = True
