from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Genre(Base):
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(30), nullable=False, index=True, unique=True)
    is_activate = Column(Boolean, default=True)

    # Many to Many relation
    user_genre = relationship('UserGenre', back_populates='genre')

    # One to Many relation
    genre_detail = relationship('GenreDetail', back_populates='genre', uselist=True)


class GenreDetail(Base):
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(30), ForeignKey('genre.code'), index=True)
    language_code = Column(String(30), ForeignKey('language.code'), default='kr')
    name = Column(String(30), default="")

    # Many to One relation
    genre = relationship('Genre', back_populates='genre_detail')
