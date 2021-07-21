"""
For Admin API : 검수
"""
from typing import Any, Optional

from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import crud
from app.schemas.admin.novel import NovelTableRow, NovelTable, NovelMetaData, SeriesDataInNovelMeta, NovelStatusEdit
from app.schemas.page_response import PageResponse
from app.controllers import deps
from app.utils.api.admin import check_updated_date
from app.utils.api.novel import get_meta_from_meta_list

router = APIRouter()


@router.get("/", response_model=PageResponse)
def get_novel_table(
        *,
        db: Session = Depends(deps.get_db),
        page_request: dict = Depends(deps.get_page_request),
        q: Optional[str] = None, min_score: Optional[int] = 0, max_score: Optional[int] = 100,
        created_from: Optional[str] = None, created_to: Optional[str] = None,
        updated_from: Optional[str] = None, updated_to: Optional[str] = None,
        is_ficpick: Optional[bool] = None, is_free: Optional[bool] = None, is_exclusive: Optional[bool] = None,
        is_advertised: Optional[bool] = None, is_impressing: bool = True,
        language_code: Optional[str] = None, genre_code: Optional[str] = None, status: str = None
) -> Any:
    """
    어드민 > 작품관리 > 작품 리스트를 리턴합니다.
    :param q: 검색어 (string)\n
    :param min_score: 최소 스코어 (int)\n
    :param max_score: 최대 스코어 (int)\n
    :param created_from: 등록일 시작점 (datetime)\n
    :param created_to: 등록일 종료점 (datetime)\n
    :param updated_from: 마지막 업로드 시작점 (datetime)\n
    :param updated_to: 마지막 업로드 종료점 (datetime)\n
    :param is_ficpick: 연재관 (None: 전체 / True: Fickpick / False: 자유연재)\n
    :param is_free: 유무료 (None: 전체 / True: 무료 / False: 유료)\n
    :param is_exclusive: 독점작 여부 (None: 전체 / True: 독점작 / False: 비독점작)\n
    :param is_advertised: 광고동의 여부 (None 전체 / True: Y / False: N)\n
    :param is_impressing: 노출 상태 셀렉 (True: 전체 / False: 비노출)__!!기획서상 얘만 T/F 입니다. 기본값은 True!!__\n
    :param language_code: 언어코드 (string)\n
    :param genre_code: 장르코드 (string)\n
    :param status: 상태 > 각각  COMPLETED, ON_PROGRESS, PAUSED 로 체크 상황에 따라 콤마 붙여서 string으로 주면 됨 (ex. 완결/연재중 체크일경우  status="COMPLETED,ON_PROFRESS" 이렇게)\n
    :param page: 조회할 페이지 수\n
    :param size: 페이지당 리턴 할 결과 수
    """
    raw_query = jsonable_encoder(crud.novel.get_list_paginated_for_admin(db=db, page_request=page_request,
                                                                         q=q, min_score=min_score, max_score=max_score, created_from=created_from, created_to=created_to,
                                                                         updated_from=updated_from, updated_to=updated_to, is_ficpick=is_ficpick, is_free=is_free,
                                                                         is_exclusive=is_exclusive, is_advertised=is_advertised, is_impressing=is_impressing,
                                                                         language_code=language_code, genre_code=genre_code, status=status))
    page_meta = raw_query.get("page_meta")
    raw_data = raw_query.get("content")

    detail_data_list = [
        NovelTableRow(
            id=data.get("id"),
            is_impressing=data.get("is_impressing"),
            title=get_meta_from_meta_list(meta_list=data.get("novel_meta"), comparison="is_origin", criteria=True, value="title"),
            writer_nickname=data.get("writer_nickname"),
            series_length=len(data.get("series")),
            view_count=0,
            rating=0,
            status=data.get("status"),
            is_ficpic=data.get("is_ficpick"),
            buy_count=0,
            is_exclusive=data.get("is_exclusive"),
            is_advertised=data.get("is_advertised"),
            created_at=data.get("created_at"),
            updated_at=check_updated_date(data.get("series")),
            translation_suggestion=False,
            score=data.get("score")
        ) for data in raw_data]

    return NovelTable(page_meta=page_meta, contents=detail_data_list)


@router.post("/{novel_id}/metadata")
def update_novel_meta(
        *,
        db: Session = Depends(deps.get_db),
        novel_id: int,
        novel_meta_in: NovelStatusEdit
) -> Any:
    """
    어드민 > 작품관리 > 작품 기본 정보 (스코어/노출현황)을 수정합니다.
    :param novel_id:
    :param novel_meta_in:
    """
    novel_data = crud.novel.get_with_join(db=db, id=novel_id)
    return crud.novel.update(
        db=db,
        db_obj=novel_data,
        obj_in=novel_meta_in
    )


@router.get("{novel_id}/series")
def get_series_from_novel(
        *,
        db: Session = Depends(deps.get_db),
        novel_id: int
) -> Any:
    """
    어드민 > 작품관리 > 작품 리스트의 각 회차 > 해당 작품 상세 정보 및 해당 작품의 회차 리스트
    """
    novel = jsonable_encoder(crud.novel.get_with_join(db=db, id=novel_id))
    user = novel.get("writer").get("user")
    series_list = novel.get("series")
    novel_day = novel.get("novel_day")

    def check_novel_day(novel_day_list):
        if novel_day_list:
            return sorted([novel_day.get("open_day") for novel_day in novel_day_list])
        else:
            return None

    novel_meta = NovelMetaData(
        title=get_meta_from_meta_list(meta_list=novel.get("novel_meta"), comparison="is_origin", criteria=True, value="title"),
        nickname=user.get("nickname"),
        writer_nickname=novel.get("writer_nickname"),
        created_at=novel.get("created_at"),
        status=novel.get("status"),
        is_exclusive=novel.get("is_exclusive"),
        is_advertised=novel.get("is_advertised"),
        updated_at=check_updated_date(series_list),
        buy_count=0,
        coupon_count=0,
        sponsor_count=0,
        is_ficpick=novel.get("is_ficpick"),
        series_length=len(series_list),
        like_count=0,
        rating=0,
        novel_day=check_novel_day(novel_day),
        language_code=novel.get("language_code"),
        region_code=novel.get("region_code"),
        genre_code=novel.get("genre_code")
    )

    series_data_list = [SeriesDataInNovelMeta(
        id=series.get("id"),
        order_number=series.get("order_number"),
        is_impressing=series.get("is_impressing"),
        title=get_meta_from_meta_list(meta_list=series.get("series_meta"), comparison="is_origin", criteria=True, value="title"),
        created_at=series.get("created_at"),
        updated_at=series.get("updated_at"),
        rating=0,
        comment=0,
        view_count=0,
        buy_count=0
    ) for series in series_list]

    return {"novel_meta": novel_meta, "series_data_list": series_data_list}