from typing import Any, Optional, List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import crud
from app.schemas.series import SeriesRead
from app.schemas.comment import CommentBase, CommentCreate, Comment, CommentDetail
from app.controllers import deps
from app.utils.api.novel import get_meta_from_meta_list

router = APIRouter()


@router.get("/{series_id}", response_model=SeriesRead)
def get_series_contents(
        *,
        series_id: int,
        language_code: str = "kr",
        db: Session = Depends(deps.get_db)) -> Any:
    """
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


@router.post("/{series_id}/comment", response_model=Comment)
def post_comment_to_series(*,
                           db: Session = Depends(deps.get_db),
                           series_id: int,
                           series_in: CommentBase,
                           # current_user 파라미터 추후 수정 필요
                           current_user: int = 2):
    # user_id 파라미터는 나중에 로그인 달때 다시 고민
    return crud.comment.create(db=db, obj_in=CommentCreate(series_id=series_id,
                                                           user_id=current_user,
                                                           content=series_in.content,
                                                           image_url=series_in.image_url))


@router.get("/{series_id}/comment", response_model=List[CommentDetail])
def get_comments_in_series(*,
                           db: Session = Depends(deps.get_db),
                           series_id: int):
    comments_raw = crud.comment.get_list_with_user(db=db, series_id=series_id)
    comments = [CommentDetail(
        id=comments.id,
        user_id=comments.user_id,
        series_id=comments.series_id,
        nickname=comments.user.nickname,
        profile_url=comments.user.profile_url,
        content=comments.content,
        image_url=comments.image_url,
        like_count=comments.like_count,
        created_at=comments.created_at) for comments in comments_raw]
    return comments
