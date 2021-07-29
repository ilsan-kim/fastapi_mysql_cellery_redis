from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_

from app.crud.base import CRUDBase
from app.models.user_rating import UserRating
from app.schemas.user_rating import UserRatingCreate, UserRatingUpdate


class CRUDUserRating(CRUDBase[UserRating, UserRatingCreate, UserRatingUpdate]):
    def get_by_ids(self, db: Session, series_id: int, user_id: int):
        return db.query(self.model).filter(self.model.series_id == series_id).filter(self.model.user_id == user_id).first()


user_rating = CRUDUserRating(UserRating)
