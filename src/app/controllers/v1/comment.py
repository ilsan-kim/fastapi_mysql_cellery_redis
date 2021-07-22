from typing import Any, Optional, List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app import crud
from app.schemas.series import SeriesRead
from app.schemas.comment import CommentBase, CommentCreate, Comment, CommentDetail
from app.controllers import deps
from app.utils.api.novel import get_meta_from_meta_list

router = APIRouter()


@router.post("/{comment_id}/like")
def post_like_to_comment(
        *,
        comment_id: int,
        db: Session = Depends(deps.get_db),
        # current_user 파라미터는 로그인 붙인 후 수정
        cureent_user: int = 2) -> Any:
    """
    댓글 좋아요 기능
    """
    comment = crud.comment.get(db=db, id=comment_id)
    try:
        crud.user_comment.create(db=db, obj_in={"comment_id": comment_id, "user_id": cureent_user})
    except IntegrityError:
        raise HTTPException(status_code=400, detail="이미 좋아요 한 댓글입니다.")

    return crud.comment.update(db=db, db_obj=comment, obj_in={"like_count": comment.like_count + 1})
