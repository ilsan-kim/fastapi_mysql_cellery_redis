from sqlalchemy import Column, Integer, ForeignKey

from app.db.base_class import Base


class CashWriter(Base):
    cash_id = Column(Integer, ForeignKey('cash.id'), primary_key=True, index=True)
    writer_id = Column(Integer, ForeignKey('user.id'), primary_key=True, index=True)
    amount = Column(Integer)
