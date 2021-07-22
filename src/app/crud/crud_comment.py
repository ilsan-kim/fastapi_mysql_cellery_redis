from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_

from app.crud.base import CRUDBase
from app.models.comment import Comment as CommentModel
from app.schemas.comment import CommentCreate, CommentUpdate, Comment
from app.schemas.page_response import paginated_query


class CRUDComment(CRUDBase[CommentModel, CommentCreate, CommentUpdate]):
    def get_list_with_user_paginated(self, db: Session, page_request: dict, series_id: int) -> Comment:

        query = db.query(self.model).\
            join(self.model.user).\
            options(joinedload(self.model.user)).\
            filter(self.model.series_id == series_id).group_by(self.model.id)

        page = page_request.get("page", 1)
        size = page_request.get("size", 20)

        return paginated_query(
            page_request,
            query,
            lambda x: x.order_by(self.model.id).limit(size).offset((page - 1) * size).all()
        )


comment = CRUDComment(CommentModel)
