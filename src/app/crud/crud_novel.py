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

    def get_list_paginated_for_admin(self, db: Session, *, page_request: dict, q: Optional[str] = None, min_score: Optional[int] = 0, max_score: Optional[int] = 100,
                                     created_from: Optional[datetime] = None, created_to: Optional[datetime] = None, updated_from: Optional[datetime] = None, updated_to: Optional[datetime] = None,
                                     ficpick_free: Optional[bool] = True, ficpick_paid: Optional[bool] = True, free_pub_free: Optional[bool] = True, free_pub_paid: Optional[bool] = True,
                                     exclusive: Optional[bool] = True, non_exclusive: Optional[bool] = True, advertised: Optional[bool] = True, non_advertised: Optional[bool] = True,
                                     impressing: Optional[bool] = True, language_code: Optional[str] = None, genre_code: Optional[str] = None, status: str = None):
        """
        통계데이터/번역 여부 데이터 가져오는 쿼리 보강해야함
        """

        # query param 으로 코드가 왔으면 그 코드 검증, 안왔으면 전체 (id 값을 갖는 모든 객체) 리턴
        if q:
            query_filter = NovelMeta.title.contains(q)
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
        '''
        oooo 전체 
        oxxx 픽픽 / 무료만 
        ooxx 픽픽
        xoxx 픽픽 / 유료만
        xxox 자유 / 무료만
        xxxo 자유 / 유료만
        xxoo 자유
        oxox 무료만
        oxxo 픽픽 / 무료만 <> 자유 / 유료만
        xoox 픽픽 / 유료만 <> 자유 / 무료만
        xoxo 유료만
        xooo 픽픽 / 유료만 <> 자유 전체
        oxoo 픽픽 / 무료만 <> 자유 전체 
        ooox 픽픽 전체 <> 자유 무료만
        ooxo 픽픽 전체 <> 자유 유료만
        '''
        if ficpick_free is True and ficpick_paid is True and free_pub_free is True and free_pub_paid is True:
            locate_filter = self.model.id
        elif ficpick_free is True and ficpick_paid is False and free_pub_free is False and free_pub_paid is False:
            locate_filter = and_(self.model.is_ficpick == True, self.model.is_free == True)
        elif ficpick_free is True and ficpick_paid is True and free_pub_free is False and free_pub_paid is False:
            locate_filter = self.model.is_ficpick == True
        elif ficpick_free is False and ficpick_paid is True and free_pub_free is False and free_pub_paid is False:
            locate_filter = and_(self.model.is_ficpick == True, self.model.is_free == False)
        elif ficpick_free is False and ficpick_paid is False and free_pub_free is True and free_pub_paid is False:
            locate_filter = and_(self.model.is_ficpick == False, self.model.is_free == True)
        elif ficpick_free is False and ficpick_paid is False and free_pub_free is False and free_pub_paid is True:
            locate_filter = and_(self.model.is_ficpick == False, self.model.is_free == False)
        elif ficpick_free is False and ficpick_paid is False and free_pub_free is True and free_pub_paid is True:
            locate_filter = self.model.is_ficpick == False
        elif ficpick_free is False and ficpick_paid is True and free_pub_free is True and free_pub_paid is False:
            locate_filter = self.model.is_free == True
        elif ficpick_free is True and ficpick_paid is False and free_pub_free is False and free_pub_paid is True:
            locate_filter = or_(and_(self.model.is_ficpick == True, self.model.is_free == True), and_(self.model.is_ficpick == False, self.model.is_free == False))
        elif ficpick_free is False and ficpick_paid is True and free_pub_free is True and free_pub_paid is False:
            locate_filter = or_(and_(self.model.is_ficpick == True, self.model.is_free == False), and_(self.model.is_ficpick == False, self.model.is_free == True))
        elif ficpick_free is False and ficpick_paid is True and free_pub_free is False and free_pub_paid is True:
            locate_filter = self.model.is_free == False
        elif ficpick_free is False and ficpick_paid is True and free_pub_free is True and free_pub_paid is True:
            locate_filter = or_(and_(self.model.is_ficpick == True, self.model.is_free == False), self.model.is_ficpick == False)
        elif ficpick_free is True and ficpick_paid is False and free_pub_free is True and free_pub_paid is True:
            locate_filter = or_(and_(self.model.is_ficpick == True, self.model.is_free == True), self.model.is_ficpick == False)
        elif ficpick_free is True and ficpick_paid is True and free_pub_free is True and free_pub_paid is False:
            locate_filter = or_(self.model.is_ficpick == True, and_(self.model.is_ficpick == False, self.model.is_free == True))
        else:
            locate_filter = or_(self.model.is_ficpick == True, and_(self.model.is_ficpick == False, self.model.is_free == False))

        if exclusive is True and non_exclusive is True:
            exclusive_filter = self.model.id
        elif exclusive is True and non_exclusive is False:
            exclusive_filter = self.model.is_exclusive is True
        else:
            exclusive_filter = self.model.is_exclusive is False

        if advertised is True and non_advertised is True:
            advertised_filter = self.model.id
        elif advertised is True and non_advertised is False:
            advertised_filter = self.model.is_advertised is True
        else:
            advertised_filter = self.model.is_advertised is False

        if impressing:
            impressing_filter = self.model.id
        else:
            impressing_filter = self.model.is_impressing is False

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
            filter(locate_filter).filter(exclusive_filter).filter(advertised_filter).filter(impressing_filter).\
            filter(language_filter).filter(genre_filter).filter(status_filter).\
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
