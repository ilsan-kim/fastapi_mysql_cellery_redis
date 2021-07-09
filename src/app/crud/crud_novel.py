from pydantic import BaseModel

from sqlalchemy.orm import Session, joinedload

from app.crud.base import CRUDBase
from app.models.novel import Novel, NovelMeta, NovelDay
from app.models.series import Series
from app.models.novel_tag import NovelTag
from app.schemas.novel import (NovelCreate, NovelUpdate,
                               NovelDayUpdate,
                               NovelMetaUpdate,
                               NovelTagUpdate)


class CRUDNovel(CRUDBase[Novel, NovelCreate, NovelUpdate]):
    def get_with_series(self, db: Session, id: int):
        return db.query(self.model).\
            outerjoin(self.model.series).\
            options(joinedload(self.model.series)).\
            filter(self.model.id == id).first()


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
