from typing import Any, Optional, List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import crud
from app.schemas import series, novel
from app.models.series import STATUS
from app.controllers import deps

router = APIRouter()


@router.get("/")
def create_language_code(
        *,
        db: Session = Depends(deps.get_db)
) -> Any:
    """
    Create new language.
    """
    return "hello world"
