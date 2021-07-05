from sqlalchemy import Column, Integer, ForeignKey

from app.db.base_class import Base

class UserRecommendLike(Base):
    user_id = Column(Integer, ForeignKey('user.id', ondelete="CASCADE"), primary_key=True, index=True)
    recommend_id = Column(Integer, ForeignKey('recommend.id', ondelete="CASCADE"))