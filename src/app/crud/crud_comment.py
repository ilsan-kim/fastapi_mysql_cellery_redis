from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_

from app.crud.base import CRUDBase
from app.models.comment import Comment as CommentModel
from app.schemas.comment import CommentCreate, CommentUpdate, Comment


class CRUDComment(CRUDBase[CommentModel, CommentCreate, CommentUpdate]):
    def get_list_with_user(self, db: Session, series_id: int) -> Comment:
        return db.query(self.model).\
            join(self.model.user).\
            options(joinedload(self.model.user)).\
            filter(self.model.series_id == series_id).all()


comment = CRUDComment(CommentModel)
