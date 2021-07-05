from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import ENUM

from app.db.base_class import Base, same_as


STATUS = ('UNAPPROVED', 'APPROVED', 'FORBIDDEN')


class Series(Base):
    id = Column(Integer, primary_key=True, index=True)
    novel_id = Column(Integer, ForeignKey('novel.id'))
    writer_id = Column(Integer, ForeignKey('user.id'))
    order_number = Column(Integer, nullable=False)
    title = Column(String(100), nullable=False, index=True)
    status = Column(ENUM(*STATUS), default=STATUS[0])
    is_free = Column(Boolean, default=True)
    published_at = Column(DateTime, default=same_as('created_at'))
    approved_at = Column(DateTime)
    is_deleted = Column(Boolean, default=False)
    is_impressed = Column(Boolean, default=True)

    # One to One relation table
    series_statistic = relationship('SeriesStatistic', uselist=False)

    # One to Many relation table
    paragraph = relationship('Paragraph', back_populates='series', uselist=True, join_depth=1)
    series_status = relationship('SeriesStatus', back_populates='series', join_depth=1)

    # Many to One relation table
    novel = relationship('Novel', back_populates='series', join_depth=1)
    writer = relationship('User', back_populates='series', join_depth=1)

    # Many to Many relation table
    user_read = relationship('UserRead', back_populates='series')
    comment = relationship('Comment', back_populates='series')


class SeriesStatus(Base):
    series_id = Column(Integer, ForeignKey('series.id'), primary_key=True)
    manager_id = Column(Integer, ForeignKey('user.id'), nullable=True)
    status = Column(ENUM(*STATUS))
    reason = Column(String(100), default="기타 회사에서 통용되는 기타 규칙에 위배되는 게시글/덧글")
    is_public = Column(Boolean, default=True)


class SeriesStatistic(Base):
    series_id = Column(Integer, ForeignKey('series.id'), primary_key=True, index=True)
    view_count = Column(Integer)
    rating_count = Column(Integer)
    payment_count = Column(Integer)
