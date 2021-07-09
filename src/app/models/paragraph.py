from sqlalchemy import Column, Integer, ForeignKey, Text, String, Boolean
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Paragraph(Base):
    id = Column(Integer, primary_key=True, index=True)
    series_id = Column(Integer, ForeignKey('series.id'), index=True)
    order_number = Column(Integer, nullable=False)
    text = Column(Text(20_000), default="")
    language_code = Column(String(30), ForeignKey('language.code'))
    like_count = Column(Integer)
    is_origin = Column(Boolean, default=False)
    is_selected = Column(Boolean, default=False)

    # Many to One relation
    series = relationship('Series', back_populates='paragraph', join_depth=1)

    # Many to Many relation
    user_paragraph = relationship('UserParagraph', back_populates='paragraph', join_depth=2)
    user_translate_like = relationship('UserTranslateLike', back_populates='paragraph', join_depth=1)
