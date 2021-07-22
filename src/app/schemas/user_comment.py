from typing import Optional, List, Any, Dict

from pydantic import BaseModel, conlist, validator


# Shared properties
class UserCommentBase(BaseModel):
    user_id: int
    comment_id: int


# Properties to Create via API
class UserCommentCreate(UserCommentBase):
    pass


# Properties to Update via API
class UserCommentUpdate(UserCommentBase):
    pass


# Properties of API Response
class UserComment(UserCommentBase):

    class Config:
        orm_mode = True
