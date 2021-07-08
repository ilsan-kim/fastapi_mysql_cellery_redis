from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Region(Base):
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(30), nullable=False, index=True, unique=True)
    is_activate = Column(Boolean, default=True)

    # One to Many relation
    region_detail = relationship('RegionDetail', back_populates='region', uselist=True)


class RegionDetail(Base):
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(30), ForeignKey('region.code'), index=True)
    language_code = Column(String(30), ForeignKey('language.code'), default='kr')
    name = Column(String(30), default="")

    # Many to One relation
    region = relationship('Region',  back_populates='region_detail')