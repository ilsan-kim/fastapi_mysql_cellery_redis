"""
For Admin API : 검수
"""
from datetime import datetime, timedelta
from typing import Any, Optional, List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.utils.api.admin import manager_name_extract, warning_level_changer
from app import crud
from app.schemas.admin import monitoring
from app.schemas.page_response import PageResponse
from app.schemas.series import SeriesUpdate, SeriesMetaUpdate, SeriesStatusUpdate
from app.models.series import Series, SeriesMeta, SeriesStatus
from app.controllers import deps

router = APIRouter()


@router.get("/", response_model=PageResponse)
def get_novel_table(
        *,
        db: Session = Depends(deps.get_db),
        page_request: dict = Depends(deps.get_page_request),
        q: Optional[str] = None, min_score: Optional[int] = 0, max_score: Optional[int] = 100, created_from: Optional[datetime] = None, created_to: Optional[datetime] = None,
        updated_from: Optional[datetime] = None, updated_to: Optional[datetime] = None, ficpick_free: Optional[bool] = True, ficpick_paid: Optional[bool] = True,
        free_pub_free: Optional[bool] = True, free_pub_paid: Optional[bool] = True, exclusive: Optional[bool] = True, non_exclusive: Optional[bool] = True,
        advertised: Optional[bool] = True, non_advertised: Optional[bool] = True, impressing: Optional[bool] = True,
        language_code: Optional[str] = None, genre_code: Optional[str] = None, status: str = None
) -> Any:
    raw_query = jsonable_encoder(crud.novel.get_list_paginated_for_admin(db=db, page_request=page_request,
                                                                         q=q, min_score=min_score, max_score=max_score, created_from=created_from, created_to=created_to,
                                                                         updated_from=updated_from, updated_to=updated_to, ficpick_free=ficpick_free, ficpick_paid=ficpick_paid,
                                                                         free_pub_free=free_pub_free, free_pub_paid=free_pub_paid, exclusive=exclusive, non_exclusive=non_exclusive,
                                                                         advertised=advertised, non_advertised=non_advertised, impressing=impressing,
                                                                         language_code=language_code, genre_code=genre_code))
    page_meta = raw_query.get("page_meta")
    raw_data = raw_query.get("content")

    detail_data_list = [{
        "id": data.get("id"),
        "is_impressing": data.get("is_impressing"),
        "title": list(filter(lambda x: x.get("is_origin") is True,
                             [novel_meta for novel_meta in
                              data.get("novel_meta")]))[0].get("title"),
        "writer_nickname": data.get("writer_nickname"),
        "series_length": len(data.get("series")),
        "view_count": 0,            # 추후 수정
        "rating": 0,                # 추후 수정
        "status": data.get("status"),
        "is_ficpick": data.get("is_ficpick"),
        "buy_count": 0,
        "is_exclusive": data.get("is_exclusive"),
        "is_advertised": data.get("is_advertised"),
        "created_at": data.get("created_at"),
        # "updated_at": data.get("series")[0].get("created_at"),      # 해당 작품의 최근 회차 업로드일
        "translation_suggestion": False,
        "score": data.get("score")
    } for data in raw_data]

    return {"page_meta": page_meta, "contents": detail_data_list}

    # raw_data = jsonable_encoder(crud.series_status.get_list_paginated(db=db, page_request=page_request))
    # detail_data = raw_data.get("content")
    # page_meta = raw_data.get("page_meta")
    # detail_data_list = [{
    #     "id": data.get("id"),
    #     "series_id": data.get("series").get("id"),
    #     "status": data.get("status"),
    #     "title": list(filter(lambda x: x.get("is_origin") is True,
    #                          [novel_meta for novel_meta in
    #                           data.get("series").get("novel").get("novel_meta")]))[0].get("title"),
    #     "episode": f"{data.get('series').get('order_number')}: "
    #                f"{list(filter(lambda x: x.get('is_origin') is True, [series_meta for series_meta in data.get('series').get('series_meta')]))[0].get('title')}",
    #     "writer_nickname": data.get("series").get("novel").get("writer_nickname"),
    #     "region_code": data.get("series").get("novel").get("region_code"),
    #     "created_at": data.get("created_at"),
    #     "processed_at": data.get("updated_at"),
    #     "manager": manager_name_extract(data.get("manager"))
    # } for data in detail_data]
    # return {"page_meta": page_meta, "contents":detail_data_list}
