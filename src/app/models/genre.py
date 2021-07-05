from sqlalchemy import Column, Integer, String, Boolean

from app.db.base_class import Base


class Genre(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(30), nullable=False, index=True)
    is_activate = Column(Boolean, default=True)
