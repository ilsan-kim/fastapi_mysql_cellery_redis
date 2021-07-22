from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Comment(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user.id', ondelete="CASCADE"), index=True)
    series_id = Column(Integer, ForeignKey('series.id', ondelete="CASCADE"), index=True)
    content = Column(String(1000))
    image_url = Column(String(300))
    like_count = Column(Integer, default=0)

    # Many to Many relation table
    user = relationship('User', back_populates='comment')
    series = relationship('Series', back_populates='comment')
    user_comment = relationship('UserComment', back_populates='comment')