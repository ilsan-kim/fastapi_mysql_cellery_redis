from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, and_

from app.crud.base import CRUDBase
from app.models.paragraph import Paragraph
from app.models.novel import Novel, NovelMeta, NovelDay
from app.models.series import Series, SeriesMeta
from app.models.novel_tag import NovelTag
from app.models.writer import Writer
from app.schemas.novel import (NovelCreate, NovelUpdate,
                               NovelDayUpdate,
                               NovelMetaCreate, NovelMetaUpdate,
                               NovelTagUpdate)
from app.schemas.page_response import paginated_query


class CRUDNovel(CRUDBase[Novel, NovelCreate, NovelUpdate]):
    def get_with_join(self, db: Session, id: int) -> Novel:
        # cash_writer(후원) / cash_series(구매) / coupon_series(보너스쿠폰) / series_statistic(관심수/별점) > 나중에 추가
        return db.query(self.model).\
            outerjoin(self.model.series).outerjoin(Series.series_meta).\
            options(joinedload(self.model.series).joinedload(Series.series_meta)).\
            outerjoin(self.model.novel_meta).\
            options(joinedload(self.model.novel_meta)).\
            join(self.model.writer).join(Writer.user).\
            options(joinedload(self.model.writer).joinedload(Writer.user)).\
            outerjoin(self.model.novel_day).\
            options(joinedload(self.model.novel_day)).\
            filter(self.model.id == id).first()

    def get_list_paginated_for_admin(self, db: Session, *, page_request: dict, q: Optional[str] = None, min_score: Optional[int] = 0, max_score: Optional[int] = 100,
                                     created_from: Optional[str] = None, created_to: Optional[str] = None, updated_from: Optional[str] = None, updated_to: Optional[str] = None,
                                     is_ficpick: Optional[bool] = None, is_free: Optional[bool] = None, is_exclusive: Optional[bool] = None, is_advertised: Optional[bool] = None,
                                     is_impressing: bool = True, language_code: Optional[str] = None, genre_code: Optional[str] = None, status: str = None):

        """
        통계데이터/번역 여부 데이터 가져오는 쿼리 보강해야함
        """
        # query param 으로 코드가 왔으면 그 코드 검증, 안왔으면 전체 (id 값을 갖는 모든 객체) 리턴
        if q:
            query_filter = or_(NovelMeta.title.contains(q), self.model.writer_nickname.contains(q))
        else:
            query_filter = self.model.id

        if created_from and created_to:
            created_time_filter = Novel.created_at.between(created_from, created_to)
        else:
            created_time_filter = self.model.id

        if updated_from and updated_to:
            upload_time_filter = Series.created_at.between(created_from, created_to)
        else:
            upload_time_filter = self.model.id

        if is_ficpick is None:
            ficpick_filter = self.model.id
        elif is_ficpick is True:
            ficpick_filter = self.model.is_ficpick == True
        else:
            ficpick_filter = self.model.is_ficpick == False

        if is_free is None:
            price_filter = self.model.id
        elif is_free is True:
            price_filter = self.model.is_free == True
        else:
            price_filter = self.model.is_free == False

        if is_exclusive is None:
            exclusive_filter = self.model.id
        elif is_exclusive is True:
            exclusive_filter = self.model.is_exclusive == True
        else:
            exclusive_filter = self.model.is_exclusive == False

        if is_advertised is None:
            advertised_filter = self.model.id
        elif is_advertised is True:
            advertised_filter = self.model.is_advertised == True
        else:
            advertised_filter = self.model.is_advertised == False

        if is_impressing is True:
            impressing_filter = self.model.id
        else:
            impressing_filter = self.model.is_impressing == False

        if language_code:
            language_filter = self.model.language_code == language_code
        else:
            language_filter = self.model.id

        if genre_code:
            genre_filter = self.model.genre_code == genre_code
        else:
            genre_filter = self.model.id

        if status:
            status_list = status.split(",")
            status_filter = self.model.status.in_(status_list)
        else:
            status_filter = self.model.id

        query = db.query(self.model).\
            outerjoin(NovelMeta).\
            options(joinedload(self.model.novel_meta)).\
            outerjoin(Series).outerjoin(Paragraph).outerjoin(SeriesMeta).\
            options(joinedload(self.model.series).joinedload(Series.series_meta)).\
            options(joinedload(self.model.series).joinedload(Series.paragraph)).\
            filter(query_filter).filter(self.model.score.between(min_score, max_score)).\
            filter(created_time_filter).filter(upload_time_filter).\
            filter(ficpick_filter).filter(price_filter).filter(exclusive_filter).filter(advertised_filter).\
            filter(impressing_filter).filter(language_filter).filter(genre_filter).filter(status_filter).\
            group_by(self.model.id)

        page = page_request.get("page", 1)
        size = page_request.get("size", 20)

        return paginated_query(
            page_request,
            query,
            lambda x: x.order_by(Novel.id.desc()).limit(size).offset((page - 1) * size).all()
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
