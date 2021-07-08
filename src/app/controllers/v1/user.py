from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud
from app.schemas import user
from app.controllers import deps

router = APIRouter()


@router.post("", response_model=user.User)
def create_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: user.UserCreate
) -> Any:
    """
    Create new user.
    """
    user = crud.user.create(db, obj_in=user_in)
    return user
