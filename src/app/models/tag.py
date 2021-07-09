from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Tag(Base):
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(30), nullable=False, index=True, unique=True)
    is_activate = Column(Boolean, default=True)

    # Many to Many relation
    novel_tag = relationship('NovelTag', back_populates='tag')
    user_tag = relationship('UserTag', back_populates='tag')

    # One to Many relation
    tag_detail = relationship('TagDetail', back_populates='tag', uselist=True)


class TagDetail(Base):
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(30), ForeignKey('tag.code'), index=True)
    language_code = Column(String(30), ForeignKey('language.code'), default='kr')
    name = Column(String(30), default="")

    # Many to One relation
    tag = relationship('Tag', back_populates='tag_detail')