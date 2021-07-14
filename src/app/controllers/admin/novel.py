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
        page_request: dict = Depends(deps.get_page_request)
) -> Any:
    raw_query = jsonable_encoder(crud.novel.get_list_paginated(db=db, page_request=page_request))
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
