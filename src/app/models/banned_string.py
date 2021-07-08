from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import ENUM

from app.db.base_class import Base


TYPE = ('NOVEL', 'COMMENT', 'NICKNAME')


class BannedString(Base):
    id = Column(Integer, primary_key=True, index=True)
    locate = Column(ENUM(*TYPE), default=TYPE[0])
    content = Column(String(100), default="", index=True)
    language_code = Column(String(30), ForeignKey('language.code'), default="all")