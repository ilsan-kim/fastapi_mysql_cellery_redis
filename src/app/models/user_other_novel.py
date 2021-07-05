from sqlalchemy import Column, Integer, ForeignKey, String

from app.db.base_class import Base


class UserOtherNovel(Base):
    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True, index=True)
    other_novel_name = Column(String(100), ForeignKey('other_novel.title'), index=True)
