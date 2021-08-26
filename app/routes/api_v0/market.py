import json
from datetime import datetime, timedelta

from flask_restx import fields, Namespace
from flask_restx.reqparse import RequestParser
from flask import request
from http import HTTPStatus
from dateutil import parser as dparser
import importlib

from .common import Resource, abort
from app.models import (
    ma,
    Stock, db
)
from openapi_genclient.models import CandleResolution
from openapi_genclient.models.candle import Candle as TinCandle

from app.logic.tinkoff_client import client
from app.logic.date import (
    date_format,
    get_date_from,
    get_from_to_intervals
)
from app.models.market import candle_factory_get


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
    name='from', type=str, required=False, nullable=True, location='query'
)
candles_req_parser.add_argument(
    name='to', type=str, required=False, nullable=True, location='query'
)
candles_req_parser.add_argument(
    name='interval', type=str, required=True, nullable=False, location='query'
)


# class CandleSchema(ma.Schema):
#     class Meta:
#         model = Candle
#         fields = [
#             'id',
#             'figi',
#             'c',
#             'h',
#             'l',
#             'o',
#             'v',
#             'time',
#             'interval',
#         ]

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


@market_ns.route('/candles', endpoint='candles')
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
        _from = request.args.get('from', default=None, type=str)
        to = request.args.get('to', default=date_format(datetime.now()), type=str)
        dt_to = dparser.parse(to)
        to = date_format(dt_to)
        if not _from:
            _from = get_date_from(to, interval)
        dt_from = dparser.parse(_from)
        _from = date_format(dt_from)
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

        tin_resp = client.market.market_candles_get(figi, _from=_from, to=to, interval=interval)
        assert tin_resp.status == 'Ok'
        assert type(tin_resp.payload.candles) == list
        candles = tin_resp.payload.candles
        tin_candle_schema = TinCandleSchema()
        res = tin_candle_schema.dump(candles, many=True)
        return {'candles': res}, HTTPStatus.OK


@market_ns.route("/intervals", endpoint='intervals')
class IntervalResource(Resource):
    def get(self):
        intervals = CandleResolution.allowable_values
        return {'intervals': intervals}, HTTPStatus.OK


####################################################
parse_req_parser = RequestParser(bundle_errors=True)
parse_req_parser.add_argument(
    name='figi', type=str, required=False, nullable=True
)
parse_req_parser.add_argument(
    name='ticker', type=str, required=False, nullable=True
)
parse_req_parser.add_argument(
    name='stock_id', type=int, required=False, nullable=True
)
parse_req_parser.add_argument(
    name='from', type=str, required=False, nullable=True
)
parse_req_parser.add_argument(
    name='to', type=str, required=False, nullable=True
)
parse_req_parser.add_argument(
    name='interval', type=str, required=True, nullable=False
)


@market_ns.route("/candles/parse", endpoint='candles-parse')
class MarketCandlesResource(Resource):
    @market_ns.expect(parse_req_parser)
    @market_ns.response(int(HTTPStatus.OK), description="Ok")
    @market_ns.response(int(HTTPStatus.BAD_REQUEST), description="Bad request")
    @market_ns.response(int(HTTPStatus.NOT_FOUND), description="Not found")
    @market_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), description="Server error")
    def post(self):
        """
        FIll db with candles parsed.
        Usually requires more than 1 request to Broker.
        """
        figi = request.args.get('figi', default=None, type=str)
        ticker = request.args.get('ticker', default=None, type=str)
        stock_id = request.args.get('stock_id', default=None, type=int)
        interval = request.args.get('interval', default='hour', type=str)
        _from = request.args.get('from', default=None, type=str)
        to = request.args.get('to', default=date_format(datetime.now()), type=str)
        dt_to = dparser.parse(to)
        to = date_format(dt_to)
        if not _from:
            _from = get_date_from(to, interval)
        dt_from = dparser.parse(_from)
        _from = date_format(dt_from)
        if (not ticker) and (not figi) and (not stock_id):
            abort(HTTPStatus.BAD_REQUEST, 'required param: figi|ticker|stock_id')
        if not figi:
            if stock_id:
                stock = Stock.query.get(stock_id)
                if not stock:
                    abort(HTTPStatus.INTERNAL_SERVER_ERROR, 'stock_id not found!')
                figi = stock.figi
            elif ticker:
                stocks = Stock.query.filter(Stock.ticker == ticker).all()
                if len(stocks) == 0:
                    abort(HTTPStatus.INTERNAL_SERVER_ERROR, 'no figi found!')
                if len(stocks) > 1:
                    figi_str = ", ".join([stock.figi for stock in stocks])
                    abort(HTTPStatus.INTERNAL_SERVER_ERROR, "figi uncertainty! {0}".format(figi_str))
                figi = stocks[0].figi
        if not figi:
            abort(HTTPStatus.INTERNAL_SERVER_ERROR, 'no figi defined!')
        if interval not in CandleResolution.allowable_values:
            abort(HTTPStatus.BAD_REQUEST, 'Bad interval!')
        try:
            stock
        except:
            stock = Stock.query.filter(Stock.figi == figi).limit(1).one()
        if not stock_id:
            stock_id = stock.id

        interval_list = get_from_to_intervals(interval, dt_from, dt_to)
        candle_clsname = candle_factory_get(interval, True)
        module = importlib.import_module('app.models.market')
        cls = getattr(module, candle_clsname)
        # TODO: make async batch calls
        candle_counter = 0
        counter_old = 0
        counter_new = 0
        for from_x, to_x in interval_list:
            tin_resp = client.market.market_candles_get(figi, _from=from_x, to=to_x, interval=interval)
            assert tin_resp.status == 'Ok'
            assert type(tin_resp.payload.candles) == list
            candles = tin_resp.payload.candles
            for row in candles:
                candle_counter +=1
                try:
                    candle = cls.query.filter(cls.stock_id == stock_id, cls.time == row.time).one()
                    exists = True
                    counter_old +=1
                except:
                    candle = cls()
                    exists = False
                    counter_new +=1
                candle.ticker = stock.ticker
                candle.stock_id = stock_id
                candle.time = row.time
                candle.o = row.o
                candle.h = row.h
                candle.l = row.l
                candle.c = row.c
                candle.v = row.v
                if not exists:
                    db.session.add(candle)
                db.session.commit()
        res = {
            'candles_parsed': candle_counter,
            'new': counter_new,
            'old': counter_old
        }
        return res, HTTPStatus.OK
