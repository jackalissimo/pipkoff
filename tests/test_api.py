import pytest
from os import environ
from datetime import datetime, timedelta
from openapi_client import openapi
from openapi_genclient.models import CandleResolution


AUTH_TOKEN = environ.get('AUTH_TOKEN')
acc_id = environ.get('ACCOUNT_ID')

def _test_default_portfolio():
    client = openapi.api_client(AUTH_TOKEN)
    # print('---client', dir(client))
    # print('---user', dir(client.user))

    pf = client.portfolio.portfolio_get()   # broker_account_id='Тинькофф'
    # pf = client.portfolio.portfolio_get(broker_account_id='ИИС')
    assert 'openapi_genclient.models.portfolio_response.PortfolioResponse' in str(type(pf))

    i=-1
    for pos in pf.payload.positions:
        i+=1
        value = pos.average_position_price.value
        curr = pos.average_position_price.currency
        avg_price_no_nkd = pos.average_position_price_no_nkd
        figi = pos.figi
        name = pos.name
        ticker = pos.ticker
        expected_yield = pos.expected_yield
        instrument_type = pos.instrument_type
        balance = pos.balance
        lots = pos.lots
        blocked = pos.blocked
        isin = pos.isin
        print("{0}\t{1}\t{2}\t{3}".format(lots, balance, figi, name))


def _test_user_accounts():
    client = openapi.api_client(AUTH_TOKEN)
    accs = client.user.user_accounts_get()
    print(accs)

def _test_iis_portfolio():
    client = openapi.api_client(AUTH_TOKEN)
    assert type(acc_id) == str
    assert len(acc_id) > 0
    pf = client.portfolio.portfolio_get(broker_account_id=acc_id)
    print(pf)
    assert pf.status == 'Ok'
    assert type(pf.payload.positions) == list


def _test_instr_search_by_figi():
    client = openapi.api_client(AUTH_TOKEN)
    resp = client.market.market_search_by_figi_get('BBG000BWPXQ8')
    assert resp.payload.name == 'British American Tobacco'
    print(resp)


def _test_instr_search_by_ticker():
    client = openapi.api_client(AUTH_TOKEN)
    resp = client.market.market_search_by_ticker_get('BTI')
    assert type(resp.payload.instruments) == list
    print(resp)


def _test_stocks_get():
    client = openapi.api_client(AUTH_TOKEN)
    stocks = client.market.market_stocks_get()  # openapi_genclient.models.market_instrument_list_response.MarketInstrumentListResponse
    assert 'openapi_genclient.models.market_instrument_list_response.MarketInstrumentListResponse' in str(type(stocks))
    print(type(stocks.payload))
    total = stocks.payload.total
    assert total > 1000
    assert type(stocks.payload.instruments) == list


def test_orderbook():
    """
    Стакан, глубина 1...20
    :return:
    """
    client = openapi.api_client(AUTH_TOKEN)
    figi = 'BBG004730JJ5'
    depth = 20
    orderbook = client.market.market_orderbook_get(figi=figi, depth=depth)
    assert orderbook.status == 'Ok'
    # print(orderbook)
    pl = orderbook.payload
    asks = pl.asks
    bids = pl.bids
    close_price = pl.close_price
    last_price = pl.last_price
    limit_down = pl.limit_down
    limit_up = pl.limit_up
    min_price_increment = pl.min_price_increment
    trade_status = pl.trade_status
    face_value = pl.face_value
    assert pl.figi == figi
    assert pl.depth == depth
    assert type(asks) == list
    assert type(bids) == list
    assert type(close_price) == float
    assert type(last_price) == float
    assert type(min_price_increment) == float
    assert asks[0].price < asks[1].price
    assert type(asks[0].quantity) == int
    assert bids[0].price < asks[0].price
    assert bids[1].price < bids[0].price



def test_market_candles_get_day():
    client = openapi.api_client(AUTH_TOKEN)
    ticker = 'VEON'
    figi = 'BBG000QCW561'
    pf = client.portfolio.portfolio_get(broker_account_id=acc_id)
    dt1 = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%dT%H:%M:%S+03:00")
    dt2 = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+03:00")
    resp = client.market.market_candles_get(figi, _from=dt1, to=dt2, interval=CandleResolution.DAY)
    assert resp.status == 'Ok'
    assert type(resp.payload.candles) == list
    assert type(resp.payload.candles[0].time) == datetime
    assert type(resp.payload.candles[0].c) == float
    assert type(resp.payload.candles[0].h) == float
    assert type(resp.payload.candles[0].l) == float
    assert type(resp.payload.candles[0].o) == float
    assert type(resp.payload.candles[0].v) == int
    assert resp.payload.candles[0].figi == figi
    assert resp.payload.candles[0].interval == CandleResolution.DAY


def test_market_candles_get_hour():
    client = openapi.api_client(AUTH_TOKEN)
    ticker = 'VEON'
    figi = 'BBG000QCW561'
    dt1 = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%dT%H:%M:%S+03:00")
    dt2 = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+03:00")
    resp = client.market.market_candles_get(figi, _from=dt1, to=dt2, interval=CandleResolution.HOUR)
    assert resp.status == 'Ok'
    assert type(resp.payload.candles) == list
    assert type(resp.payload.candles[0].time) == datetime
    assert type(resp.payload.candles[0].c) == float
    assert type(resp.payload.candles[0].h) == float
    assert type(resp.payload.candles[0].l) == float
    assert type(resp.payload.candles[0].o) == float
    assert type(resp.payload.candles[0].v) == int
    assert resp.payload.candles[0].figi == figi
    assert resp.payload.candles[0].interval == CandleResolution.HOUR

