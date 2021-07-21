from typing import Any, Optional, List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import crud
from app.schemas.series import SeriesRead
from app.controllers import deps
from app.utils.api.series import get_meta_from_meta_list

router = APIRouter()


@router.get("/{series_id}")
def get_series_contents(
        *,
        series_id: int,
        language_code: str = "kr",
        db: Session = Depends(deps.get_db)) -> Any:
    """
    Create new series.
    """
    series_raw = crud.series.get_detail(db=db, id=series_id)
    meta_list = series_raw.series_meta
    statistic = series_raw.series_statistic
    paragraph_list = series_raw.paragraph
    contents = SeriesRead(
        id=series_raw.id,
        title=get_meta_from_meta_list(meta_list=meta_list, comparison="language_code", criteria=language_code, value="title"),
        description=get_meta_from_meta_list(meta_list=meta_list, comparison="language_code", criteria=language_code, value="description"),
        order_number=series_raw.order_number,
        created_at=series_raw.created_at,
        rating=statistic.rating,
        view_count=statistic.view_count,
        paragraph_list=[{"id": paragraph.id, "text": paragraph.text} for paragraph in paragraph_list]
    )
    return contents
