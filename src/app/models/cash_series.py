from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class CashSeries(Base):
    cash_id = Column(Integer, ForeignKey('cash.id'), primary_key=True, index=True)
    series_id = Column(Integer, ForeignKey('series.id'), primary_key=True, index=True)
    amount = Column(Integer)

    # Many to Many relation
    cash = relationship('Cash', back_populates='cash_series')
    series = relationship('Series', back_populates='cash_series')