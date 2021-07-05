from sqlalchemy import Column, Integer, ForeignKey, String

from app.db.base_class import Base


class NovelTag(Base):
    novel_id = Column(Integer, ForeignKey('novel.id'), primary_key=True, index=True)
    tag_name = Column(String(30), ForeignKey('tag.name'), index=True)
