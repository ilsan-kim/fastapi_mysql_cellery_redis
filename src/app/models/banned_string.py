from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import ENUM

from app.db.base_class import Base


TYPE = ('NOVEL', 'COMMENT', 'NICKNAME')


class BannedString(Base):
    id = Column(Integer, primary_key=True, index=True)
    type = Column(ENUM(*TYPE), default=TYPE[0])
    content = Column(String(100), default="", index=True)

    # Many to One relation table
    novel = relationship('Novel', back_populates='paragraph', join_depth=1)
    writer = relationship('User', back_populates='paragraph', join_depth=2)
