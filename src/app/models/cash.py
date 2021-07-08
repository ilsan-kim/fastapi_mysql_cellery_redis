from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import ENUM

from app.db.base_class import Base, BaseNoDatetime

SOURCE = ('NPAY', 'KAKAOPAY', 'CREDITCARD')


class Cash(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user.id'), index=True)
    source = Column(ENUM(*SOURCE))
    amount = Column(Integer)
    expired_at = Column(DateTime)

    # Many to Many relation
    cash_series = relationship('CashSeries', back_populates='cash', join_depth=1)
    cash_writer = relationship('CashWriter', back_populates='cash', join_depth=2)
