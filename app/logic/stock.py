from app.models import (
    Stock,
    db
)
from app.logic.tinkoff_client import client


def stock_init_db():
    stocks = client.market.market_stocks_get()
    total = stocks.payload.total
    assert total > 1000
    assert type(stocks.payload.instruments) == list
    for instr in stocks.payload.instruments:
        stock = None
        is_new = False
        try:
            stock = Stock.query.filter(Stock.figi == instr.figi).limit(1).one()
        except Exception:
            stock = Stock()
            is_new = True
        if not instr.min_price_increment:
            print('{0} {1}: no min_price_increment, set to 0.01'.format(instr.figi, instr.name))
        stock.currency = instr.currency
        stock.figi = instr.figi
        stock.isin = instr.isin
        stock.lot = instr.lot
        stock.min_price_increment = instr.min_price_increment or 0.01
        stock.name = instr.name
        stock.ticker = instr.ticker
        stock.type = instr.type
        if is_new:
            db.session.add(stock)
        db.session.commit()
