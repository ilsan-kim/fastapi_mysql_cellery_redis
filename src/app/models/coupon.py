from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import ENUM

from app.db.base_class import Base

SOURCE = ('WELCOME', 'CASH', 'EVENT')


class Coupon(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user.id'), index=True)
    source = Column(ENUM(*SOURCE))
    amount = Column(Integer)

    # Many to Many relation
    coupon_series = relationship('CouponSeries', back_populates='coupon', join_depth=1)
