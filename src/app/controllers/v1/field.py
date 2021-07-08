from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud
from app.schemas import field
from app.controllers import deps


router = APIRouter()


@router.post("/tag", response_model=field.Field)
def create_tag_code(
        *,
        db: Session = Depends(deps.get_db),
        field_in: field.FieldCreate
) -> Any:
    """
    Create new tag.
    """
    dup_check_query = crud.tag.get_by_code(db, code=field_in.code)
    if dup_check_query:
        raise HTTPException(status_code=400, detail=f'이미 입력한 태그가 있습니다. {field_in.code}')
    tag = crud.tag.create(db, obj_in=field_in)
    return tag


@router.post("/genre", response_model=field.Field)
def create_genre_code(
        *,
        db: Session = Depends(deps.get_db),
        field_in: field.FieldCreate
) -> Any:
    """
    Create new genre.
    """
    genre = crud.genre.create(db, obj_in=field_in)
    return genre


@router.post("/region", response_model=field.CodeField)
def create_region_code(
        *,
        db: Session = Depends(deps.get_db),
        field_in: field.CodeFieldCreate
) -> Any:
    """
    Create new region.
    """
    region = crud.region.create(db, obj_in=field_in)
    return region


@router.post("/language", response_model=field.CodeField)
def create_language_code(
        *,
        db: Session = Depends(deps.get_db),
        field_in: field.CodeFieldCreate
) -> Any:
    """
    Create new language.
    """
    language = crud.language.create(db, obj_in=field_in)
    return language


''' 이하 추후 사용 (운영자가 직접 필드 코드에 각 번역값 붙이게 될 때)
@router.post("/tag/detail", response_model=field.FieldDetail)
def create_tag_detail(
        *,
        db: Session = Depends(deps.get_db),
        field_in: field.FieldDetailCreate
) -> Any:
    """
    Create new tag.
    """
    tag_detail = crud.tag_detail.create(db, obj_in=field_in)
    return tag_detail


@router.post("/genre/detail", response_model=field.FieldDetail)
def create_genre_detail(
        *,
        db: Session = Depends(deps.get_db),
        field_in: field.FieldDetailCreate
) -> Any:
    """
    Create new tag.
    """
    genre_detail = crud.genre_detail.create(db, obj_in=field_in)
    return genre_detail


@router.post("/region/detail", response_model=field.FieldDetail)
def create_region_detail(
        *,
        db: Session = Depends(deps.get_db),
        field_in: field.FieldDetailCreate
) -> Any:
    """
    Create new tag.
    """
    region_detail = crud.region_detail.create(db, obj_in=field_in)
    return region_detail


@router.post("/language/detail", response_model=field.FieldDetail)
def create_language_detail(
        *,
        db: Session = Depends(deps.get_db),
        field_in: field.FieldDetailCreate
) -> Any:
    """
    Create new tag.
    """
    create_language_detail = crud.language_detail.create(db=db, obj_in=field_in)
    return create_language_detail
'''
