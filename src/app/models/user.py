import enum

from sqlalchemy import Boolean, Column, Integer, String, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base

class SnsProviderType(enum.Enum):
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
    """
    유저의 기본 메타데이터 저장
    """
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    hashed_password = Column(String, nullable=False)
    nickname = Column(String, nullable=False)
    name = Column(String, nullable=False)
    phone_number = Column(String, default="")
    gender = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    region = Column(String, nullable=False)
    language = Column(String, nullable=False)
    status = Column(String, nullable=False)
    is_super = Column(Boolean, default=False)
    is_authenticated = Column(Boolean, default=False)
    accept_notification = Column(Boolean, default=False)
    accept_mailing = Column(Boolean, default=False)
    login_at = Column(DateTime)

    # One to One relation table with SnsAccount & BankingInfo
    sns_account = relationship('SnsAccount', back_populates='user', uselist=False)
    banking_info = relationship('BankingInfo', back_populates='user', uselist=False)


class SnsAccount(Base):
    """
    SNS 인증정보 저장
    """
    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True, nullable=False)
    sns_provider = Column(Enum(SnsProviderType))
    sns_id = Column(String)
    auth_key = Column(String)

    # One to One relation table with User
    user = relationship('User', back_populates='sns_account', uselist=False)


class BankingInfo(Base):
    """
    은행 계좌 정보 저장
    """
    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True, nullable=False)
    bank_name = Column(String, nullable=False, default="")
    bank_account = Column(String, nullable=False, default="")
    account_holder = Column(String, nullable=False, default="")

    # One to One relation table with User
    user = relationship('User', back_populates='banking_info', uselist=False)