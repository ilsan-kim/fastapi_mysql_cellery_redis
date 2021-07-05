from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Recommend(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user.id', ondelete="CASCADE"), primary_key=True, index=True)
    novel_id = Column(Integer, ForeignKey('novel.id', ondelete="CASCADE"), primary_key=True, index=True)
    title = Column(String(100))
    content = Column(String(500))

    # One to One relation table
    recommend_statistic = relationship('RecommendStatistic', uselist=False)

    # Many to Many relation table
    user_recommend_like = relationship('UserRecommendLike', back_populates='recommend', join_depth=1)


class RecommendStatistic(Base):
    recommend_id = Column(Integer, ForeignKey('recommend.id'), primary_key=True, index=True)
    view_count = Column(Integer)
    like_count = Column(Integer)
