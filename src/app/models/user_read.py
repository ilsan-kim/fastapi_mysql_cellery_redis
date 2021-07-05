from sqlalchemy import Column, Integer, ForeignKey

from app.db.base_class import Base


class UserRead(Base):
    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True, index=True)
    series_id = Column(Integer, ForeignKey('series.id'), primary_key=True, index=True)
