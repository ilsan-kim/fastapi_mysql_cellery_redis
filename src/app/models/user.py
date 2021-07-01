from typing import TYPE_CHECKING
import enum

from sqlalchemy import Boolean, Column, Integer, String, JSON, Enum
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .timetable import Timetable    # noqa: F401


class SnsLoginSource(enum.Enum):
    NAVER = 'naver'
    GOOGLE = 'google'


class User(Base):
    id = Column(Integer, primary_key=True, indext=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    profile = Column(JSON)
    auth_key = Column(String, unique=True)
    source = Column(Enum(SnsLoginSource))
    timetables = relationship('Timetable', back_populates='user', lazy='noload')