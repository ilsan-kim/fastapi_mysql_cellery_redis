from typing import Any, Dict, Optional, Union, List

from sqlalchemy import or_
from sqlalchemy.orm import Session, joinedload, contains_eager
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app.models.novel import Novel, NovelMeta, NovelDay
from app.models.novel_tag import NovelTag
from app.schemas.novel import (NovelCreate, NovelUpdate,
                               NovelDayUpdate,
                               NovelMetaUpdate,
                               NovelTagUpdate)


class CRUDNovel(CRUDBase[Novel, NovelCreate, NovelUpdate]):
    pass


class CRUDNovelMeta(CRUDBase[NovelMeta, BaseModel, NovelMetaUpdate]):
    pass


class CRUDNovelDay(CRUDBase[NovelDay, BaseModel, NovelDayUpdate]):
    pass


class CRUDNovelTag(CRUDBase[NovelTag, BaseModel, NovelTagUpdate]):
    pass


novel = CRUDNovel(Novel)
novel_meta = CRUDNovelMeta(NovelMeta)
novel_day = CRUDNovelDay(NovelDay)
novel_tag = CRUDNovelTag(NovelTag)
