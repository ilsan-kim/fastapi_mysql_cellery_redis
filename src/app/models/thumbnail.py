from sqlalchemy import Column, Integer, String, ForeignKey

from app.db.base_class import Base


class Thumbnail(Base):
    id = Column(Integer, primary_key=True, index=True)
    image_url = Column(String(300), default="")
    title = Column(String(100), default="")
    genre = Column(String(30), ForeignKey('genre.name'))
    manager_id = Column(Integer, ForeignKey('user.id'))
