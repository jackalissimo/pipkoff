from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.sql import func
from sqlalchemy.orm import (
    relationship,
    backref,
    declared_attr,
)
from sqlalchemy.ext.hybrid import hybrid_property
from .common import db


class Candle(db.Model):
    __abstract__ = True

    id = Column(Integer(), primary_key=True)
    ticker = Column(String(8), nullable=True)
    o = Column(Float(), nullable=False)
    h = Column(Float(), nullable=False)
    l = Column(Float(), nullable=False)
    c = Column(Float(), nullable=False)
    v = Column(Integer(), nullable=False)
    time = Column(DateTime(timezone=True), nullable=False)

    @declared_attr
    def stock_id(cls):
        return Column(Integer(), ForeignKey('stocks.id'), nullable=False, index=True)

    date_update = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        db.UniqueConstraint('stock_id', 'time'),
    )


class CandleHour(Candle):
    __tablename__ = 'candle_hour'


class CandleDay(Candle):
    __tablename__ = 'candle_day'


class CandleWeek(Candle):
    __tablename__ = 'candle_week'


class CandleMonth(Candle):
    __tablename__ = 'candle_month'


class Candle30Min(Candle):
    __tablename__ = 'candle_30min'


class Candle15Min(Candle):
    __tablename__ = 'candle_15min'


class Candle10Min(Candle):
    __tablename__ = 'candle_10min'


class Candle5Min(Candle):
    __tablename__ = 'candle_5min'


class Candle3Min(Candle):
    __tablename__ = 'candle_3min'


class Candle2Min(Candle):
    __tablename__ = 'candle_2min'


class Candle1Min(Candle):
    __tablename__ = 'candle_1min'


def candle_factory_get(interval: str, clsname_only=False):
    d = {
        'hour': 'CandleHour',
        'day' : 'CandleDay',
        'week' : 'CandleWeek',
        'month': 'CandleMonth',
        '30min': 'Candle30Min',
        '15min': 'Candle15Min',
        '10min': 'Candle10Min',
        '5min' : 'Candle5Min',
        '3min' : 'Candle3Min',
        '2min' : 'Candle2Min',
        '1min' : 'Candle1Min',
    }
    if interval in d:
        if clsname_only:
            return d[interval]
        else:
            return d[interval]()
    else:
        raise UnknownIntervalException


class UnknownIntervalException(Exception):
    pass
