from sqlalchemy import Column, Integer, ForeignKey, String

from app.db.base_class import Base


class UserTag(Base):
    user_Id = Column(Integer, ForeignKey('user.id'), primary_key=True, index=True)
    tag_name = Column(String(30), ForeignKey('tag.name'), index=True)
