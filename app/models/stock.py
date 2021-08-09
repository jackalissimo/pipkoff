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


class Stock(db.Model):
    """
    Stock model
    """
    __tablename__ = 'stocks'

    id = Column(Integer(), primary_key=True)
    currency = Column(String(5), nullable=False)
    figi = Column(String(16), nullable=False, unique=True)
    isin = Column(String(16), nullable=False)
    lot = Column(Integer(), nullable=False)
    min_price_increment = Column(Float(), nullable=True)
    name = Column(String(64), nullable=False)
    ticker = Column(String(12), nullable=False, index=True)
    type = Column(String(16), nullable=False)
    active = Column(Integer(), nullable=False, default='1', server_default='1')
    date_update = Column(DateTime(), onupdate=func.now(), nullable=True)
