from typing import Optional, List, Any, Dict, Tuple

from pydantic import BaseModel, conlist

from app.models.novel import STATUS


'''
basic novel tags schema class
'''


# Shared properties
class NovelTagBase(BaseModel):
    tag_list: Optional[List[str]]


# Properties to Create via API
class NovelTagCreate(NovelTagBase):
    pass


# Properties to Update via API
class NovelTagUpdate(NovelTagBase):
    novel_id: int


# Properties of API Response
class NovelTag(NovelTagBase):
    novel_id: int
    tag_code: str

    class Config:
        orm_mode = True


'''
basic novel metadata schema class
'''


# Shared properties
class NovelMetaBase(BaseModel):
    title: str = ""
    description: str = ""
    language_code: str = 'kr'


# Properties to Create via API
class NovelMetaCreate(NovelMetaBase):
    pass


# Properties to Update via API
class NovelMetaUpdate(NovelMetaBase):
    pass


# Properties of API Response
class NovelMeta(NovelMetaBase):
    id: int
    is_origin: bool

    class Config:
        orm_mode = True


'''
basic novel open day schema class
'''


# Shared properties
class NovelDayBase(BaseModel):
    pass


# Properties to Create via API
class NovelDayCreate(NovelDayBase):
    open_day_list: Optional[List[int]]


# Properties to Update via API
class NovelDayUpdate(NovelDayBase):
    novel_id: int


# Properties of API Response
class NovelDay(NovelDayBase):
    novel_id: int
    open_day: int

    class Config:
        orm_mode = True


'''
basic novel schema class
'''


# Shared properties
class NovelBase(BaseModel):
    writer_id: int
    writer_nickname: str
    thumbnail_url: str = ""
    genre_code: str = "FANTASY"
    region_code: str = "KR"
    language_code: str = "kr"
    is_scheduled: Optional[bool] = False
    is_exclusive: Optional[bool] = False
    is_censored: Optional[bool] = False
    is_free: Optional[bool] = True
    is_event: Optional[bool] = False


# Properties to Create via API
class NovelCreate(NovelBase):
    pass


# Properties to Update via API
class NovelUpdate(NovelBase):
    score: Optional[int] = None
    is_ficpick: Optional[bool] = False
    is_advertised: Optional[bool] = False
    is_deleted: Optional[bool] = False
    referral_url: Optional[str] = None
    status: Optional[str] = "ON_PROGRESS"


# Properties of API Response
class Novel(NovelBase):
    id: int
    is_fickpick: Optional[bool]
    is_advertised: Optional[bool]
    is_deleted: Optional[bool]
    referral_url: Optional[str]
    score: Optional[int]
    status: Optional[str]
    novel_tag: Optional[List[NovelTag]]
    novel_notice: Optional[List]
    series: Optional[List]
    novel_meta: Optional[List[NovelMeta]]
    novel_day: Optional[List[NovelDay]]

    class Config:
        orm_mode = True
