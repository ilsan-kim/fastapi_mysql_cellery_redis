from typing import Any, Dict, Optional, Union, List

from sqlalchemy import or_
from sqlalchemy.orm import Session, joinedload, contains_eager

from app.crud.base import CRUDBase
from app.models.banned_string import BannedString
from app.schemas.banned_string import BannedStringCreate, BannedStringUpdate


class CRUDBannedString(CRUDBase[BannedString, BannedStringCreate, BannedStringUpdate]):
    pass


banned_string = CRUDBannedString(BannedString)