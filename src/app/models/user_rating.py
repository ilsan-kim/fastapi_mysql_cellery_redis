from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class UserRating(Base):
    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True, index=True)
    series_id = Column(Integer, ForeignKey('series.id'), primary_key=True, index=True)
    rating = Column(Integer, nullable=False)

    # Many to Many relation
    user = relationship('User', back_populates='user_rating')
    series = relationship('Series', back_populates='user_rating')