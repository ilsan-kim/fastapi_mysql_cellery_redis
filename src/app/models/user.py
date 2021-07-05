from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import ENUM

from app.db.base_class import Base


GENDER = ('ETC', 'MALE', 'FEMALE')

SNS_PROVIDER = ('NAVER', 'GOOGLE', 'KAKAO', 'FACEBOOK')

STATUS = ('NORMAL', 'WARNING', 'WARNING2', 'WARNING3', 'PAUSED', 'BANNED')


class User(Base):
    """
    유저의 기본 메타데이터 저장
    """
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(30), index=True)
    hashed_password = Column(String(64), nullable=False)
    nickname = Column(String(30), nullable=False)
    name = Column(String(30), nullable=False)
    phone_number = Column(String(30), default="")
    gender = Column(ENUM(*GENDER), default=GENDER[0])
    email = Column(String(100), unique=True, index=True, nullable=False)
    region = Column(Integer, ForeignKey('region.id'))
    language = Column(Integer, ForeignKey('language.id'))
    status = Column(ENUM(*STATUS), default=STATUS[0])
    is_super = Column(Boolean, default=False)
    is_authenticated = Column(Boolean, default=False)
    accept_notification = Column(Boolean, default=False)
    accept_mailing = Column(Boolean, default=False)
    login_at = Column(DateTime)

    # One to One relation table
    sns_account = relationship('SnsAccount', back_populates='user', uselist=False)
    banking_info = relationship('BankingInfo', back_populates='user', uselist=False)
    writer = relationship('Writer', back_populates='user', uselist=False)

    # One to Many relation table
    novel = relationship('Novel', back_populates='user', join_depth=1)
    novel_notice = relationship('NovelNotice', back_populates='user', join_depth=1)
    series = relationship('Series', back_populates='user', join_depth=1)
    commission = relationship('Commission')
    thumbnail = relationship('Thumbnail')

    # Many to Many relation table
    user_like = relationship('UserLike', back_populates='user', join_depth=1)
    user_read = relationship('UserRead', back_populates='user', join_depth=1)
    user_rating = relationship('UserRating', back_populates='user', join_depth=1)
    user_paragraph = relationship('UserParagraph', back_populates='user', join_depth=2)
    comment = relationship('Comment', back_populates='user', join_depth=1)
    user_other_novel = relationship('UserOtherNovel', back_populates='user', join_depth=1)
    cash_series = relationship('CashSeries', back_populates='user', join_depth=1)
    cash_writer = relationship('CashWriter', back_populates='user', join_depth=2)
    coupon_series = relationship('CouponSeries', back_populates='user', join_depth=1)
    recommend = relationship('Recommend', back_populates='user', join_depth=1)
    user_recommend_like = relationship('UserRecommendLike', back_populates='user', join_depth=1)


class SnsAccount(Base):
    """
    SNS 인증정보 저장
    """
    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True, nullable=False)
    sns_provider = Column(ENUM(*SNS_PROVIDER), nullable=True)
    sns_id = Column(String(30))
    auth_key = Column(String(100))

    # One to One relation table
    user = relationship('User', back_populates='sns_account', uselist=False)


class BankingInfo(Base):
    """
    은행 계좌 정보 저장
    """
    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True, nullable=False)
    bank_name = Column(String(30), nullable=False, default="")
    bank_account = Column(String(30), nullable=False, default="")
    account_holder = Column(String(30), nullable=False, default="")

    # One to One relation table
    user = relationship('User', back_populates='banking_info', uselist=False)
