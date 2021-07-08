from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class OtherNovel(Base):
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(30), index=True)
    is_activate = Column(Boolean, default=True)

    # Many to Many relation
    user_other_novel = relationship('UserOtherNovel', back_populates='other_novel')

    # One to Many relation
    other_novel_detail = relationship('OtherNovelDetail', back_populates='other_novel', uselist=True)


class OtherNovelDetail(Base):
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(30), ForeignKey('other_novel.code'), index=True)
    language_code = Column(String(30), ForeignKey('language.code'), default='kr')
    name = Column(String(30), default="")

    # Many to One relation
    other_novel = relationship('OtherNovel', back_populates='other_novel_detail')