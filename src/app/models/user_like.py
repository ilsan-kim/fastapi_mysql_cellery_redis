from sqlalchemy import Column, Integer, ForeignKey

from app.db.base_class import Base


class UserLike(Base):
    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True, index=True)
    novel_id = Column(Integer, ForeignKey('novel.id'), primary_key=True, index=True)
