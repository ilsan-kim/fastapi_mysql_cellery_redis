from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class NovelTag(Base):
    novel_id = Column(Integer, ForeignKey('novel.id'), primary_key=True, index=True)
    tag_code = Column(String(30), ForeignKey('tag.code'), primary_key=True, index=True)

    # Many to Many relation
    novel = relationship('Novel', back_populates='novel_tag')
    tag = relationship('Tag', back_populates='novel_tag')