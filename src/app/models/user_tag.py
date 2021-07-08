from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class UserTag(Base):
    user_Id = Column(Integer, ForeignKey('user.id'), primary_key=True, index=True)
    tag_code = Column(String(30), ForeignKey('tag.code'), primary_key=True, index=True)

    # Many to Many relation
    user = relationship('User', back_populates='user_tag')
    tag = relationship('Tag', back_populates='user_tag')