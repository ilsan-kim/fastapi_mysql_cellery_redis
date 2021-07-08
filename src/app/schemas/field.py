from typing import Optional, List, Any, Dict

from pydantic import BaseModel, conlist, validator


# Shared properties with Fields and CodeFields
class FieldBase(BaseModel):
    code: str


# Properties to Create via API
class FieldCreate(FieldBase):
    pass


# Properties to Update via API
class FieldUpdate(FieldBase):
    pass


# Properties of API Response
class Field(FieldBase):
    id: int
    is_activate: Optional[bool] = True

    class Config:
        orm_mode = True


# Properties to Create with code via API
class CodeFieldCreate(FieldBase):
    is_activate: Optional[bool] = True

    @validator('code')
    def is_iso(cls, v):
        if len(v) != 3 and len(v) != 2:
            raise ValueError('language_code: ISO 639-1 & region_code: ISO 3166-1 alpha-2 & If you need to define "all", use "ALL"')
        return v


# Properties to Update via API
class CodeFieldUpdate(CodeFieldCreate):
    pass


# Properties of API Response
class CodeField(CodeFieldCreate):
    pass

    class Config:
        orm_mode = True


# Shared properties
class FieldDetailBase(BaseModel):
    code: str
    language_code: str = "kr"
    name: str


# Properties to Create via API
class FieldDetailCreate(FieldDetailBase):
    pass


# Properties to Update via API
class FieldDetailUpdate(FieldDetailBase):
    pass


# Properties of API Response
class FieldDetail(FieldDetailBase):

    class Config:
        orm_mode = True
