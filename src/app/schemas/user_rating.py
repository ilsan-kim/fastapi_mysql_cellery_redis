from typing import Optional, List, Any, Dict

from pydantic import BaseModel, conlist, validator


class UserRatingBase(BaseModel):
    rating: float

    @validator('rating')
    def under_five(cls, v):
        if v < 0 or v > 5:
            raise ValueError('Rating only allow 0 to 5 value')
        return v


# 레이팅 매기기 인풋값
class UserRatingCreate(UserRatingBase):
    pass


class UserRatingUpdate(UserRatingBase):
    pass


class UserRating(UserRatingBase):
    user_id: int
    series_id: int
