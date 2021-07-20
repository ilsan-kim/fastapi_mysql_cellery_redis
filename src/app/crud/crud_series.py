from datetime import datetime, timedelta
from typing import Any, Dict, Optional, Union, List

from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload, contains_eager
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

from app.crud.base import CRUDBase
from app.models.user import User
from app.models.writer import Writer
from app.models.novel import Novel, NovelMeta
from app.models.series import Series, SeriesMeta, SeriesStatus, SeriesStatistic, STATUS
from app.models.paragraph import Paragraph
from app.schemas.series import (SeriesCreate, SeriesUpdate,
                                SeriesMetaCreate, SeriesMetaUpdate,
                                SeriesStatusCreate, SeriesStatusUpdate,
                                SeriesStatisticCreate, SeriesStatisticUpdate)
from app.schemas.page_response import paginated_query


class CRUDSeries(CRUDBase[Series, SeriesCreate, SeriesUpdate]):
    def get_order_number(self, db: Session, novel_id: int):
        series_list = db.query(self.model).filter(self.model.novel_id == novel_id).order_by(self.model.order_number.desc()).first()
        if series_list:
            return series_list.order_number + 1
        return 1

    def get_detail(self, db: Session, id: int):
        series_data = db.query(self.model).\
            outerjoin(SeriesMeta).outerjoin(Paragraph).outerjoin(Novel).outerjoin(NovelMeta).\
            options(joinedload(self.model.series_meta)).\
            options(joinedload(self.model.paragraph)).\
            options(joinedload(self.model.novel).joinedload(Novel.novel_meta)).\
            filter(self.model.id == id).first()
        return series_data

    def delete_by_monitoring(self, db: Session, id: int):
        series_obj = db.query(self.model).get(id)
        db.delete(series_obj)
        db.commit()
        return series_obj


class CRUDSeriesMeta(CRUDBase[SeriesMeta, SeriesMetaCreate, SeriesMetaUpdate]):
    pass


class CRUDSeriesStatus(CRUDBase[SeriesStatus, SeriesStatusCreate, SeriesStatusUpdate]):
    def get_all(self, db: Session) -> List[SeriesStatus]:
        return db.query(self.model).all()

    def get_list_paginated_for_admin(self, db: Session, *,
                                     page_request: dict, q: Optional[str] = None, region_code: Optional[str] = None,
                                     created_from: Optional[str] = None,
                                     created_to: Optional[str] = None,
                                     status: str = None):
        """
        :param q: 검색어 (string)
        :param region_code:  권역 코드 (string)
        :param created_from:  등록일 시작점 (datetime)
        :param created_to:    등록일 종료점 (datetime)
        :param status:       작품 상태 (list of string) > 전체 = ["UNAPPROVED", "APPROVED"] / 미처리만 = ["UNAPPROVED"] / 처리만 = ["APPROVED"]
        """

        # query param 으로 코드가 왔으면 그 코드 검증, 안왔으면 전체 (id 값을 갖는 모든 객체) 리턴
        if q:
            query_filter = NovelMeta.title.contains(q) | \
                           SeriesMeta.title.contains(q) | \
                           Novel.writer_nickname.contains(q)
        else:
            query_filter = self.model.id

        if region_code:
            region_filter = Novel.region_code == region_code
        else:
            region_filter = self.model.id

        if created_from and created_to:
            time_filter = Series.created_at.between(created_from, created_to)
        else:
            time_filter = self.model.id

        if status:
            status_list = status.split(",")
            status_filter = self.model.status.in_(status_list)
        else:
            status_filter = self.model.id

        query = db.query(self.model).\
            outerjoin(Series).outerjoin(SeriesMeta).outerjoin(Novel).outerjoin(NovelMeta).\
            options(joinedload(self.model.series).joinedload(Series.series_meta)).\
            options(joinedload(self.model.series).joinedload(Series.novel).joinedload(Novel.novel_meta)).\
            outerjoin(User).\
            options(joinedload(self.model.manager)).\
            filter(query_filter).\
            filter(region_filter).\
            filter(time_filter).\
            filter(status_filter).\
            group_by(self.model.id)

        page = page_request.get("page", 1)
        size = page_request.get("size", 20)

        return paginated_query(
            page_request,
            query,
            lambda x: x.order_by(SeriesStatus.id.desc()).limit(size).offset((page - 1) * size).all()
        )

    def get_detail(self, db: Session, id: int) -> Optional[SeriesStatus]:
        return db.query(self.model).\
            outerjoin(Series).outerjoin(Writer).outerjoin(User).\
            options(joinedload(self.model.series).joinedload(Series.writer).joinedload(Writer.user)).filter(self.model.id == id).first()


class CRUDSeriesStatistic(CRUDBase[SeriesStatistic, SeriesStatisticCreate, SeriesStatisticUpdate]):
    pass


series = CRUDSeries(Series)
series_meta = CRUDSeriesMeta(SeriesMeta)
series_status = CRUDSeriesStatus(SeriesStatus)
series_statistic = CRUDSeriesStatistic(SeriesStatistic)