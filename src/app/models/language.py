from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Language(Base):
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(10), nullable=False, index=True)
    is_activate = Column(Boolean, default=True)


class LanguageDetail(Base):
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(30), ForeignKey('language.code'), index=True)
    language_code = Column(String(30), ForeignKey('language.code'), default='kr')
    name = Column(String(30), default="")

    code_itself = relationship('Language', foreign_keys=[code])
    code_presented = relationship('Language', foreign_keys=[language_code])