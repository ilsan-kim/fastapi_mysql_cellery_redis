import enum

from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import ENUM

from app.db.base_class import Base, BaseNoDatetime

STATUS = ('ON_PROGRESS', 'COMPLETED', 'PAUSED')


class Novel(Base):
    id = Column(Integer, primary_key=True, index=True)
    writer_id = Column(Integer, ForeignKey('user.id'), primary_key=True, nullable=False)
    writer_nickname = Column(String(50))
    title = Column(String(50), nullable=False, index=True)
    description = Column(String(1000), default="")
    thumbnail_url = Column(String(300), default="")
    status = Column(ENUM(*STATUS), default=STATUS[0])
    genre = Column(String(30), ForeignKey('genre.name'))
    region = Column(String(30), ForeignKey('region.name'))
    language = Column(String(30), ForeignKey('language.name'))
    is_ficpick = Column(Boolean, default=False)
    is_exclusive = Column(Boolean, default=False)
    is_censored = Column(Boolean, default=False)
    is_scheduled = Column(Boolean, default=False)
    is_free = Column(Boolean, default=True)
    is_advertised = Column(Boolean, default=False)
    is_event = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)
    referral_url = Column(String(300), default="")
    score = Column(Integer, default=0)

    # One to Many relation table
    novel_notice = relationship('NovelNotice', back_populates='novel', uselist=True, join_depth=1)
    series = relationship('Series', back_populates='novel', uselist=True, join_depth=1)
    novel_day = relationship('NovelDay', back_populates='novel', uselist=True)

    # One to One relation table
    writer = relationship('User', back_populates='novel', uselist=False, join_depth=2)

    # Many to Many relation table
    user_like = relationship('UserLike', back_populates='novel', join_depth=1)
    novel_tag = relationship('NovelTag', back_populates='novel', join_depth=1)
    recommend = relationship('Recommend', back_populates='novel', join_depth=1)


class NovelDay(BaseNoDatetime):
    __tablename__ = "novel_day"

    novel_id = Column(ForeignKey('novel.id'), primary_key=True, index=True)
    open_day = Column(Integer)
