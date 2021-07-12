from typing import Optional, List

from pydantic import BaseModel


'''
basic series schema class
'''


# Shared properties
class ParagraphBase(BaseModel):
    series_id: int
    order_number: int
    text: str
    language_code: str
    is_origin: bool = False
    is_selected: bool = False


# Properties to Create via API
class ParagraphCreate(ParagraphBase):
    pass


# Properties to Update via API
class ParagraphUpdate(ParagraphBase):
    pass


# Properties of API Response
class Paragraph(ParagraphBase):
    id: int

    class Config:
        orm_mode = True
