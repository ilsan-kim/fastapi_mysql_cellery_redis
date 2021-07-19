from datetime import datetime
from typing import Optional, List, Dict

from pydantic import BaseModel

from app.schemas.page_response import PageResponse

'''
basic novel management schema class for API response
'''


# 어드민 > 작품관리 > 작품 테이블의 행
class NovelTableRow(BaseModel):
    id: int
    is_impressing: bool
    title: str
    writer_nickname: str
    series_length: int
    view_count: int = 0
    rating: float = 0
    status: str
    buy_count: int = 0
    is_exclusive: bool
    is_advertised: bool
    created_at: datetime
    updated_at: Optional[datetime]        # 최종 업로드일
    translation_suggestion: bool
    score: int


# 어드민 > 작품관리 > 작품 테이블 // FOR API RESPONSE
class NovelTable(PageResponse):
    contents: Optional[List[NovelTableRow]]

    class Config:
        orm_mode = True


# 어드민 > 작품관리 > 작품 스코어 및 노출 현황 수정
class NovelStatusEdit(BaseModel):
    is_impressing: Optional[bool] = None
    score: Optional[int] = None


# 어드민 > 작품관리 > 작품 상세정보의 작품 메타 데이터
class NovelMetaData(BaseModel):
    title: str
    nickname: str
    writer_nickname: str
    created_at: datetime
    status: str
    is_exclusive: bool
    is_advertised: bool
    updated_at: Optional[datetime]
    buy_count: int
    coupon_count: int
    sponsor_count: int
    is_ficpick: bool
    series_length: int
    like_count: int
    rating: float
    novel_day: Optional[List[int]]
    language_code: str
    region_code: str
    genre_code: str


# 어드민 > 작품관리 > 작품 상세정보 시리즈 데이터 리스트
class SeriesDataInNovelMeta(BaseModel):
    id: int
    order_number: int
    is_impressing: bool
    title: str
    created_at: datetime
    updated_at: datetime
    rating: int
    comment: int
    view_count: int
    buy_count: int
