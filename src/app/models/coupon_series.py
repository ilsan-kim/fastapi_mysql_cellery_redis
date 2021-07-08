from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class CouponSeries(Base):
    coupon_id = Column(Integer, ForeignKey('coupon.id'), primary_key=True, index=True)
    series_id = Column(Integer, ForeignKey('series.id'), primary_key=True, index=True)
    amount = Column(Integer)

    # Many to Many relation
    coupon = relationship('Coupon', back_populates='coupon_series')
    series = relationship('Series', back_populates='coupon_series')