from sqlalchemy import Column, Integer, ForeignKey

from app.db.base_class import Base


class CashSeries(Base):
    cash_id = Column(Integer, ForeignKey('cash.id'), primary_key=True, index=True)
    series_id = Column(Integer, ForeignKey('series.id'), primary_key=True, index=True)
    amount = Column(Integer)
