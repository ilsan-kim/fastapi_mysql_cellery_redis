from datetime import datetime
from typing import Optional, List, Dict

from pydantic import BaseModel


'''
basic novel management schema class for API response
'''


# Shared properties
class NovelManagement(BaseModel):
    id: int
    is_impressing: bool
    title: str
    writer_nickname: str
    language_code: str
    series_length: int
    view_count: int = 0
    rating: float = 0
    status: str
    is_ficpick: bool
    buy_count: int = 0
    is_exclusive: bool
    is_advertised: bool
    created_at: datetime
    updated_at: datetime        # 최종 업로드일
    translation_suggestion: bool
    score: int
