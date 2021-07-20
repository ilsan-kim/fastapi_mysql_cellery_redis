from sqlalchemy import Column, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class UserNovel(Base):
    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True, index=True)
    novel_id = Column(Integer, ForeignKey('novel.id'), primary_key=True, index=True)
    like = Column(Boolean, default=False)
    auto_payment = Column(Boolean, default=False)

    # Many to Many relation
    user = relationship('User', back_populates='user_novel')
    novel = relationship('Novel', back_populates='user_novel')