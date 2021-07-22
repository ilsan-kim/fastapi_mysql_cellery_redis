from typing import Any, Optional, List
from operator import itemgetter
import random

from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse

from .series import get_series_contents
from app import crud
from app.models.series import STATUS
from app.schemas.novel import NovelCreate, Novel, NovelListRow, NovelDetail
from app.schemas.series import SeriesInNovelDetail, SeriesInNovelDetailPage, Series, SeriesCreate
from app.controllers import deps
from app.utils.api.novel import get_sum_of_count, get_avg_rating, get_meta_from_meta_list

router = APIRouter()


@router.post("/", response_model=Novel)
def create_novel(
        *,
        db: Session = Depends(deps.get_db),
        novel_in: NovelCreate
) -> Any:
    """
    Create new novel.
    """

    # validation 영역
    # 작품 스케쥴 / 정기연재인지, 자유연재인지
    if novel_in.is_scheduled and len(novel_in.open_day_list) == 0:
        raise HTTPException(status_code=400, detail=f'정기연재 소설은 연재일을 지정해야 합니다. : {novel_in.open_day_list}')
    elif novel_in.is_scheduled is False and len(novel_in.open_day_list) > 0:
        raise HTTPException(status_code=400, detail=f'자유연재 소설은 연재일을 지정할 수 없습니다. : {novel_in.open_day_list}')
    elif len(novel_in.open_day_list) > 7:
        raise HTTPException(status_code=400, detail=f'연재일은 7일 까지만 지정할 수 있습니다. : {novel_in.open_day_list}')

    # 작품 태그 존재 확인 / 태그는 최대 5개 까지
    [crud.tag.check_presence_by_code(db, code=novel_tag) for novel_tag in novel_in.tag_list]
    if novel_in.tag_list and len(novel_in.tag_list) > 5:
        raise HTTPException(status_code=400, detail=f'태그는 5개까지만 선택할 수 있습니다. : {novel_in.tag_list}')

    # 장르/권역/언어 존재 확인
    crud.genre.check_presence_by_code(db, code=novel_in.genre_code)
    crud.region.check_presence_by_code(db, code=novel_in.region_code)
    crud.language.check_presence_by_code(db, code=novel_in.language_code)

    # 작품 모델 기본 파라미터
    novel_params = {
        'writer_id': novel_in.writer_id,
        'writer_nickname': novel_in.writer_nickname,
        'thumbnail_url': novel_in.thumbnail_url,
        'genre_code': novel_in.genre_code,
        'region_code': novel_in.region_code,
        'language_code': novel_in.language_code,
        'is_scheduled': novel_in.is_scheduled,
        'is_exclusive': novel_in.is_exclusive,
        'is_censored': novel_in.is_censored,
        'is_free': novel_in.is_free,
        'is_event': novel_in.is_event
    }

    # DB 입력 영역
    # 작품 입력
    novel = crud.novel.create(db, obj_in=novel_params)

    # 연재 주기 테이블 입력
    [crud.novel_day.create(db, obj_in={'novel_id': novel.id, 'open_day': novel_day}) for novel_day in novel_in.open_day_list]

    # 태그 테이블 입력
    [crud.novel_tag.create(db, obj_in={'novel_id': novel.id, 'tag_code': novel_tag}) for novel_tag in novel_in.tag_list]

    # 작품 원어의 메타데이터력 입력
    novel_meta_params = {
        'novel_id': novel.id,
        'is_origin': True,
        'title': novel_in.title,
        'description': novel_in.description,
        'language_code': novel_in.language_code
    }
    crud.novel_meta.create(db, obj_in=novel_meta_params)

    return novel


@router.get("/home", response_model=List[NovelListRow])
def get_list_for_home(
        *,
        db: Session = Depends(deps.get_db),
        sort: Optional[str] = "updated_at"
) -> List[NovelListRow]:
    """
    기본 내용외에 추후 확장성을 고려하여, __"writer_id" 와 "is_censored" 파라미터를 함께 리턴합니다.__\n
    """
    novel_list_raw = crud.novel.get_all(db=db)
    novel_list = [
        jsonable_encoder(NovelListRow(
            id=novel.id,
            writer_id=novel.writer_id,
            writer_nickname=novel.writer_nickname,
            thumbnail_url=novel.thumbnail_url,
            genre_code=novel.genre_code,
            is_censored=novel.is_censored,
            is_free=novel.is_free,
            title=novel.novel_meta[0].title,
            description=novel.novel_meta[0].description,
            is_ficpick=novel.is_ficpick,
            view_count=get_sum_of_count([series for series in novel.series], "view_count"),
            like_count=get_sum_of_count([series for series in novel.series], "like_count"),
            rating=get_avg_rating([series for series in novel.series]),
            updated_at=[series for series in novel.series][0].created_at
        ))
        for novel in novel_list_raw]
    if sort == "random":
        random.shuffle(novel_list)
        sorted_data = novel_list
    elif sort == "view_count":
        sorted_data = sorted(novel_list, key=itemgetter("view_count"), reverse=True)
    else:
        sorted_data = sorted(novel_list, key=itemgetter("updated_at"), reverse=True)
    return sorted_data


