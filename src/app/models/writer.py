from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Writer(Base):
    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True, index=True, nullable=False)
    is_contracted = Column(Boolean, default=False)
    commission_rate = Column(Float, default=0.6)
    nickname_1 = Column(String(30))
    nickname_2 = Column(String(30))
    nickname_3 = Column(String(30))

    # One to One relation table
    user = relationship('User', back_populates='writer', uselist=False)

    # One to Many relation table
    commission = relationship('Commission', uselist=True)


class Commission(Base):
    writer_id = Column(Integer, ForeignKey('writer.user_id'), primary_key=True, index=True)
    manager_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    rate = Column(Float)