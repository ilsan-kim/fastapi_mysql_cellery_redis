from typing import Optional, List, Dict

from pydantic import BaseModel


'''
basic series schema class
'''


# Shared properties
class SeriesBase(BaseModel):
    is_completed: Optional[bool] = False


# Properties to Create via API
class SeriesCreate(SeriesBase):
    title: str
    paragraph: dict
    description: Optional[str] = ""


# Properties to Update via API
class SeriesUpdate(SeriesBase):
    id: int
    series_id: int
    title: str
    paragraph: dict
    description: str = ""


# Properties of API Response
class Series(SeriesBase):
    novel_id: int
    id: int
    paragraph: dict
    description: Optional[str] = ""

    class Config:
        orm_mode = True


'''
basic series metadata schema class
'''


# Shared properties
class SeriesMetaBase(BaseModel):
    title: str
    description: str = ""
    language_code: str = "kr"


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
