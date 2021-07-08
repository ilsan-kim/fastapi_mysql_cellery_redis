from typing import Any, Dict, Optional, Union, List

from sqlalchemy import or_
from sqlalchemy.orm import Session, joinedload, contains_eager

from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app.models.writer import Writer, Commission
from app.schemas.writer import WriterCreate, WriterUpdate


class CRUDWriter(CRUDBase[Writer, WriterCreate, WriterUpdate]):
    pass


writer = CRUDWriter(Writer)