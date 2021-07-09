from typing import Any, Optional, List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import crud
from app.schemas import series, novel
from app.controllers import deps
from app.controllers.v1.novel import router

novel_router = router


@router.post("/{novel_id}/", response_model=series.Series)
def create_series(
        *,
        novel_id: int,
        db: Session = Depends(deps.get_db),
        series_in: series.SeriesCreate
) -> Any:

    """
    Create new series.
    """
    # series params
    novel_data = crud.novel.get_with_series(db=db, id=novel_id)
    writer_id = novel_data.writer_id
    novel_is_free = novel_data.is_free
    paid_from = novel_data.need_pay_from
    order_number = crud.series.get_order_number(db=db, novel_id=novel_id)

    if novel_is_free is True:
        is_free = True
    elif paid_from > order_number:
        is_free = True
    else:
        is_free = False

    series_params = {
        'novel_id': novel_id,
        'writer_id': writer_id,
        'order_number': order_number,
        'is_completed': series_in.is_completed,
        'status': 'UNAPPROVED',
        'is_free': is_free
    }

    # paragraph 입력 구현
    # series_meta 입력 구현

    series = crud.series.create(db, obj_in=series_params)

    return series
