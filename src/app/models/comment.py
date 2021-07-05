from sqlalchemy import Column, Integer, ForeignKey, String

from app.db.base_class import Base


class Comment(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user.id', ondelete="CASCADE"), primary_key=True, index=True)
    series_id = Column(Integer, ForeignKey('series.id', ondelete="CASCADE"), primary_key=True, index=True)
    content = Column(String(1000))
