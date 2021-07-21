from typing import Optional, List, Dict
from datetime import datetime

from pydantic import BaseModel

from app.schemas.page_response import PageResponse
from .paragraph import Paragraph, ParagraphInSeries

'''
basic series statistic schema class
'''


# Shared properties
class SeriesStatisticBase(BaseModel):
    series_id: int
    view_count: int = 0
    like_count: int = 0
    rating: float = 0
    payment_count: int = 0
    language_code: str = "kr"


class SeriesStatisticCreate(SeriesStatisticBase):
    pass


class SeriesStatisticUpdate(SeriesStatisticBase):
    pass


class SeriesStatistic(SeriesStatisticBase):
    class Config:
        orm_mode = True



'''
basic series metadata schema class
'''


# Shared properties
class SeriesMetaBase(BaseModel):
    title: str
    description: Optional[str] = ""
    language_code: str


# Properties to Create via API
class SeriesMetaCreate(SeriesMetaBase):
    pass


# Properties to Update via API
class SeriesMetaUpdate(SeriesMetaBase):
    id: int
    series_id: int


# Properties of API Response
class SeriesMeta(SeriesMetaBase):
    is_origin: bool

    class Config:
        orm_mode = True


'''
basic series status management schema class
'''


# Shared properties
class SeriesStatusBase(BaseModel):
    series_id: int
    manager_id: Optional[int]
    status: str = "UNAPPROVED"
    reason: str = "NORMAL"


# Properties to Create via API
class SeriesStatusCreate(SeriesStatusBase):
    pass


# Properties to Update via API
class SeriesStatusUpdate(SeriesStatusCreate):
    status: Optional[str]
    reason: Optional[str]


# Properties of API Response
class SeriesStatus(SeriesStatusBase):
    pass

    class Config:
        orm_mode = True


'''
basic series schema class
'''


# Shared properties
class SeriesBase(BaseModel):
    is_completed: Optional[bool] = False


# Properties to Create via API
class SeriesCreate(SeriesBase):
    title: str
    paragraph: list
    description: Optional[str] = ""


# Properties to Update via API
class SeriesUpdate(SeriesBase):
    title: Optional[str]
    paragraph: Optional[dict]
    description: Optional[str] = ""
    status: Optional[str]


# Properties of API Response
class Series(SeriesBase):
    novel_id: int
    id: int
    order_number: int
    status: str
    paragraph: List[Paragraph]
    series_meta: Optional[List[SeriesMeta]]
    series_statistic: Optional[List[SeriesStatistic]]

    class Config:
        orm_mode = True


# 리더기 > 작품 조회
class SeriesRead(BaseModel):
    id: int
    title: str
    description: str
    created_at: datetime
    paragraph_list: List[ParagraphInSeries]
    rating: float


# 특정 작품의 회차 리스트
class SeriesInNovelDetail(SeriesBase):
    id: int
    title: str
    order_number: int
    created_at: datetime
    rating: float
    view_count: int


# 회차 리스트 with 페이징
class SeriesInNovelDetailPage(PageResponse):
    contents: Optional[List[SeriesInNovelDetail]]

    class Config:
        orm_mode = True
