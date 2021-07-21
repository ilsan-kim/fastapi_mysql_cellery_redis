from typing import Optional, List

from pydantic import BaseModel


'''
basic series schema class
'''


# Shared properties
class ParagraphBase(BaseModel):
    text: str


# Properties to Create via API
class ParagraphCreate(ParagraphBase):
    language_code: str
    is_origin: bool = False
    is_selected: bool = False
    series_id: int
    order_number: int


# Properties to Update via API
class ParagraphUpdate(ParagraphBase):
    language_code: str
    is_origin: bool = False
    is_selected: bool = False
    series_id: int
    order_number: int


# Properties of API Response
class Paragraph(ParagraphBase):
    id: int
    language_code: str
    is_origin: bool = False
    is_selected: bool = False
    series_id: int
    order_number: int

    class Config:
        orm_mode = True


# 리더기의 문단별 텍스트 영역
class ParagraphInSeries(ParagraphBase):
    id: int
