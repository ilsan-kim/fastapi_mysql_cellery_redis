from typing import Any, Optional, List, Union

from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app import crud
from app.schemas.series import SeriesRead
from app.schemas.user_rating import UserRating, UserRatingCreate
from app.schemas.comment import CommentBase, CommentCreate, Comment, CommentDetail, CommentPage
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


@router.get("/{series_id}/comment", response_model=CommentPage)
def get_comments_in_series(*,
                           page_request: dict = Depends(deps.get_page_request_size_ten),
                           db: Session = Depends(deps.get_db),
                           series_id: int):
    raw_query = crud.comment.get_list_with_user_paginated(db=db, page_request=page_request, series_id=series_id)

    page_meta = raw_query.get("page_meta")
    raw_data = raw_query.get("content")

    comments = [CommentDetail(
        id=comments.id,
        user_id=comments.user_id,
        series_id=comments.series_id,
        nickname=comments.user.nickname,
        profile_url=comments.user.profile_url,
        content=comments.content,
        image_url=comments.image_url,
        like_count=comments.like_count,
        created_at=comments.created_at) for comments in raw_data]

    return CommentPage(page_meta=page_meta, contents=comments)


@router.post("/{series_id}/rating")
def post_rating_to_series(*,
                          series_id: int,
                          # current_user 파라미터 추후 수정 필요
                          current_user: int = 2,
                          rating_in: UserRatingCreate,
                          db: Session = Depends(deps.get_db)):

    series_statistic = crud.series_statistic.get_by_series_id(db=db, series_id=series_id)
    prev_rating = crud.user_rating.get_by_ids(db=db, series_id=series_id, user_id=current_user)

    # 이미 평점 매긴 경우 평점 수정
    if prev_rating:
        rating_count = series_statistic.rating_count
        print(f"직전까지 회차 통계의 레이팅 참여 갯수 : {rating_count}")
        total_rating = series_statistic.total_rating - prev_rating.rating + rating_in.rating
        print(f"직전까지 회차 통계의 레이팅 총합 : {series_statistic.total_rating}")
        print(f"평가자의 직전 평가의 레이팅 점수 : {prev_rating.rating}")
        print(f"평가자의 이번 평가의 레이팅 점수 : {rating_in.rating}")
        crud.series_statistic.update(db=db, db_obj=series_statistic,
                                     obj_in={
                                         "rating_count": rating_count,
                                         "total_rating": total_rating,
                                         "rating": total_rating / rating_count})
        # 레이팅에 0을 줘도 안변하는 에러,, 해결해야함 !!!!!!!!!!!!
        return crud.user_rating.update(db=db, db_obj=prev_rating, obj_in=UserRating(series_id=series_id,
                                                                                    user_id=current_user,
                                                                                    rating=rating_in.rating))
    # 평점 안매긴 경우 새로 생성
    else:
        rating_count = series_statistic.rating_count + 1
        total_rating = series_statistic.total_rating + rating_in.rating
        crud.series_statistic.update(db=db, db_obj=series_statistic,
                                     obj_in={
                                         "rating_count": rating_count,
                                         "total_rating": total_rating,
                                         "rating": total_rating / rating_count})
        return crud.user_rating.create(db=db, obj_in=UserRating(series_id=series_id,
                                                                user_id=current_user,
                                                                rating=rating_in.rating))
