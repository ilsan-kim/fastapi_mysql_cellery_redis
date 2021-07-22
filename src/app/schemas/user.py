from typing import Optional, List, Any, Dict

from pydantic import BaseModel, conlist


# Shared properties
class UserBase(BaseModel):
    email: str = "aa@aa.com"
    nickname: str = "somenickname"
    phone_number: Optional[str] = '010-1111-1111'
    gender: Optional[str] = 'ETC'
    language_code: Optional[str] = 'kr'
    profile_url: Optional[str] = None


# Properties to Create via API
class UserCreate(UserBase):
    password: str


# Properties to Update via API
class UserUpdate(UserBase):
    password: Optional[str] = None


# Properties of API Response
class User(UserBase):
    id: int
    is_super: Optional[bool] = False
    is_authenticated: Optional[bool] = False
    accept_notification: Optional[bool] = False
    accept_mailing: Optional[bool] = False
    status: Optional[str] = 'NORMAL'
    name: Optional[str] = ""

    class Config:
        orm_mode = True
