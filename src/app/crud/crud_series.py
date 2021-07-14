from datetime import datetime, timedelta
from typing import Any, Dict, Optional, Union, List

from sqlalchemy import or_
from sqlalchemy.orm import Session, joinedload, contains_eager
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

from app.crud.base import CRUDBase
from app.models.user import User
from app.models.writer import Writer
from app.models.novel import Novel, NovelMeta
from app.models.series import Series, SeriesMeta, SeriesStatus, STATUS
from app.models.paragraph import Paragraph
from app.schemas.series import SeriesCreate, SeriesUpdate, SeriesMetaCreate, SeriesMetaUpdate, SeriesStatusCreate, SeriesStatusUpdate
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

    def get_list_paginated(self, db: Session, *,
                           q: Optional[str] = None, page_request: dict, region_code: Optional[str] = None,
                           create_from: Optional[datetime] = None, create_to: Optional[datetime] = None, status: str = None):

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

        if create_from and create_to:
            time_filter = Series.created_at.between(create_from, create_to)
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
            filter(status_filter)

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


series = CRUDSeries(Series)
series_meta = CRUDSeriesMeta(SeriesMeta)
series_status = CRUDSeriesStatus(SeriesStatus)