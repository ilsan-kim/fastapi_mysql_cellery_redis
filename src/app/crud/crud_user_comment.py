from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_

from app.crud.base import CRUDBase
from app.models.user_comment import UserComment as UserCommentModel
from app.schemas.user_comment import UserCommentCreate, UserCommentUpdate, UserComment


class CRUDUserComment(CRUDBase[UserCommentModel, UserCommentCreate, UserCommentUpdate]):
    pass


user_comment = CRUDUserComment(UserCommentModel)
