from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class CashWriter(Base):
    cash_id = Column(Integer, ForeignKey('cash.id'), primary_key=True, index=True)
    writer_id = Column(Integer, ForeignKey('writer.id'), primary_key=True, index=True)
    amount = Column(Integer)

    # Many to Many relation
    cash = relationship('Cash', back_populates='cash_writer')
    writer = relationship('Writer', back_populates='cash_writer')