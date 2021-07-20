from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import ENUM

from app.db.base_class import Base

STATUS = ('ON_PROGRESS', 'COMPLETED', 'PAUSED')


class Novel(Base):
    id = Column(Integer, primary_key=True, index=True)
    writer_id = Column(Integer, ForeignKey('writer.id'), nullable=False)
    writer_nickname = Column(String(50))
    thumbnail_url = Column(String(300), default="")
    status = Column(ENUM(*STATUS), default=STATUS[0])
    genre_code = Column(String(30), ForeignKey('genre.code'))
    region_code = Column(String(30), ForeignKey('region.code'))
    language_code = Column(String(30), ForeignKey('language.code'))
    is_ficpick = Column(Boolean, default=False)
    is_exclusive = Column(Boolean, default=False)
    is_censored = Column(Boolean, default=False)
    is_scheduled = Column(Boolean, default=False)
    is_free = Column(Boolean, default=True)
    need_pay_from = Column(Integer, default=None)
    is_advertised = Column(Boolean, default=False)
    is_event = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)
    referral_url = Column(String(300), default="")
    score = Column(Integer, default=0)
    is_impressing = Column(Boolean, default=True)
    isbn_code = Column(String(30), default="")

    # One to Many relation
    novel_notice = relationship('NovelNotice', back_populates='novel', uselist=True, join_depth=1)
    series = relationship('Series', back_populates='novel', uselist=True, join_depth=1, order_by="desc(Series.order_number)")
    novel_meta = relationship('NovelMeta', back_populates='novel', uselist=True)
    novel_day = relationship('NovelDay', back_populates='novel', uselist=True)

    # One to One relation
    writer = relationship('Writer', back_populates='novel', uselist=False, join_depth=2)

    # Many to Many relation
    user_novel = relationship('UserNovel', back_populates='novel', join_depth=1)
    novel_tag = relationship('NovelTag', back_populates='novel', join_depth=1)
    recommend = relationship('Recommend', back_populates='novel', join_depth=1)


class NovelDay(Base):
    novel_id = Column(Integer, ForeignKey('novel.id'), primary_key=True, index=True)
    open_day = Column(Integer, primary_key=True, index= True)

    # Many to One relation
    novel = relationship('Novel', back_populates='novel_day')


class NovelMeta(Base):
    id = Column(Integer, primary_key=True, index=True)
    novel_id = Column(Integer, ForeignKey('novel.id'), index=True)
    is_origin = Column(Boolean, default=False)
    title = Column(String(50), nullable=False, index=True)
    description = Column(String(1000), default="")
    language_code = Column(String(30), ForeignKey('language.code'), default='')

    # Many to One relation
    novel = relationship('Novel', back_populates='novel_meta')