@router.get("/{novel_id}", response_model=NovelDetail)
def get_detail(
    *,
    db: Session = Depends(deps.get_db),
    novel_id: int,
    language_code: Optional[str] = "kr"
):
    novel_data = crud.novel.get_with_join(db=db, id=novel_id)
    novel_meta = novel_data.novel_meta
    series = novel_data.series
    novel_detail = NovelDetail(
        id=novel_data.id,
        writer_id=novel_data.writer_id,
        writer_nickname=novel_data.writer_nickname,
        title=get_meta_from_meta_list(meta_list=novel_meta, comparison='language_code', criteria=language_code, value="title"),
        description=get_meta_from_meta_list(meta_list=novel_meta, comparison='language_code', criteria=language_code, value="description"),
        thumbnail_url=novel_data.thumbnail_url,
        genre_code=novel_data.genre_code,
        is_free=novel_data.is_free,
        is_censored=novel_data.is_censored,
        is_ficpick=novel_data.is_ficpick,
        is_exclusive=novel_data.is_exclusive,
        view_count=get_sum_of_count(series, "view_count"),
        rating=get_avg_rating(series),
        status=novel_data.status,
        open_day=sorted([novel_day.open_day for novel_day in novel_data.novel_day]),
        tag_list=[novel_tag.tag_code for novel_tag in novel_data.novel_tag],
        auto_payment=False
    )
    return novel_detail


@router.post("/{novel_id}/series", response_model=Series)
def create_series(
        *,
        novel_id: int,
        db: Session = Depends(deps.get_db),
        series_in: SeriesCreate
) -> Any:

    """
    Create new series.
    """
    # series params
    novel_data = crud.novel.get(db=db, id=novel_id)
    writer_id = novel_data.writer_id
    novel_is_free = novel_data.is_free
    paid_from = novel_data.need_pay_from
    order_number = crud.series.get_order_number(db=db, novel_id=novel_id)
    novel_lang = novel_data.language_code

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
        'status': STATUS[0],
        'is_free': is_free
    }

    # db 입력 영역
    series = crud.series.create(db, obj_in=series_params)

    # paragraph 입력
    [crud.paragraph.create(db, obj_in={
        "series_id": series.id,
        "order_number": index,
        "text": series_in.paragraph[index],
        "language_code": novel_lang,
        "is_origin": True,
        "is_selected": True
    })
     for index in range(len(series_in.paragraph))]

    # series_meta 입력
    crud.series_meta.create(db, obj_in={
        "series_id": series.id,
        "is_origin": True,
        "title": series_in.title,
        "description": series_in.description,
        "language_code": novel_lang
    })

    # series_status 입력
    crud.series_status.create(db, obj_in={
        "series_id": series.id,
        "manager_id": None,
        "status": STATUS[0],
        "reason": None
    })

    # series_statistic 테이블 자동 생성
    crud.series_statistic.create(db, obj_in={
        "series_id": series.id,
        "view_count": 0,
        "rating_count": 0,
        "payment_count": 0,
        "language_code": novel_lang
    })

    '''
    추가할것 
    is_complete == True 면 작품 상태 변경 
    '''

    return series


@router.get("/{novel_id}/series", response_model=SeriesInNovelDetailPage)
def get_series_list(*,
                    page_request: dict = Depends(deps.get_page_request_for_series),
                    db: Session = Depends(deps.get_db),
                    novel_id: int,
                    order: Optional[str] = "latest",
                    language_code: Optional[str] = "kr"):
    raw_query = crud.series.get_list_paginated(db=db, page_request=page_request, id=novel_id, order=order)

    page_meta = raw_query.get("page_meta")
    raw_data = raw_query.get("content")

    series = [SeriesInNovelDetail(
        id=series.id,
        title=get_meta_from_meta_list(meta_list=series.series_meta, comparison="language_code", criteria=language_code, value="title"),
        order_number=series.order_number,
        created_at=series.created_at,
        rating=series.series_statistic.rating,
        view_count=series.series_statistic.view_count
    ) for series in raw_data]
    return SeriesInNovelDetailPage(page_meta=page_meta, contents=series)


@router.get("/{novel_id}/first")
def get_first_series(*,
                     db: Session = Depends(deps.get_db),
                     novel_id: int,
                     language_code: Optional[str] = "kr"):
    series_list = jsonable_encoder(crud.novel.get_with_join(db=db, id=novel_id).series)
    first_series_id = sorted(series_list, key=itemgetter("order_number"))[0].get("id")
    response = get_series_contents(db=db, series_id=first_series_id, language_code=language_code)
    return response


@router.get("/{novel_id}/latest")
def get_latest_series(*,
                     db: Session = Depends(deps.get_db),
                     novel_id: int,
                     language_code: Optional[str] = "kr"):
    series_list = jsonable_encoder(crud.novel.get_with_join(db=db, id=novel_id).series)
    first_series_id = sorted(series_list, key=itemgetter("order_number"), reverse=True)[0].get("id")
    response = get_series_contents(db=db, series_id=first_series_id, language_code=language_code)
    return response


@router.post("/{novel_id}/notice")
def post_novel_notice(*,
                      db: Session = Depends(deps.get_db),
                      novel_id: int):
    return
