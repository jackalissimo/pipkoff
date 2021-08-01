from tests.api.common import TestBaseApi


class TestMarket(TestBaseApi):
    def test_market_stocks_get(self):
        stocks = self.client.market.market_stocks_get()  # openapi_genclient.models.market_instrument_list_response.MarketInstrumentListResponse
        assert 'openapi_genclient.models.market_instrument_list_response.MarketInstrumentListResponse' in str(
            type(stocks))
        print(type(stocks.payload))
        total = stocks.payload.total
        assert total > 1000
        assert type(stocks.payload.instruments) == list
        instr0 = stocks.payload.instruments[0]
        assert 'currency' in instr0
        assert 'figi' in instr0
        assert 'isin' in instr0
        assert 'lot' in instr0
        assert 'min_price_increment' in instr0
        assert 'name' in instr0
        assert 'ticker' in instr0
        assert 'type' in instr0
        print(stocks.payload)
