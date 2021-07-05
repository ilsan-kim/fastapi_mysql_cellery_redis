from sqlalchemy import Column, Integer, String, Boolean

from app.db.base_class import Base


class OtherNovel(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), primary_key=True, nullable=False, index=True)
    is_activate = Column(Boolean, default=True)
