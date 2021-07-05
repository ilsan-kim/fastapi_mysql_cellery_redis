from sqlalchemy import Column, Integer, ForeignKey, Text, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Paragraph(Base):
    id = Column(Integer, primary_key=True, index=True)
    series_id = Column(Integer, ForeignKey('series.id'), index=True)
    writer_id = Column(Integer, ForeignKey('user.id'), index=True)
    translator_id = Column(Integer, ForeignKey('user.id'), index=True)
    order_number = Column(Integer, nullable=False)
    text = Column(Text(20_000), default="")
    language = Column(String(30), ForeignKey('language.name'))

    # Many to One relation table
    series = relationship('Series', back_populates='paragraph', join_depth=1)

    # Many to Many relation table
    user_paragraph = relationship('UserParagraph', back_populates='paragraph', join_depth=2)
