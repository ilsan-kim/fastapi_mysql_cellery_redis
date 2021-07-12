from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud
from app.schemas import banned_string
from app.controllers import deps

router = APIRouter()


@router.post("/", response_model=banned_string.BannedString)
def banned_string(
        *,
        db: Session = Depends(deps.get_db),
        banned_string_in: banned_string.BannedStringCreate
) -> Any:
    """
    Create new tag.
    """
    banned_string = crud.banned_string.create(db, obj_in=banned_string_in)
    return banned_string
