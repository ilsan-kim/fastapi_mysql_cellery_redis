from typing import TYPE_CHECKING
import enum
import datetime

from sqlalchemy import Boolean, Column, Integer, String, JSON, Enum, DateTime
from sqlalchemy.orm import relationship

from ..db.base_class import Base

if TYPE_CHECKING:
    from .timetable import Timetable    # noqa: F401


class SnsLoginSource(enum.Enum):
    NAVER = 'naver'
    GOOGLE = 'google'
    KAKAO = 'kakao'
    FACEBOOK = 'facebook'


class Status(enum.Enum):
    NORMAL = '정상'
    WARNING = '경고'
    WARNING2 = '경고2'
    PAUSED = '일시정지'
    BANNED = '영구정지'


class User(Base):
    id = Column(Integer, primary_key=True, indext=True)
    username = Column(String, index=True)
    hashed_password = Column(String, nullable=False)
    nickname = Column(String, nullable=False)
    name = Column(String, nullable=False)
    phone_number = Column(String, default='')
    gender = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    region = Column(String, nullable=False)
    language = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now)
    login_at = Column(DateTime)
    status = Column(String, nullable=False)
    is_super = Column(Boolean, default=False)
    is_authenticated = Column(Boolean, default=False)
    accept_notification = Column(Boolean, default=False)
    accept_mailing = Column(Boolean, default=False)

    cash = relationship('Cash', back_populates='user', lazy='joined', join_depth=1)
    coupon = relationship('Coupon', back_populates='user', lazy='joined', join_depth=1)