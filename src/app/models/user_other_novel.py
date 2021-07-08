from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class UserOtherNovel(Base):
    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True, index=True)
    other_novel_code = Column(String(100), ForeignKey('other_novel.code'), primary_key=True, index=True)

    # Many to Many relation
    user = relationship('User', back_populates='user_other_novel')
    other_novel = relationship('OtherNovel', back_populates='user_other_novel')