from datetime import datetime
from typing import Optional, List, Dict

from pydantic import BaseModel

from app.schemas.page_response import PageResponse

'''
basic series status statistic schema class for API response
'''


# 어드민 > 모니터링 현황 > 월별 누적 데이터
class MonthlyData(BaseModel):
    month: int
    registered: int
    processed: int
    unprocessed: int


# 어드민 > 모니터링 현황 > 월별 누적 데이터 조합 // FOR API RESPONSE
class MonthlyStatistic(BaseModel):
    total: int
    detail: List[MonthlyData]

    class Config:
        orm_mode = True


# 어드민 > 모니터링 테이블에 들어갈 행
class MonitoringTableRow(BaseModel):
    id: int
    series_id: int
    status: str
    title: str
    series: str
    writer_nickname: str
    region_code: str
    created_at: datetime
    processed_at: datetime
    manager: Optional[str]


# 어드민 > 모니터링 테이블 // FOR API RESPONSE
class MonitoringTablePage(PageResponse):
    contents: Optional[List[MonitoringTableRow]]

    class Config:
        orm_mode = True


class SeriesDataBase(BaseModel):
    id: int
    status: str
    title: str
    series: str
    writer_nickname: str
    region_code: str
    created_at: datetime

    class Config:
        orm_mode = True


# 어드민 > 모니터링 > 회차 상세정보 // FOR API RESPONSE
class SeriesDetail(SeriesDataBase):
    is_censored: bool
    contents: Optional[List[str]]


class SeriesStatusEdit(BaseModel):
    is_impressing: bool = True
    is_warning: bool = False
    is_delete: bool = False
    reason: str = "NORMAL"


class SeriesStatusList(SeriesDataBase):
    processed_at: datetime
    manager: Optional[str]