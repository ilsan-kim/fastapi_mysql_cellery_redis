from typing import Any, Optional, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud
from app.schemas import novel
from app.controllers import deps

router = APIRouter()


@router.post("/", response_model=novel.Novel)
def create_novel(
        *,
        db: Session = Depends(deps.get_db),
        novel_in: novel.NovelCreate
) -> Any:
    """
    Create new novel.
    """
    # 작품 모델 기본 파라미터
    novel_params = {
        'writer_id' : novel_in.writer_id,
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
    novel = crud.novel.create(db, obj_in=novel_params)

    # 작품 스케쥴 / 정기연재인지, 자유연재인지
    if novel.is_scheduled and len(novel_in.open_day_list) == 0:
        raise HTTPException(status_code=400, detail=f'정기연재 소설은 연재일을 지정해야 합니다. : {novel_in.open_day_list}')
    elif novel.is_scheduled is False and len(novel_in.open_day_list) > 0:
        raise HTTPException(status_code=400, detail=f'자유연재 소설은 연재일을 지정할 수 없습니다. : {novel_in.open_day_list}')
    elif len(novel_in.open_day_list) > 7:
        raise HTTPException(status_code=400, detail=f'연재일은 7일 까지만 지정할 수 있습니다. : {novel_in.open_day_list}')
    elif novel.is_scheduled is True and novel_in.open_day_list:
        [crud.novel_day.create(db, obj_in={'novel_id': novel.id, 'open_day': novel_day})
         for novel_day in novel_in.open_day_list]

    # 작품 태그 확인 / 태그는 최대 5개 까지
    if novel_in.tag_list and len(novel_in.tag_list) > 5:
        raise HTTPException(status_code=400, detail=f'태그는 5개까지만 선택할 수 있습니다. : {novel_in.tag_list}')
    elif novel_in.tag_list and len(novel_in.tag_list) <= 5:
        [crud.novel_tag.create(db, obj_in={'novel_id': novel.id, 'tag_code': novel_tag})
         for novel_tag in novel_in.tag_list]

    # 작품 원어의 메타데이터
    novel_meta_params = {
        'novel_id': novel.id,
        'is_origin': True,
        'title': novel_in.title,
        'description': novel_in.description,
        'language_code': novel_in.language_code
    }
    crud.novel_meta.create(db, obj_in=novel_meta_params)

    return novel
