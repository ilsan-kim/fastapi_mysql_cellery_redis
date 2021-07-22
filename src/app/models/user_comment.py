from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class UserComment(Base):
    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True, index=True)
    comment_id = Column(Integer, ForeignKey('comment.id'), primary_key=True, index=True)

    # Many to Many relation
    user = relationship('User', back_populates='user_comment')
    comment = relationship('Comment', back_populates='user_comment')
