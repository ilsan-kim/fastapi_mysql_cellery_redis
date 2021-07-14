from pydantic import BaseModel

from sqlalchemy.orm import Session, joinedload

from app.crud.base import CRUDBase
from app.models.paragraph import Paragraph
from app.models.novel import Novel, NovelMeta, NovelDay
from app.models.series import Series, SeriesMeta
from app.models.novel_tag import NovelTag
from app.schemas.novel import (NovelCreate, NovelUpdate,
                               NovelDayUpdate,
                               NovelMetaCreate, NovelMetaUpdate,
                               NovelTagUpdate)
from app.schemas.page_response import paginated_query


class CRUDNovel(CRUDBase[Novel, NovelCreate, NovelUpdate]):
    def get_with_series(self, db: Session, id: int):
        return db.query(self.model).\
            outerjoin(self.model.series).\
            options(joinedload(self.model.series)).\
            filter(self.model.id == id).first()

    def get_list_paginated(self, page_request: dict, db: Session):
        """
        통계데이터/번역 여부 데이터 가져오는 쿼리 보강해야함
        """
        page = page_request.get("page", 1)
        size = page_request.get("size", 20)

        # base_query > 기본 쿼리 (total length 측정용)
        # paginated > 페이징 적용
        # query > 완성된 쿼리
        base_query = db.query(self.model)
        paginated = base_query.order_by(Novel.id.desc()).limit(size).offset((page - 1) * size).from_self()
        query = paginated.\
            outerjoin(NovelMeta).\
            options(joinedload(self.model.novel_meta)).\
            outerjoin(Series).outerjoin(Paragraph).outerjoin(SeriesMeta).\
            options(joinedload(self.model.series).joinedload(Series.series_meta)).\
            options(joinedload(self.model.series).joinedload(Series.paragraph))

        return paginated_query(
            page_request=page_request,
            base_query=base_query,
            completed_query=query,
            query_executor=lambda x: x.all()
        )


class CRUDNovelMeta(CRUDBase[NovelMeta, NovelMetaCreate, NovelMetaUpdate]):
    pass


class CRUDNovelDay(CRUDBase[NovelDay, BaseModel, NovelDayUpdate]):
    pass


class CRUDNovelTag(CRUDBase[NovelTag, BaseModel, NovelTagUpdate]):
    pass


novel = CRUDNovel(Novel)
novel_meta = CRUDNovelMeta(NovelMeta)
novel_day = CRUDNovelDay(NovelDay)
novel_tag = CRUDNovelTag(NovelTag)
