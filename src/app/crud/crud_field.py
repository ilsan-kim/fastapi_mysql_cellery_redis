from typing import Any, Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase, ModelType, CreateSchemaType, UpdateSchemaType
from app.models.other_novel import OtherNovel
from app.models.genre import Genre, GenreDetail
from app.models.tag import Tag, TagDetail
from app.models.language import Language, LanguageDetail
from app.models.region import Region, RegionDetail
from app.schemas.field import FieldCreate, FieldUpdate, CodeFieldCreate, CodeFieldUpdate, FieldDetailCreate, FieldDetailUpdate


# base class for field categories
class CRUDFieldBase(CRUDBase[ModelType, CreateSchemaType, UpdateSchemaType]):
    def get_by_code(self, db: Session, code: Any) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.code == code).first()

    def check_presence_by_code(self, db: Session, code: Any) -> Any:
        if self.get_by_code(db=db, code=code) is None:
            raise HTTPException(status_code=400, detail='입력한 값이 존재하지 않습니다.')


class CRUDGenre(CRUDFieldBase[Genre, FieldCreate, FieldUpdate]):
    pass


class CRUDTag(CRUDFieldBase[Tag, FieldCreate, FieldUpdate]):
    pass


class CRUDLanguage(CRUDFieldBase[Language, CodeFieldCreate, CodeFieldUpdate]):
    pass


class CRUDRegion(CRUDFieldBase[Language, CodeFieldCreate, CodeFieldUpdate]):
    pass


class CRUDOtherNovel(CRUDFieldBase[OtherNovel, FieldCreate, FieldUpdate]):
    pass


class CRUDGenreDetail(CRUDFieldBase[GenreDetail, FieldDetailCreate, FieldDetailUpdate]):
    pass


class CRUDTagDetail(CRUDFieldBase[TagDetail, FieldDetailCreate, FieldDetailUpdate]):
    pass


class CRUDLanguageDetail(CRUDFieldBase[LanguageDetail, FieldDetailCreate, FieldDetailUpdate]):
    pass


class CRUDRegionDetail(CRUDFieldBase[RegionDetail, FieldDetailCreate, FieldDetailUpdate]):
    pass


genre = CRUDGenre(Genre)
tag = CRUDTag(Tag)
language = CRUDLanguage(Language)
region = CRUDRegion(Region)
other_novel = CRUDOtherNovel(OtherNovel)
genre_detail = CRUDGenreDetail(GenreDetail)
tag_detail = CRUDTagDetail(TagDetail)
language_detail = CRUDLanguageDetail(LanguageDetail)
region_detail = CRUDRegionDetail(RegionDetail)
