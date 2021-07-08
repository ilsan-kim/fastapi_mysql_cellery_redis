from app.crud.base import CRUDBase
from app.models.genre import Genre, GenreDetail
from app.models.tag import Tag, TagDetail
from app.models.language import Language, LanguageDetail
from app.models.region import Region, RegionDetail
from app.schemas.field import FieldCreate, FieldUpdate, CodeFieldCreate, CodeFieldUpdate, FieldDetailCreate, FieldDetailUpdate


class CRUDGenre(CRUDBase[Genre, FieldCreate, FieldUpdate]):
    pass


class CRUDTag(CRUDBase[Tag, FieldCreate, FieldUpdate]):
    pass


class CRUDLanguage(CRUDBase[Language, CodeFieldCreate, CodeFieldUpdate]):
    pass


class CRUDRegion(CRUDBase[Language, CodeFieldCreate, CodeFieldUpdate]):
    pass


class CRUDGenreDetail(CRUDBase[GenreDetail, FieldDetailCreate, FieldDetailUpdate]):
    pass


class CRUDTagDetail(CRUDBase[TagDetail, FieldDetailCreate, FieldDetailUpdate]):
    pass


class CRUDLanguageDetail(CRUDBase[LanguageDetail, FieldDetailCreate, FieldDetailUpdate]):
    pass


class CRUDRegionDetail(CRUDBase[RegionDetail, FieldDetailCreate, FieldDetailUpdate]):
    pass


genre = CRUDGenre(Genre)
tag = CRUDTag(Tag)
language = CRUDLanguage(Language)
region = CRUDRegion(Region)
genre_detail = CRUDGenreDetail(GenreDetail)
tag_detail = CRUDTagDetail(TagDetail)
language_detail = CRUDLanguageDetail(LanguageDetail)
region_detail = CRUDRegionDetail(RegionDetail)
