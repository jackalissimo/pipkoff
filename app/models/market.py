from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.hybrid import hybrid_property
from .common import db


class Candle(db.Model):
    """
    Stock model
    """
    __tablename__ = 'candles'

    id = Column(Integer(), primary_key=True)
    figi = Column(String(16), ForeignKey('stocks.figi'), nullable=False, index=True)
    c = Column(Float(), nullable=False)
    h = Column(Float(), nullable=False)
    l = Column(Float(), nullable=False)
    o = Column(Float(), nullable=False)
    v = Column(Integer(), nullable=False)
    time = Column(DateTime(), nullable=False)
    interval = Column(String(16), nullable=False)

    __table_args__ = (
        db.Index('candles_interval_time_idx', figi, interval, time.desc()),
    )
