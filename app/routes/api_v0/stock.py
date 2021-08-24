from flask_restx import fields, Namespace
from flask_restx.reqparse import RequestParser
from flask import request
from http import HTTPStatus

from .common import Resource, abort
from app.models import Stock, ma
from app.logic.stock import stock_init_db

stock_ns = Namespace(
    name="stock", description="CRUD stock", path="/stock"
)

stock_req_parser = RequestParser(bundle_errors=True)
stock_req_parser.add_argument(
    name='figi', type=str, required=False, nullable=True, location='query'
)
stock_req_parser.add_argument(
    name='id', type=int, required=False, nullable=True, location='query'
)
stock_req_parser.add_argument(
    name='ticker', type=str, required=False, nullable=True, location='query'
)
stock_req_parser.add_argument(
    name='name', type=str, required=False, nullable=True, location='query'
)

class StockSchema(ma.Schema):
    class Meta:
        model = Stock
        fields = [
            'id',
            'currency',
            'figi',
            'ticker',
            'name',
            'lot',
            'min_price_increment',
            'type',
            'isin',
            'active',
        ]

@stock_ns.route("", endpoint='stock')
class StockResource(Resource):
    @stock_ns.expect(stock_req_parser)
    @stock_ns.response(int(HTTPStatus.OK), description="Запрос создан")
    @stock_ns.response(int(HTTPStatus.BAD_REQUEST), description="Ошибка валидации")
    @stock_ns.response(int(HTTPStatus.NOT_FOUND), description="Не найден")
    @stock_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), description="Ошибка сервера")
    def get(self):
        figi = request.args.get('figi', default=None, type=str)
        id = request.args.get('id', default=None, type=int)
        ticker = request.args.get('ticker', default=None, type=str)
        name = request.args.get('name', default=None, type=str)
        if (not figi) and (not id) and (not ticker) and (not name):
            abort(HTTPStatus.BAD_REQUEST, 'required param: figi|id|ticker|name')
        and_vals = []
        if figi:
            and_vals.append(Stock.figi == figi)
        if id:
            and_vals.append(Stock.id == id)
        if ticker:
            and_vals.append(Stock.ticker == ticker)
        if name:
            and_vals.append(Stock.name.ilike("%{0}%".format(name)))
        stocks = Stock.query.filter(*and_vals).all()
        stock_schema = StockSchema()
        res = stock_schema.dump(stocks, many=True)
        if len(stocks) == 0:
            return {'stocks': res}, HTTPStatus.NOT_FOUND
        return {'stocks': res}, HTTPStatus.OK


@stock_ns.route('/init', endpoint='stock-init')
class StockInitResource(Resource):
    @stock_ns.response(int(HTTPStatus.OK), description="Запрос создан")
    @stock_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), description="Ошибка сервера")
    def post(self):
        """
        parse all stocks meta and save to db
        """
        if stock_init_db(verbose=True):
            return {}, HTTPStatus.OK
        else:
            abort(HTTPStatus.INTERNAL_SERVER_ERROR, 'stocks metadata parsing failed')
