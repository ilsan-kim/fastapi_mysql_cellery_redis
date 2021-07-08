from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class UserRecommendLike(Base):
    user_id = Column(Integer, ForeignKey('user.id', ondelete="CASCADE"), primary_key=True, index=True)
    recommend_id = Column(Integer, ForeignKey('recommend.id', ondelete="CASCADE"), primary_key=True, index=True)

    # Many to Many relation
    user = relationship('User', back_populates='user_recommend_like')
    recommend = relationship('Recommend', back_populates='user_recommend_like')