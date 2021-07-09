from typing import Any, Dict, Optional, Union, List

from sqlalchemy import or_
from sqlalchemy.orm import Session, joinedload, contains_eager
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

from app.crud.base import CRUDBase
from app.models.series import Series, SeriesMeta
from app.schemas.series import SeriesCreate, SeriesUpdate, SeriesMetaCreate, SeriesMetaUpdate


class CRUDSeries(CRUDBase[Series, SeriesCreate, SeriesUpdate]):
    def get_order_number(self, db: Session, novel_id: int):
        series_list = db.query(self.model).filter(self.model.novel_id == novel_id).order_by(self.model.order_number.desc()).first()
        if series_list:
            return series_list.order_number + 1
        return 1


class CRUDSeriesMeta(CRUDBase[SeriesMeta, SeriesMetaCreate, SeriesMetaUpdate]):
    pass


series = CRUDSeries(Series)
series_meta = CRUDSeriesMeta(SeriesMeta)
