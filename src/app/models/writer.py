from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Writer(Base):
    id = Column(Integer, ForeignKey('user.id'), primary_key=True, index=True, nullable=False)
    is_contracted = Column(Boolean, default=False)
    commission_rate = Column(Float, default=0.6)
    nickname_1 = Column(String(30), default="")
    nickname_2 = Column(String(30), default="")
    nickname_3 = Column(String(30), default="")

    # One to One relation table
    user = relationship('User', back_populates='writer', uselist=False)
    novel = relationship('Novel', back_populates='writer', uselist=False, join_depth=1)

    # One to Many relation table
    commission = relationship('Commission', uselist=True)
    series = relationship('Series', back_populates='writer', join_depth=1, uselist=True)

    # Many to Many relation table
    novel_notice = relationship('NovelNotice', back_populates='writer', join_depth=1)
    cash_writer = relationship('CashWriter', back_populates='writer', join_depth=2)


class Commission(Base):
    writer_id = Column(Integer, ForeignKey('writer.id'), primary_key=True, index=True)
    manager_id = Column(Integer, ForeignKey('user.id'), primary_key=True, index=True)
    rate = Column(Float)
