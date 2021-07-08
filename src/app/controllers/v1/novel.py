from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud
from app.schemas import novel
from app.controllers import deps
from app.core import errors

router = APIRouter()


@router.post("/", response_model=novel.Novel)
def create_novel(
        *,
        db: Session = Depends(deps.get_db),
        novel_in: novel.NovelCreate,
        novel_day_in: novel.NovelDayCreate,
        novel_tag_in: novel.NovelTagCreate,
        novel_meta_in: novel.NovelMetaCreate
) -> Any:
    """
    Create new novel.
    """
    novel = crud.novel.create(db, obj_in=novel_in)

    # 작품 스케쥴 / 정기연재인지, 자유연재인지
    if novel.is_scheduled is True and novel_day_in.open_day_list:
        [crud.novel_day.create(db, obj_in={'novel_id': novel.id, 'open_day': novel_day})
         for novel_day in novel_day_in.open_day_list]
    elif novel.is_scheduled and novel_day_in.open_day_list is None:
        raise errors.NovelException('정기연재 소설은 연재일을 지정해야 합니다.', novel_day_in)
    elif novel.is_scheduled is False and novel_day_in.open_day_list:
        raise errors.NovelException('자유연재 소설은 연재일을 지정할 수 없습니다.', novel_day_in)

    # 작품 태그 확인 / 태그는 최대 5개 까지
    if novel_tag_in and len(novel_tag_in.tag_list) <= 5:
        [crud.novel_tag.create(db, obj_in={'novel_id': novel.id, 'tag_code': novel_tag})
         for novel_tag in novel_tag_in.tag_list]
    elif novel_tag_in and len(novel_tag_in.tag_list) > 6:
        raise errors.NovelException('태그는 5개까지만 선택할 수 있습니다.', novel_tag_in.tag_list)

    if novel_meta_in:
        novel_meta_params = {
            'novel_id': novel.id,
            'is_origin': True,
            'title': novel_meta_in.title,
            'description': novel_meta_in.description,
            'language_code': novel_meta_in.language_code
        }
        crud.novel_meta.create(db, obj_in=novel_meta_params)

    return novel
