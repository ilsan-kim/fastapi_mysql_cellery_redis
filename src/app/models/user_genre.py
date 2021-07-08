from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class UserGenre(Base):
    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True, index=True)
    genre_code = Column(String(30), ForeignKey('genre.code'), index=True)

    # Many to Many relation
    user = relationship('User', back_populates='user_genre')
    genre = relationship('Genre', back_populates='user_genre')