from sqlalchemy import (
    Column,
    DateTime,
    Date,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)

from .common import db


class Snp500(db.Model):
    id = Column(Integer(), primary_key=True)
    ticker = Column(String(8), nullable=False, unique=True)
    name = Column(String(80), nullable=False)
    gics_sector = Column(String(80), nullable=True, comment="Global Industry Classification Standart Sector")
    gics_subindustry = Column(String(80), nullable=True, comment="Global Industry Classification Standart Sub-Industry")
    hq_location = Column(String(80), nullable=True, comment="headquaters location")
    info_source = Column(String(80), nullable=True)
    date_first_added = Column(Date(), nullable=True)
    date_first_added_opt = Column(String(80), nullable=True)
    cik = Column(String(16), nullable=True, comment="Central Index Key")
    founded = Column(String(80), nullable=True)


class Snp500Changes(db.Model):
    id = Column(Integer(), primary_key=True)
    date = Column(Date(), nullable=False)
    ticker_added = Column(String(8), nullable=False, index=True)
    name_added = Column(String(80), nullable=False)
    ticker_removed = Column(String(8), nullable=False, index=True)
    name_removed = Column(String(80), nullable=False)
    reason = Column(Text(), nullable=True)
    info_source = Column(String(80), nullable=True)

