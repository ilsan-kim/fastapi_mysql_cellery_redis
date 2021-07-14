from datetime import datetime
from typing import Optional, List, Dict

from pydantic import BaseModel


'''
basic series status statistic schema class for API response
'''


# Shared properties
class MonthlyData(BaseModel):
    month: int
    registered: int
    processed: int
    unprocessed: int


# Properties of API Response
class SeriesStatusStatistic(BaseModel):
    total: int
    detail: List[MonthlyData]

    class Config:
        orm_mode = True


class SeriesDataBase(BaseModel):
    id: int
    status: str
    title: str
    episode: str
    writer_nickname: str
    region_code: str
    created_at: datetime

    class Config:
        orm_mode = True


class SeriesStatusList(SeriesDataBase):
    processed_at: datetime
    manager: Optional[str]


class SeriesDetail(SeriesDataBase):
    is_censored: bool
    contents: List[str]


class SeriesStatusEdit(BaseModel):
    is_impressing: bool = True
    is_warning: bool = False
    is_delete: bool = False
    reason: str = "NORMAL"
