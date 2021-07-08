from typing import Optional, List, Any, Dict

from pydantic import BaseModel, conlist, validator


# Shared properties
class BannedStringBase(BaseModel):
    locate: str = "NOVEL"
    language_code: str = "all"
    content: str


# Properties to Create via API
class BannedStringCreate(BannedStringBase):
    pass


# Properties to Update via API
class BannedStringUpdate(BannedStringBase):
    pass


# Properties of API Response
class BannedString(BannedStringBase):

    class Config:
        orm_mode = True
