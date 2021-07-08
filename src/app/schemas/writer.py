from typing import Optional, List, Any, Dict

from pydantic import BaseModel, conlist


# Shared properties
class WriterBase(BaseModel):
    id: int
    nickname_1: Optional[str] = ""
    nickname_2: Optional[str] = ""
    nickname_3: Optional[str] = ""


# Properties to Create via API
class WriterCreate(WriterBase):
    pass


# Properties to Update via API
class WriterUpdate(WriterCreate):
    is_contracted: bool = False
    commission_rate: float = 0.6


# Properties of API Response
class Writer(WriterBase):
    is_contracted: bool
    commission_rate: float

    class Config:
        orm_mode = True
