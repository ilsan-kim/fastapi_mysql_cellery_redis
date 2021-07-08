from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud
from app.schemas import writer
from app.controllers import deps

router = APIRouter()


@router.post("/", response_model=writer.Writer)
def create_writer(
    *,
    db: Session = Depends(deps.get_db),
    writer_in: writer.WriterCreate
) -> Any:
    """
    Create new tag.
    """
    writer = crud.writer.create(db, obj_in=writer_in)
    return writer
