from sqlalchemy import Column, Integer, ForeignKey, String, Text

from app.db.base_class import Base


class TempSave(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True, index=True)
    novel_id = Column(Integer, ForeignKey('novel.id'), primary_key=True, index=True)
    title = Column(String(100), default="")
    text = Column(Text(20_000), default="")
