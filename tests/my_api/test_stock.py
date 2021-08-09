import requests
import json

from tests.my_api.common import TestMyApiBase


class TestStock(TestMyApiBase):
    def test_stock_get_by_id(self):
        id  = 1658
        figi = 'BBG000BT7ZK6'
        ticker = 'SONY'
        res = requests.get(self.base_url + 'stock', params={'id': id})
        assert res.status_code == 200
        cont = json.loads(res.content)
        stock = cont['data']['stocks'][0]
        assert stock['ticker'] == ticker
        assert stock['figi'] == figi
        assert stock['id'] == id


    def test_stock_get_by_figi(self):
        id = 1658
        figi = 'BBG000BT7ZK6'
        ticker = 'SONY'
        res = requests.get(self.base_url + 'stock', params={'figi': figi})
        assert res.status_code == 200
        cont = json.loads(res.content)
        stock = cont['data']['stocks'][0]
        assert stock['ticker'] == ticker
        assert stock['figi'] == figi
        assert stock['id'] == id


    def test_stock_get_by_ticker(self):
        id = 1658
        figi = 'BBG000BT7ZK6'
        ticker = 'SONY'
        res = requests.get(self.base_url + 'stock', params={'ticker': ticker})
        assert res.status_code == 200
        cont = json.loads(res.content)
        assert len(cont['data']['stocks']) == 1
        stock = cont['data']['stocks'][0]
        assert stock['ticker'] == ticker
        assert stock['figi'] == figi
        assert stock['id'] == id


    def test_stock_get_404(self):
        id = 44
        figi = 'BBG000BT7ZK6'
        ticker = 'SONY'
        res = requests.get(self.base_url + 'stock', params={'ticker': ticker, 'id': id})
        assert res.status_code == 404


    def test_stock_get_400_on_no_params(self):
        id = 44
        figi = 'BBG000BT7ZK6'
        ticker = 'SONY'
        res = requests.get(self.base_url + 'stock', params={})
        assert res.status_code == 400
