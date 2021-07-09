from app.crud.base import CRUDBase
from app.models.banned_string import BannedString
from app.schemas.banned_string import BannedStringCreate, BannedStringUpdate


class CRUDBannedString(CRUDBase[BannedString, BannedStringCreate, BannedStringUpdate]):
    pass


banned_string = CRUDBannedString(BannedString)