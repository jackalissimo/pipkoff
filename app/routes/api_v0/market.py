import json
from datetime import datetime, timedelta

from flask_restx import fields, Namespace
from flask_restx.reqparse import RequestParser
from flask import request
from http import HTTPStatus
from dateutil import parser as dparser

from .common import Resource, abort
from app.models import Candle, ma, Stock
from openapi_genclient.models import CandleResolution
from openapi_genclient.models.candle import Candle as TinCandle

from app.logic.tinkoff_client import client
from utils.date import date_format


market_ns = Namespace(
    name="market", description="CRUD market", path="/market"
)

candles_req_parser = RequestParser(bundle_errors=True)
candles_req_parser.add_argument(
    name='figi', type=str, required=False, nullable=True, location='query'
)
candles_req_parser.add_argument(
    name='ticker', type=str, required=False, nullable=True, location='query'
)
candles_req_parser.add_argument(
    name='_from', type=str, required=False, nullable=True, location='query'
)
candles_req_parser.add_argument(
    name='to', type=str, required=False, nullable=True, location='query'
)
candles_req_parser.add_argument(
    name='interval', type=str, required=True, nullable=False, location='query'
)


class CandleSchema(ma.Schema):
    class Meta:
        model = Candle
        fields = [
            'id',
            'figi',
            'c',
            'h',
            'l',
            'o',
            'v',
            'time',
            'interval',
        ]

class TinCandleSchema(ma.Schema):
    class Meta:
        model = TinCandle
        fields = [
            'c',
            'h',
            'l',
            'o',
            'v',
            'time',
            'interval',
        ]



@market_ns.route("/candles", endpoint='candles')
class MarketCandlesResource(Resource):
    @market_ns.expect(candles_req_parser)
    @market_ns.response(int(HTTPStatus.OK), description="Ok")
    @market_ns.response(int(HTTPStatus.BAD_REQUEST), description="Bad request")
    @market_ns.response(int(HTTPStatus.NOT_FOUND), description="Not found")
    @market_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), description="Server error")
    def get(self):
        figi = request.args.get('figi', default=None, type=str)
        ticker = request.args.get('ticker', default=None, type=str)
        interval = request.args.get('interval', default='hour', type=str)
        _from = request.args.get('_from', default=None, type=str)
        to = request.args.get('to', default=date_format(datetime.now()), type=str)
        if (not ticker) and (not figi):
            abort(HTTPStatus.BAD_REQUEST, 'required param: figi|ticker')
        if not figi:
            stocks = Stock.query.filter(Stock.ticker == ticker).all()
            if len(stocks) == 0:
                abort(HTTPStatus.INTERNAL_SERVER_ERROR, 'no figi found!')
            if len(stocks) > 1:
                figi_str = ", ".join([stock.figi for stock in stocks])
                abort(HTTPStatus.INTERNAL_SERVER_ERROR, "figi uncertainty! {0}".format(figi_str))
            figi = stocks[0].figi
        if interval not in CandleResolution.allowable_values:
            abort(HTTPStatus.BAD_REQUEST, 'Bad interval!')

        if not _from:
            _from = get_date_from(to, interval)
        tin_resp = client.market.market_candles_get(figi, _from=_from, to=to, interval=interval)
        assert tin_resp.status == 'Ok'
        assert type(tin_resp.payload.candles) == list
        candles = tin_resp.payload.candles
        tin_candle_schema = TinCandleSchema()
        res = tin_candle_schema.dump(candles, many=True)

        # and_vals = []
        # candles = Candle.query.filter(*and_vals).all()
        # candle_schema = CandleSchema()
        # res = candle_schema.dump(candles, many=True)
        return {'candles': res}, HTTPStatus.OK


@market_ns.route("/intervals", endpoint='intervals')
class IntervalResource(Resource):
    def get(self):
        intervals = CandleResolution.allowable_values
        return {'intervals': intervals}, HTTPStatus.OK


def get_date_from(date_to: str, interval: str):
    dt2 = dparser.parse(date_to)
    if interval == 'hour':
        dt1 = dt2 - timedelta(hours=7 * 24)
    elif interval == 'day':
        dt1 = dt2 - timedelta(days=90)
    elif interval == 'week':
        dt1 = dt2 - timedelta(weeks=104)
    elif interval == 'month':
        dt1 = dt2 - timedelta(weeks=150)
    elif interval == '30min':
        dt1 = dt2 - timedelta(hours=24)
    elif interval == '15min' or interval == '10min':
        dt1 = dt2 - timedelta(hours=24)
    elif interval == '5min' or interval == '3min':
        dt1 = dt2 - timedelta(hours=12)
    elif interval == '1min' or interval == '2min':
        dt1 = dt2 - timedelta(hours=3)
    else:
        dt1 = dt2 - timedelta(days=7)
    return date_format(dt1)
