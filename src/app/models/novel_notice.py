from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class NovelNotice(Base):
    id = Column(Integer, primary_key=True, index=True)
    novel_id = Column(Integer, ForeignKey('novel.id'))
    writer_id = Column(Integer, ForeignKey('user.id'))
    title = Column(String(100), index=True, nullable=False)
    content = Column(Text(20_000), default="")

    # Many to One relation table
    novel = relationship('Novel', back_populates='paragraph', join_depth=1)
    writer = relationship('User', back_populates='paragraph', join_depth=2)
