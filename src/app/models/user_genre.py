from sqlalchemy import Column, Integer, ForeignKey, String

from app.db.base_class import Base


class UserGenre(Base):
    user_Id = Column(Integer, ForeignKey('user.id'), primary_key=True, index=True)
    genre_name = Column(String(30), ForeignKey('genre.name'), index=True)
