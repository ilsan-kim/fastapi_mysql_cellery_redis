from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import ENUM

from app.db.base_class import Base, same_as


STATUS = ('UNAPPROVED', 'APPROVED', 'FORBIDDEN')


class Series(Base):
    id = Column(Integer, primary_key=True, index=True)
    novel_id = Column(Integer, ForeignKey('novel.id'))
    writer_id = Column(Integer, ForeignKey('writer.id'))
    order_number = Column(Integer, nullable=False)
    status = Column(ENUM(*STATUS), default=STATUS[0])
    is_free = Column(Boolean, default=True)
    published_at = Column(DateTime, default=same_as('created_at'))
    approved_at = Column(DateTime)
    is_deleted = Column(Boolean, default=False)
    is_impressing = Column(Boolean, default=True)

    # One to One relation
    series_statistic = relationship('SeriesStatistic', uselist=False)

    # One to Many relation
    paragraph = relationship('Paragraph', back_populates='series', uselist=True, join_depth=1)
    series_status = relationship('SeriesStatus', back_populates='series', join_depth=1)
    series_meta = relationship('SeriesMeta', back_populates='series')

    # Many to One relation
    novel = relationship('Novel', back_populates='series', join_depth=1)
    writer = relationship('Writer', back_populates='series', join_depth=1)

    # Many to Many relation
    user_read = relationship('UserRead', back_populates='series')
    user_rating = relationship('UserRating', back_populates='series')
    comment = relationship('Comment', back_populates='series')
    coupon_series = relationship('CouponSeries', back_populates='series', join_depth=1)
    cash_series = relationship('CashSeries', back_populates='series', join_depth=1)


class SeriesStatus(Base):
    series_id = Column(Integer, ForeignKey('series.id'), primary_key=True)
    manager_id = Column(Integer, ForeignKey('user.id'), nullable=True)
    status = Column(ENUM(*STATUS))
    reason = Column(String(100), default="기타 회사에서 통용되는 기타 규칙에 위배되는 게시글/덧글")
    is_public = Column(Boolean, default=True)

    # Many to One relation
    series = relationship('Series', back_populates='series_status')


class SeriesStatistic(Base):
    series_id = Column(Integer, ForeignKey('series.id'), primary_key=True, index=True)
    view_count = Column(Integer)
    rating_count = Column(Integer)
    payment_count = Column(Integer)

    # One to One relation
    series = relationship('Series', back_populates='series_statistic')


class SeriesMeta(Base):
    id = Column(Integer, primary_key=True, index=True)
    series_id = Column(Integer, ForeignKey('series.id'), index=True)
    is_origin = Column(Boolean, default=False)
    title = Column(String(100), nullable=False, index=True)
    description = Column(String(1000), default="")
    language_code = Column(String(30), ForeignKey('language.code'), default='kr')

    # Many to One relation
    series = relationship('Series', back_populates='series_meta')
