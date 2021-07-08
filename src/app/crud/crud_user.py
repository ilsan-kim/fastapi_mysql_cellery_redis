from typing import Any, Dict, Optional, Union, List

from sqlalchemy import or_
from sqlalchemy.orm import Session, joinedload, contains_eager

from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        db_obj = User(
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
            nickname=obj_in.nickname,
            phone_number=obj_in.phone_number,
            gender=obj_in.gender,
            language_code=obj_in.language_code
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


user = CRUDUser(User)
